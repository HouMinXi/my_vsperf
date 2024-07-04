import sys

sockets = []
cores = []
core_map = {}

fd=open("/proc/cpuinfo")
lines = fd.readlines()
fd.close()

core_details = []
core_lines = {}
for line in lines:
    if len(line.strip()) != 0:
    	name, value = line.split(":", 1)
    	core_lines[name.strip()] = value.strip()
    else:
    	core_details.append(core_lines)
    	core_lines = {}

for core in core_details:
    for field in ["processor", "core id", "physical id"]:
        if field not in core:
    	    print "Error getting '%s' value from /proc/cpuinfo" % fieldf
    	    sys.exit(1)
    	core[field] = int(core[field])

    if core["core id"] not in cores:
    	cores.append(core["core id"])
    if core["physical id"] not in sockets:
    	sockets.append(core["physical id"])
    key = (core["physical id"], core["core id"])
    if key not in core_map:
        core_map[key] = []
    core_map[key].append(core["processor"])

def cpu_socket(core_num):
    rlt = []
    rlt.append("Core " + str(core_num))
    if len(sockets) == 2:
        rlt.append(str(core_map.get((0, core_num))))
        rlt.append(str(core_map.get((1, core_num))))
    else:
        rlt.append(str(core_map.get((0, core_num))))
    return rlt

core_info = []
def get_core():

    core_info.append(['cores = ' + str(cores), '',''])
    core_info.append(['sockets = ' + str(sockets),'',''])
    
    if len(sockets) == 1:
            core_info.append(['','Socket 0', ''])
            core_info.append(['', '------'])
    if len(sockets) == 2:
            core_info.append(['', 'Socket 0', 'Socket 1'])
            core_info.append(['', '------', '------'])	
    for i in cores:
            core_info.append(cpu_socket(i))
    return core_info
