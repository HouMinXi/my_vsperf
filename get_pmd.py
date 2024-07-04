import sys, getopt
from subprocess import Popen, PIPE
import os

def usages():
    print """
usage 1: caculate hex mask
python get_pmd.py --cmd host_pmd --nic enp1s0f0 --pmd 8  

usage 2:
python get_pmd.py --cmd guest_pmd --nic enp1s0f0 --cpu 9

usage 3:
python get_pmd.py --cmd dpdk_args --nic enp1s0f0

usage 4:
python get_pmd.py --cmd spec_dpdk_args --nic enp1s0f0

usage 5:
python get_pmd.py --cmd last_cpu --nic enp1s0f0 --cpu 4

usage 5:
python get_pmd.py --cmd dpdk_config --nic enp1s0f0

usage6:
get other numanode cpu
python2 get_pmd.py --cmd qemu_emulator -nic enp1s0f0 
    """

cmd=None
pmd_num=None
cpu_num=None
nic=None

opts, args = getopt.getopt(sys.argv[1:], 'm:p:n:c:', ['cmd=', 'pmd=', 'nic=', 'cpu='])
if len(opts) == 0:
    print "Please input correct params!"
    usages()
    sys.exit()


for op, value in opts:
    if op in ('-m', '--cmd'):
        cmd = value
    elif op in ('-p', '--pmd'):
        pmd_num = value
    elif op in ('-n', '--nic'):
        nic = value
    elif op in ('-c', '--cpu'):
        cpu_num = value

SOCKET = 2


def run_shell(cmd):
    return Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]

# read cpu info from /proc/cpuinfo, core_map structure like {(physical id,core id): [processor1, processor2].....}
"""
# python3 /usr/share/dpdk/usertools/cpu_layout.py
======================================================================
Core and Socket Information (as reported by '/sys/devices/system/cpu')
======================================================================

cores =  [16, 2, 9, 4, 3, 20, 11, 17, 19, 18, 24, 27]
sockets =  [0, 1]

        Socket 0        Socket 1       
        --------        --------       
Core 16 [0, 16]         [11, 27]       
Core 2  [4, 20]         [1, 17]        
Core 9  [2, 18]         [9, 25]        
Core 4                  [3, 19]        
Core 3                  [5, 21]        
Core 20 [6, 22]                        
Core 11                 [7, 23]        
Core 17 [8, 24]                        
Core 19 [10, 26]                       
Core 18 [12, 28]                       
Core 24                 [13, 29]       
Core 27 [14, 30]        [15, 31] 

# python3 /usr/share/dpdk/usertools/cpu_layout.py
======================================================================
Core and Socket Information (as reported by '/sys/devices/system/cpu')
======================================================================

cores =  [0, 5, 1, 4, 2, 3, 8, 13, 9, 12, 10, 11]
sockets =  [0, 1]

        Socket 0        Socket 1       
        --------        --------       
Core 0  [0, 24]         [1, 25]        
Core 5  [2, 26]         [3, 27]        
Core 1  [4, 28]         [5, 29]        
Core 4  [6, 30]         [7, 31]        
Core 2  [8, 32]         [9, 33]        
Core 3  [10, 34]        [11, 35]       
Core 8  [12, 36]        [13, 37]       
Core 13 [14, 38]        [15, 39]       
Core 9  [16, 40]        [17, 41]       
Core 12 [18, 42]        [19, 43]       
Core 10 [20, 44]        [21, 45]       
Core 11 [22, 46]        [23, 47] 
"""


def get_core_map(numa_id):
    sockets = []
    cores = []
    core_map = {}

    fd=open("/proc/cpuinfo")
    lines = fd.readlines()
    fd.close()

    core_details = []
    core_lines = {}
    for line in lines:
        # Delete space line
        if len(line.strip()) != 0:
            name, value = line.split(":", 1)
            # get all information from /proc/cpuinfo and set a ket/value
            core_lines[name.strip()] = value.strip()
        else:
            core_details.append(core_lines)
            core_lines = {}

    for core in core_details:
        # physical id == socket, core id == core, processor == processor
        for field in ["processor", "core id", "physical id"]:
            if field not in core:
                print "Error getting '%s' value from /proc/cpuinfo" % field
                sys.exit(1)
            core[field] = int(core[field])
        if core["physical id"] == numa_id:
            if core["core id"] not in cores:
                cores.append(core["core id"])
            if core["physical id"] not in sockets:
                sockets.append(core["physical id"])
            key = (core["physical id"], core["core id"])
            if key not in core_map:
                core_map[key] = []
            # (Socket num, core num): [processor1, processor2]
            core_map[key].append(core["processor"])

    return core_map, cores

def get_cores(data):
    sort_core = [] 
    for k in data.keys():
        sort_core.append(k[1])
    sort_core = list(set(sort_core))
    sort_core.reverse()
    # Sort core num in descending order
    return sort_core

