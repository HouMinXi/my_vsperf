# Copyright 2015-2016 Intel Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Automation of QEMU hypervisor for launching guests.
"""

import os
import logging
import locale
import re
import subprocess
import time
import pexpect

from conf import settings as S
from conf import get_test_param
from vnfs.vnf.vnf import IVnf

class IVnfQemu(IVnf):
    """
    Abstract class for controling an instance of QEMU
    """
    _cmd = None
    _expect = None
    _proc_name = 'qemu'

    class GuestCommandFilter(logging.Filter):
        """
        Filter out strings beginning with 'guestcmd :'.
        """
        def filter(self, record):
            return record.getMessage().startswith(self.prefix)

    def __init__(self):
        """
        Initialisation function.
        """
        super(IVnfQemu, self).__init__()

        self._expect = S.getValue('GUEST_PROMPT_LOGIN')[self._number]
        self._logger = logging.getLogger(__name__)
        self._logfile = os.path.join(
            S.getValue('LOG_DIR'),
            S.getValue('LOG_FILE_QEMU')) + str(self._number)
        self._timeout = S.getValue('GUEST_TIMEOUT')[self._number]
        self._monitor = '%s/vm%dmonitor' % ('/tmp', self._number)
        # read GUEST NICs configuration and use only defined NR of NICS
        nics_nr = S.getValue('GUEST_NICS_NR')[self._number]
        # and inform user about missconfiguration
        if nics_nr < 1:
            raise RuntimeError('At least one VM NIC is mandotory, but {} '
                               'NICs are configured'.format(nics_nr))
        elif nics_nr > 1 and nics_nr % 2:
            nics_nr = int(nics_nr / 2) * 2
            self._logger.warning('Odd number of NICs is configured, only '
                                 '%s NICs will be used', nics_nr)

        self._nics = S.getValue('GUEST_NICS')[self._number][:nics_nr]

        # set guest loopback application based on VNF configuration
        # cli option take precedence to config file values
        self._guest_loopback = S.getValue('GUEST_LOOPBACK')[self._number]

        self._testpmd_fwd_mode = S.getValue('GUEST_TESTPMD_FWD_MODE')[self._number]
        # in case of SRIOV we must ensure, that MAC addresses are not swapped
        if S.getValue('SRIOV_ENABLED') and self._testpmd_fwd_mode.startswith('mac') and \
           not S.getValue('VNF').endswith('PciPassthrough'):

            self._logger.info("SRIOV detected, forwarding mode of testpmd was changed from '%s' to '%s'",
                              self._testpmd_fwd_mode, 'io')
            self._testpmd_fwd_mode = 'io'

        name = 'Client%d' % self._number
        vnc = ':%d' % self._number
        # don't use taskset to affinize main qemu process; It causes hangup
        # of 2nd VM in case of DPDK. It also slows down VM responsivnes.
        cpumask = ",".join(S.getValue('GUEST_CORE_BINDING')[self._number])
        #self._cmd = ['sudo', '-E', 'taskset', '-c', cpumask,
        self._cmd = ['sudo', '-E', 'taskset', '-c', cpumask,
                     S.getValue('TOOLS')['qemu-system'],
                     '-m', S.getValue('GUEST_MEMORY')[self._number],
                     '-smp', str(S.getValue('GUEST_SMP')[self._number]),       
                     '-cpu', 'host,migratable=off',
                     '-drive', 'if={},file='.format(S.getValue(
                         'GUEST_BOOT_DRIVE_TYPE')[self._number]) +
                     S.getValue('GUEST_IMAGE')[self._number],
                     '-boot', 'c', '--enable-kvm',
                     '-monitor', 'unix:%s,server,nowait' % self._monitor,
                     '-object',
                     'memory-backend-file,id=mem,size=' +
                     str(S.getValue('GUEST_MEMORY')[self._number]) + 'M,' +
                     'mem-path=' + S.getValue('HUGEPAGE_DIR') + ',share=on',
                     # due bug 1624223, delete -mem-prealloc
                     '-numa', 'node,memdev=mem -mem-prealloc',
                     '-nographic', '-vnc', str(vnc), '-name', name,
                     '-snapshot', '-net none', '-no-reboot',
                     '-M q35,kernel-irqchip=split -device intel-iommu,device-iotlb=on,intremap,caching-mode=true',
                     '-device pcie-root-port,id=root.1,slot=1 -device pcie-root-port,id=root.2,slot=2 -device pcie-root-port,id=root.3,slot=3 -device pcie-root-port,id=root.4,slot=4',
                     #'-drive',
                     #'if=%s,format=raw,file=fat:rw:%s,snapshot=off' %
                     #(S.getValue('GUEST_SHARED_DRIVE_TYPE')[self._number],
                     # S.getValue('GUEST_SHARE_DIR')[self._number]),
                    ]
        self._configure_logging()

    def _configure_logging(self):
        """
        Configure logging.
        """
        self.GuestCommandFilter.prefix = self._log_prefix

        logger = logging.getLogger()
        cmd_logger = logging.FileHandler(
            filename=os.path.join(S.getValue('LOG_DIR'),
                                  S.getValue('LOG_FILE_GUEST_CMDS')) +
            str(self._number))
        cmd_logger.setLevel(logging.DEBUG)
        cmd_logger.addFilter(self.GuestCommandFilter())
        logger.addHandler(cmd_logger)

    # startup/Shutdown

    def start(self):
        """
        Start QEMU instance, login and prepare for commands.
        """
        super(IVnfQemu, self).start()
        if S.getValue('VNF_AFFINITIZATION_ON'):
            self._affinitize()

        if S.getValue('VSWITCH_VHOST_NET_AFFINITIZATION') and S.getValue(
                'VNF') == 'QemuVirtioNet':
            self._affinitize_vhost_net()

        if self._timeout:
            self._config_guest_loopback()

    def stop(self):
        """
        Stops VNF instance gracefully first.
        """
        try:
            # exit testpmd if needed
            if self._guest_loopback == 'testpmd':
                self.execute_and_wait('stop', 120, "Done")
                self.execute_and_wait('quit', 120, "[bB]ye")

            # turn off VM
            self.execute_and_wait('poweroff', 120, "Power down")

        except pexpect.TIMEOUT:
            self.kill()

        # wait until qemu shutdowns
        self._logger.debug('Wait for QEMU to terminate')
        for dummy in range(30):
            time.sleep(1)
            if not self.is_running():
                break

        # just for case that graceful shutdown failed
        super(IVnfQemu, self).stop()

    # helper functions

    def _login(self, timeout=120):
        """
        Login to QEMU instance.

        This can be used immediately after booting the machine, provided a
        sufficiently long ``timeout`` is given.

        :param timeout: Timeout to wait for login to complete.

        :returns: None
        """
        # if no timeout was set, we likely started QEMU without waiting for it
        # to boot. This being the case, we best check that it has finished
        # first.
        if not self._timeout:
            self._expect_process(timeout=timeout)

        self._child.sendline(S.getValue('GUEST_USERNAME')[self._number])
        self._child.expect(S.getValue('GUEST_PROMPT_PASSWORD')[self._number], timeout=5)
        self._child.sendline(S.getValue('GUEST_PASSWORD')[self._number])

        self._expect_process(S.getValue('GUEST_PROMPT')[self._number], timeout=5)

    def send_and_pass(self, cmd, timeout=30):
        """
        Send ``cmd`` and wait ``timeout`` seconds for it to pass.

        :param cmd: Command to send to guest.
        :param timeout: Time to wait for prompt before checking return code.

        :returns: None
        """
        self.execute(cmd)
        self.wait(S.getValue('GUEST_PROMPT')[self._number], timeout=timeout)
        self.execute('echo $?')
        self._child.expect('^0$', timeout=1)  # expect a 0
        self.wait(S.getValue('GUEST_PROMPT')[self._number], timeout=timeout)

    def _affinitize(self):
        """
        Affinitize the SMP cores of a QEMU instance.

        This is a bit of a hack. The 'socat' utility is used to
        interact with the QEMU HMP. This is necessary due to the lack
        of QMP in older versions of QEMU, like v1.6.2. In future
        releases, this should be replaced with calls to libvirt or
        another Python-QEMU wrapper library.

        :returns: None
        """
        #thread_id = (r'.* CPU #%d: .* thread_id=(\d+)')
        thread_id = (r'.* CPU #%d: thread_id=(\d+)')

        self._logger.info('Affinitizing guest...')

        cur_locale = locale.getdefaultlocale()[1]
        proc = subprocess.Popen(
            ('echo', 'info cpus'), stdout=subprocess.PIPE)
        output = subprocess.check_output(
            ('sudo', 'socat', '-', 'UNIX-CONNECT:%s' % self._monitor),
            stdin=proc.stdout)
        proc.wait()

        for cpu in range(0, int(S.getValue('GUEST_SMP')[self._number])):
            match = None
            guest_thread_binding = S.getValue('GUEST_THREAD_BINDING')[self._number]
            if guest_thread_binding is None:
                guest_thread_binding = S.getValue('GUEST_CORE_BINDING')[self._number]
            for line in output.decode(cur_locale).split('\n'):
                match = re.search(thread_id % cpu, line)
                if match:
                    self._affinitize_pid(guest_thread_binding[cpu], match.group(1))
                    break

            if not match:
                self._logger.error('Failed to affinitize guest core #%d. Could'
                                   ' not parse tid.', cpu)

    def _affinitize_vhost_net(self):
        """
        Affinitize the vhost net threads for Vanilla OVS and guest nic queues.

        :return: None
        """
        self._logger.info('Affinitizing VHOST Net threads.')
        args1 = ['pgrep', 'vhost-']
        process1 = subprocess.Popen(args1, stdout=subprocess.PIPE,
                                    shell=False)
        out = process1.communicate()[0]
        processes = out.decode(locale.getdefaultlocale()[1]).split('\n')
        if processes[-1] == '':
            processes.pop() # pgrep may return an extra line with no data
        self._logger.info('Found %s vhost net threads...', len(processes))

        cpumap = S.getValue('VSWITCH_VHOST_CPU_MAP')
        mapcount = 0
        for proc in processes:
            self._affinitize_pid(cpumap[mapcount], proc)
            mapcount += 1
            if mapcount + 1 > len(cpumap):
                # Not enough cpus were given in the mapping to cover all the
                # threads on a 1 to 1 ratio with cpus so reset the list counter
                #  to 0.
                mapcount = 0

    def _config_guest_loopback(self):
        """
        Configure VM to run VNF, e.g. port forwarding application based on the configuration
        """
        if self._guest_loopback == 'testpmd':
            self._login()
            self._configure_testpmd()
        elif self._guest_loopback == 'l2fwd':
            self._login()
            self._configure_l2fwd()
        elif self._guest_loopback == 'linux_bridge':
            self._login()
            self._configure_linux_bridge()
        elif self._guest_loopback != 'buildin':
            self._logger.error('Unsupported guest loopback method "%s" was specified. Option'
                               ' "buildin" will be used as a fallback.', self._guest_loopback)

    def wait(self, prompt=None, timeout=30):
        if prompt is None:
            prompt = S.getValue('GUEST_PROMPT')[self._number]
        super(IVnfQemu, self).wait(prompt=prompt, timeout=timeout)

    def execute_and_wait(self, cmd, timeout=30, prompt=None):
        if prompt is None:
            prompt = S.getValue('GUEST_PROMPT')[self._number]
        super(IVnfQemu, self).execute_and_wait(cmd, timeout=timeout,
                                               prompt=prompt)

    def _modify_dpdk_makefile(self):
        """
        Modifies DPDK makefile in Guest before compilation if needed
        """
        pass

    def _configure_copy_sources(self, dirname):
        """
        Mount shared directory and copy DPDK and l2fwd sources
        """
        # mount shared directory
        self.execute_and_wait('umount /dev/sdb1')
        self.execute_and_wait('rm -rf ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number])
        self.execute_and_wait('mkdir -p ' + S.getValue('GUEST_OVS_DPDK_SHARE')[self._number])
        self.execute_and_wait('mount -o ro,iocharset=utf8 /dev/sdb1 ' +
                              S.getValue('GUEST_OVS_DPDK_SHARE')[self._number])
        self.execute_and_wait('mkdir -p ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number])
        self.execute_and_wait('cp -r ' + os.path.join(S.getValue('GUEST_OVS_DPDK_SHARE')[self._number], dirname) +
                              ' ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number])
        self.execute_and_wait('umount /dev/sdb1')

    def _configure_disable_firewall(self):
        """
        Disable firewall in VM
        """
        for iptables in ['iptables', 'ip6tables']:
            # filter table
            for chain in ['INPUT', 'FORWARD', 'OUTPUT']:
                self.execute_and_wait("{} -t filter -P {} ACCEPT".format(iptables, chain))
            # mangle table
            for chain in ['PREROUTING', 'INPUT', 'FORWARD', 'OUTPUT', 'POSTROUTING']:
                self.execute_and_wait("{} -t mangle -P {} ACCEPT".format(iptables, chain))
            # nat table
            for chain in ['PREROUTING', 'INPUT', 'OUTPUT', 'POSTROUTING']:
                self.execute_and_wait("{} -t nat -P {} ACCEPT".format(iptables, chain))

            # flush rules and delete chains created by user
            for table in ['filter', 'mangle', 'nat']:
                self.execute_and_wait("{} -t {} -F".format(iptables, table))
                self.execute_and_wait("{} -t {} -X".format(iptables, table))


    def _configure_testpmd(self):
        """
        Configure VM to perform L2 forwarding between NICs by DPDK's testpmd
        """
        #self._configure_copy_sources('DPDK')
        #self.execute_and_wait('systemctl stop irqbalance')
        #self.execute_and_wait('. /root/ovs_dpdk/DPDK/affinity.sh')
        self._configure_disable_firewall()

        # Guest images _should_ have 1024 hugepages by default,
        # but just in case:'''
        self.execute_and_wait('sysctl vm.nr_hugepages={}'.format(S.getValue('GUEST_HUGEPAGES_NR')[self._number]))

        # Mount hugepages
        self.execute_and_wait('mkdir -p /dev/hugepages')
        self.execute_and_wait(
            'mount -t hugetlbfs hugetlbfs /dev/hugepages')

        # build and configure system for dpdk
        '''
        self.execute_and_wait('cd ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number] +
                              '/DPDK')
        self.execute_and_wait('export CC=gcc')
        self.execute_and_wait('export RTE_SDK=' +
                              S.getValue('GUEST_OVS_DPDK_DIR')[self._number] + '/DPDK')
        self.execute_and_wait('export RTE_TARGET=%s' % S.getValue('RTE_TARGET'))

        # modify makefile if needed
        self._modify_dpdk_makefile()
        '''
        #self.execute_and_wait('tuned-adm profile cpu-partitioning')
        #self.execute_and_wait('cat /var/log/tuned/tuned.log')
        self.execute_and_wait('cat /proc/meminfo')
        self.execute_and_wait('rpm -ivh /root/dpdkrpms/1711-14/dpdk*.rpm ')
        #self.execute_and_wait('tuna -Q')
        self.execute_and_wait('cat /proc/cmdline')
        #self.execute_and_wait('systemctl status tuned')
        #self.execute_and_wait('systemctl is-enabled tuned;echo $?')
        #self.execute_and_wait('tuned-adm profile cpu-partitioning')
        #self.execute_and_wait('tuned-adm active')
        #self.execute_and_wait('./tools/dpdk*bind.py --status')

        # disable network interfaces, so DPDK can take care of them
        for nic in self._nics:
            self.execute_and_wait('ifdown ' + nic['device'])

        # build and insert igb_uio and rebind interfaces to it
        '''
        self.execute_and_wait('make RTE_OUTPUT=$RTE_SDK/$RTE_TARGET -C '
                              '$RTE_SDK/lib/librte_eal/linuxapp/igb_uio')
        self.execute_and_wait('modprobe uio')
        self.execute_and_wait('insmod %s/kmod/igb_uio.ko' %
                              S.getValue('RTE_TARGET'))
        self.execute_and_wait('./tools/dpdk*bind.py --status')
        pci_list = ' '.join([nic['pci'] for nic in self._nics])
        self.execute_and_wait('./tools/dpdk*bind.py -u ' + pci_list)
        self.execute_and_wait('./tools/dpdk*bind.py -b igb_uio ' + pci_list)
        self.execute_and_wait('./tools/dpdk*bind.py --status')
        '''
        self.execute_and_wait('/usr/bin/dpdk-devbind.py --status')
        pci_list = ' '.join([nic['pci'] for nic in self._nics])
        self.execute_and_wait('/usr/bin/dpdk-devbind.py -u ' + pci_list)
        self._bind_dpdk_driver(S.getValue(
            'GUEST_DPDK_BIND_DRIVER')[self._number], pci_list)
        self.execute_and_wait('/usr/bin/dpdk-devbind.py --status')

        # build and run 'test-pmd'
        '''
        self.execute_and_wait('cd ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number] +
                              '/DPDK/app/test-pmd')
        self.execute_and_wait('make clean')
        self.execute_and_wait('make')
        '''
        list_string = ""
        for nic in pci_list.split():
            list_string += "-w {} ".format(nic)
        # get testpmd settings from CLI
        testpmd_params = S.getValue('GUEST_TESTPMD_PARAMS')[self._number]
        if S.getValue('VSWITCH_JUMBO_FRAMES_ENABLED'):
            testpmd_params += ' --max-pkt-len={}'.format(S.getValue(
                'VSWITCH_JUMBO_FRAMES_SIZE'))
        self.execute_and_wait('cd /usr/bin')
        self.execute_and_wait('./dpdk-testpmd {}'.format(testpmd_params), 60, "Done")
        self.execute('set fwd ' + self._testpmd_fwd_mode, 1)
        self.execute_and_wait('start', 20, 'testpmd>')

    def _configure_l2fwd(self):
        """
        Configure VM to perform L2 forwarding between NICs by l2fwd module
        """
        if int(S.getValue('GUEST_NIC_QUEUES')[self._number]):
            self._set_multi_queue_nic()
        self._configure_copy_sources('l2fwd')
        self._configure_disable_firewall()

        # configure all interfaces
        for nic in self._nics:
            self.execute('ip addr add ' +
                         nic['ip'] + ' dev ' + nic['device'])
            if S.getValue('VSWITCH_JUMBO_FRAMES_ENABLED'):
                self.execute('ifconfig {} mtu {}'.format(
                    nic['device'], S.getValue('VSWITCH_JUMBO_FRAMES_SIZE')))
            self.execute('ip link set dev ' + nic['device'] + ' up')

        # build and configure system for l2fwd
        self.execute_and_wait('cd ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number] +
                              '/l2fwd')
        self.execute_and_wait('export CC=gcc')

        self.execute_and_wait('make')
        if len(self._nics) == 2:
            self.execute_and_wait('insmod ' + S.getValue('GUEST_OVS_DPDK_DIR')[self._number] +
                                  '/l2fwd' + '/l2fwd.ko net1=' + self._nics[0]['device'] +
                                  ' net2=' + self._nics[1]['device'])
        else:
            raise RuntimeError('l2fwd can forward only between 2 NICs, but {} NICs are '
                               'configured inside GUEST'.format(len(self._nics)))

    def _configure_linux_bridge(self):
        """
        Configure VM to perform L2 forwarding between NICs by linux bridge
        """
        if int(S.getValue('GUEST_NIC_QUEUES')[self._number]):
            self._set_multi_queue_nic()
        self._configure_disable_firewall()

        # configure linux bridge
        #self.execute('brctl addbr br0')

        # add all NICs into the bridge
        for nic in self._nics:
            self.execute('ip addr add ' +
                         nic['ip'] + ' dev ' + nic['device'])
            if S.getValue('VSWITCH_JUMBO_FRAMES_ENABLED'):
                self.execute('ifconfig {} mtu {}'.format(
                    nic['device'], S.getValue('VSWITCH_JUMBO_FRAMES_SIZE')))
            self.execute('ip link set dev ' + nic['device'] + ' up')
            #self.execute('brctl addif br0 ' + nic['device'])

        #self.execute('ip addr add 192.168.1.2/24 enp0s6')
        #self.execute('ip addr add 192.168.1.3/24 enp0s7')
        self.execute('ip link add br0 type bridge')
        self.execute('ip link set dev enp0s6 master br0')
        self.execute('ip link set dev enp0s7 master br0')
        self.execute('ip addr add ' +
                     S.getValue('GUEST_BRIDGE_IP')[self._number] +
                     ' dev br0')
        self.execute('ip link set dev br0 up')

        # Add the arp entries for the IXIA ports and the bridge you are using.
        # Use command line values if provided.
        trafficgen_mac = get_test_param('vanilla_tgen_port1_mac',
                                        S.getValue('VANILLA_TGEN_PORT1_MAC'))
        trafficgen_ip = get_test_param('vanilla_tgen_port1_ip',
                                       S.getValue('VANILLA_TGEN_PORT1_IP'))

        self.execute('arp -s ' + trafficgen_ip + ' ' + trafficgen_mac)

        trafficgen_mac = get_test_param('vanilla_tgen_port2_mac',
                                        S.getValue('VANILLA_TGEN_PORT2_MAC'))
        trafficgen_ip = get_test_param('vanilla_tgen_port2_ip',
                                       S.getValue('VANILLA_TGEN_PORT2_IP'))

        self.execute('arp -s ' + trafficgen_ip + ' ' + trafficgen_mac)

        # Enable forwarding
        self.execute('sysctl -w net.ipv4.ip_forward=1')
        self.execute('yum install -y tuna')
        self.execute_and_wait('tuned-adm profile network-latency')
        self.execute('tuna -Q')

        # Controls source route verification
        # 0 means no source validation
        self.execute('sysctl -w net.ipv4.conf.all.rp_filter=0')
        for nic in self._nics:
            self.execute('sysctl -w net.ipv4.conf.' + nic['device'] + '.rp_filter=0')
    
    def _bind_dpdk_driver(self, driver, pci_slots):
        """
        Bind the virtual nics to the driver specific in the conf file
        :return: None
        """
        if driver == 'uio_pci_generic':
            if S.getValue('VNF') == 'QemuPciPassthrough':
                # unsupported config, bind to igb_uio instead and exit the
                # outer function after completion.
                self._logger.error('SR-IOV does not support uio_pci_generic. '
                                   'Igb_uio will be used instead.')
                self._bind_dpdk_driver('igb_uio_from_src', pci_slots)
                return
            self.execute_and_wait('modprobe uio_pci_generic')
            self.execute_and_wait('/usr/bin/dpdk-devbind.py -b uio_pci_generic '+
                                  pci_slots)
        elif driver == 'vfio_no_iommu':
            #self.execute_and_wait('modprobe -r vfio')
            #self.execute_and_wait('modprobe -r vfio_iommu_type1')
            #self.execute_and_wait('modprobe vfio enable_unsafe_noiommu_mode=Y')
            self.execute_and_wait('modprobe vfio')
            self.execute_and_wait('modprobe vfio-pci')
            self.execute_and_wait('/usr/bin/dpdk-devbind.py -b vfio-pci ' +
                                  pci_slots)
        elif driver == 'igb_uio_from_src':
            # build and insert igb_uio and rebind interfaces to it
            self.execute_and_wait('make RTE_OUTPUT=$RTE_SDK/$RTE_TARGET -C '
                                  '$RTE_SDK/lib/librte_eal/linuxapp/igb_uio')
            self.execute_and_wait('modprobe uio')
            self.execute_and_wait('insmod %s/kmod/igb_uio.ko' %
                                  S.getValue('RTE_TARGET'))
            self.execute_and_wait('/usr/bin/dpdk-devbind.py -b igb_uio ' + pci_slots)
        else:
            self._logger.error(
                'Unknown driver for binding specified, defaulting to igb_uio')
            self._bind_dpdk_driver('igb_uio_from_src', pci_slots)

    def _set_multi_queue_nic(self):
        """
        Enable multi-queue in guest kernel with ethool.
        :return: None
        """
        for nic in self._nics:
            self.execute_and_wait('ethtool -L {} combined {}'.format(
                nic['device'], S.getValue('GUEST_NIC_QUEUES')[self._number]))
            self.execute_and_wait('ethtool -l {}'.format(nic['device']))
