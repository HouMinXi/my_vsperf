#!/usr/bin/python
import os
from subprocess import Popen, PIPE
import cpu_layout
import config

def run_shell(cmd):
    return Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]

def ver_setup_data():

    #generate RPMS_Used list
    rpm_info_dict = {}
    RPMS_Used = []
    rpm_info_dict["RPMS Used"] = RPMS_Used

    ovs_version_cmd = "rpm -qa|grep openvswitch"
    ovs_version = run_shell(ovs_version_cmd)
    dpdk_version_cmd = "rpm -qa|grep dpdk-[0-9]"
    dpdk_version = run_shell(dpdk_version_cmd)
    dpdk_tools_version_cmd = "rpm -qa|grep dpdk-tools"
    dpdk_tools_version = run_shell(dpdk_tools_version_cmd)
    RPMS_Used.append(ovs_version.strip())
    RPMS_Used.append(dpdk_version.strip())
    RPMS_Used.append(dpdk_tools_version.strip())

    for i in os.popen('rpm -qa|grep qemu').read(). splitlines():
        RPMS_Used.append(i)
    for j in os.popen('rpm -qa|grep tuned').read(). splitlines():
    	RPMS_Used.append(j)

    kernel_version = "* OS:" + str(os.popen('uname -r').read().strip())

    #generate Host_Info list
    Host_Info = []
    host_info_dict = {}
    host_info_dict["Host Info"]=Host_Info
    Host_Info.append(kernel_version)

    redhat_version_cmd = "cat /etc/redhat-release"
    redhat_version = "* Kernel Version: " + str(os.popen(redhat_version_cmd).read().strip())
    Host_Info.append(redhat_version)

    Host_Info.append("* NIC(s):")

    try:
        nic1_pciinfo_cmd = "ethtool -i " + config.NIC1 + " |grep bus-info|awk -F ' ' '{printf $2}'"
        raw_data = run_shell(nic1_pciinfo_cmd) 
        NIC1_PCI_ADDR = str(raw_data.splitlines()[0])
        NIC1_PCI_ADDR = NIC1_PCI_ADDR[5:]
        nic1_info_cmd='lspci |grep ' + NIC1_PCI_ADDR
        nic1_info = run_shell(nic1_info_cmd) 
        nic1_info = "* " + nic1_info[8:]
        Host_Info.append(str(nic1_info).strip())
    except Exception, e:
        Host_Info.append('')

    try:
        nic2_pciinfo_cmd = "ethtool -i " + config.NIC2 + " |grep bus-info|awk -F ' ' '{printf $2}'"
        raw_data = run_shell(nic2_pciinfo_cmd) 
        NIC2_PCI_ADDR = str(raw_data.splitlines()[0])
        NIC2_PCI_ADDR = NIC2_PCI_ADDR[5:]
        nic2_info_cmd ='lspci |grep ' + NIC2_PCI_ADDR
        nic2_info = run_shell(nic2_info_cmd) 
        nic2_info = "* " + nic2_info[8:]
        Host_Info.append(str(nic2_info).strip())
    except Exception, e:
        Host_Info.append('')

    board_vendor_cmd = "cat /sys/class/dmi/id/board_vendor"
    board_vendor = run_shell(board_vendor_cmd)
    board_vendor = "* Board: " + str(board_vendor).strip()

    board_name_cmd = "cat /sys/class/dmi/id/board_name"
    board_name = run_shell(board_name_cmd)
    board_name = str(board_name).strip()

    socket_info = []
    num_nodes = len([name for name in os.listdir(
    	'/sys/devices/system/node/') if name.startswith('node')])
    socket_info.append(''.join(['[', str(num_nodes), ' sockets]']))
    socket_info = str(socket_info).strip()

    board_info = [ board_vendor, board_name, socket_info ]
    board_info = ' '.join(board_info)
    Host_Info.append(board_info)

    cpu_info_cmd = "cat /proc/cpuinfo|grep 'model name'| uniq -c | awk -F ':' '{printf $2}'"
    cpu_info = run_shell(cpu_info_cmd).strip()
    Host_Info.append("* CPU: " + cpu_info)

    cpu_core_num_cmd = "cat /proc/cpuinfo|grep process|wc -l"
    cpu_core_num = run_shell(cpu_core_num_cmd)
    Host_Info.append("* CPU cores: " + str(cpu_core_num).strip())

    mem_info_cmd = "cat /proc/meminfo|grep MemTotal| awk -F ':' '{printf $2}'"
    mem_info = run_shell(mem_info_cmd)
    Host_Info.append("* Memory: " + str(mem_info).strip())

    #generate Guest_Info list
    guest_info_dict = {}
    Guest_Info = []
    guest_info_dict['Guest_Info'] = Guest_Info
    Guest_Info.append("Guest Info")
    Guest_Info.append("* Kernel Version: 3.10.0-691.el7.x86_64")

    return [rpm_info_dict, host_info_dict, guest_info_dict] 

def core_data():
    return cpu_layout.get_core() 