def pmdMask(core_map, pmd_num, socket):
    rlt = []
    c = get_cores(core_map)
    if len(core_map[(0, 0)]) == 1:
        tmp = int(pmd_num)
    elif len(core_map[(0, 0)]) == 2:
        tmp = int(pmd_num) / 2
    else:
        print "ERROR, can't got cpu number"
    for i in c:
        rlt.extend(list(core_map[(int(socket), i)]))
        tmp = tmp - 1
        if tmp <= 0:
            break
    return rlt 

def host_pmd():
    socket = numa(nic)
    data, _ = get_core_map(socket)
    r = 0
    for i in pmdMask(data, pmd_num, socket):
        r += 2 ** i
    rlt = str(hex(r))
    if rlt[-1] == 'L':
        rlt = rlt[:-1]
    return rlt

def numa(nic):
    if nic is None:
        return None
    else:
        numa_file = "/tmp/numa"
        if os.path.exists(numa_file):
            return int(run_shell("cat %s" % numa_file))
        else:
            node = int(run_shell("cat /sys/class/net/%s/device/numa_node" % nic))
            with open(numa_file, 'wt') as f:
                f.write(str(node))
            return node 

def guest_pmd():
    rlt = []
    global nic, cpu_num
    var_numa = numa(nic)
    data, cores = get_core_map(var_numa)
    # usually socket0 and socket 1 the first procress use to housekeeping
    # python3 /usr/share/dpdk/usertools/cpu_layout.py
#     == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#     Core and Socket
#     Information(as reported
#     by
#     '/sys/devices/system/cpu')
#     == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
#     cores = [0, 5, 1, 4, 2, 3, 8, 13, 9, 12, 10, 11]
#     sockets = [0, 1]
#
#     Socket 0          Socket1
#     --------        --------
# Core  0[0, 24]        [1, 25]

    for i in range(len(cores)):
        if i == 0:
            continue
            # consider disable hyper thread. don't use cpu0 and sibling cores
            # rlt.append(str(data[(var_numa, cores[i])][1]))
        # elif i == 1:
        #     rlt.append(str(data[(var_numa, cores[i])][0]))
        else:
            for tmp in data[(var_numa, cores[i])]:
                rlt.append(str(tmp))
            if len(rlt) >= int(cpu_num):
                break
    return [tuple(rlt)]


def dpdk_config():
    rlt = {'dpdk-init' : 'true','dpdk-lcore-mask' : '',}
    global nic
    var_numa = numa(nic)
    data, cores = get_core_map(var_numa)
    hex_mask = data[(var_numa, cores[0])][0]
    rlt['dpdk-lcore-mask'] = str(hex(2 ** hex_mask))
    return rlt

def dpdk_args():
    rlt = ['-c', '', '-n', '4', '--socket-mem 4096,4096']
    global nic
    var_numa = numa(nic)
    data, cores = get_core_map(var_numa)
    hex_mask = data[(var_numa, cores[0])][0]
    rlt[1] = str(hex(2 ** hex_mask))
    return rlt

def spec_dpdk_args():
    rlt = ['-l', '', '-n', '4', '--socket-mem 4096,4096']
    global nic
    var_numa = numa(nic)
    data, cores = get_core_map(var_numa)
    length = len(cores)
    tmp = []
    for i in range(length - 3, length):
        tmp.append(str(data[(var_numa, cores[i])][0]))
    rlt[1] = ','.join(tmp)
    return rlt

def last_cpu():
    global nic, cpu_num
    socket = numa(nic)
    data, _ = get_core_map(socket)
    return pmdMask(data, cpu_num, socket)

def qemu_emulator():
    nic_numanode = numa(nic)
    global cpu_num
    try:
        # only support x86 server
        numactl_info = run_shell("numactl --hardware")
        numanode_info = numactl_info.split('available:')[1].split('nodes')[1].split('node')[0].split('(')[1].split(')')[0]
        max_numa = int(numanode_info[-1:])
        min_numa = int(numanode_info[:1])
        numa_list = range(min_numa, max_numa + 1)
        if nic_numanode == max_numa:
            qemu_emulator = "0"
            return qemu_emulator
        elif nic_numanode in numa_list:
            # 0 in [0,1]
            emulator_node = numa_list[numa_list.index(nic_numanode) + 1]
            cmd_line = """numactl --hardware | grep "node %s cpus:" | awk -F "node %s cpus:" '{print $NF}' """ % (emulator_node,emulator_node)
            emulator_cpu_string = run_shell(cmd_line)
            emulator_cpu_list = tuple(emulator_cpu_string.strip().split(' ')[3:3+int(cpu_num)])
            qemu_emulator = []
            qemu_emulator.append(emulator_cpu_list)
            return qemu_emulator
        else:
            # don't use emulator to start qemu
            pass
    except Exception as e:
        print e
        raise


if cmd == 'host_pmd':
    print host_pmd()
elif cmd == 'guest_pmd':
    print guest_pmd()
elif cmd == 'dpdk_args':
    print dpdk_args()
elif cmd == 'spec_dpdk_args':
    print spec_dpdk_args()
elif cmd == 'last_cpu':
    print last_cpu()
elif cmd == 'dpdk_config':
    print dpdk_config()
elif cmd == 'qemu_emulator':
    print qemu_emulator()
