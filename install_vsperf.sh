#!/bin/bash

# added debug flag to t-shoot
set -x
echo "Starting $0"

. /mnt/tests/kernel/networking/common/include.sh || exit 1
CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/common.sh

# Detect OS name and version from systemd based os-release file
. /etc/os-release
set -x

# Get OS name (the First word from $NAME in /etc/os-release)
OS_NAME="$VERSION_ID"

clone_and_checkout_vsperf() {
echo "start to clone vsperf project..."
ping -c 2 -w 2 gerrit.opnfv.org
nslookup gerrit.opnfv.org
cat /etc/resolv.conf
pushd /root/
export https_proxy=http://squid.apac.redhat.com:3128
yum install -y vim
git clone https://gerrit.opnfv.org/gerrit/vswitchperf
cd vswitchperf
git checkout $VSPERF_COMMIT
if (($(bc <<< "$VERSION_ID >= 8"))); then
	pushd systems
	for i in $(grep -R python-six * | awk -F ":" '{print $1}'); do
		sed -i 's/python-six/python3-six/g' $i
	done
	popd
fi	
popd
cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
cp -f ${CASE_PATH}/beaker_ci_conf/tasks.py /root/vswitchperf/tools/tasks.py
cp -f ${CASE_PATH}/beaker_ci_conf/testpmd_proc.py /root/vswitchperf/src/dpdk/testpmd_proc.py
# use for trex2.41
#sed -i 's/src\/trex\/trex\/scripts\/automation\/trex_control_plane\/stl/src\/trex\/trex\/automation\/trex_control_plane\/stl/g' /root/vswitchperf/conf/03_traffic.conf
# use for trex2.41+
sed -i 's/src\/trex\/trex\/scripts\/automation\/trex_control_plane\/stl/src\/trex\/trex\/automation\/trex_control_plane\/interactive/g' /root/vswitchperf/conf/03_traffic.conf
#For 100g xena, xena should configure EnableFec as false
if [ ${XENA_SPEED} != 10 ];then
sed -i '/EnableFec/c\        "EnableFec": "false",' /root/vswitchperf/tools/pkt_gen/xena/profiles/baseconfig.x2544
fi
}

change_to_7_4() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 7.4

}

change_to_7_5() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 7.5

}

change_to_7_6() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 7.6

}


change_to_8_0() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 8.0

}

change_to_7_7() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 7.7

}

change_to_7_8() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 7.8

}

change_to_7_9() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 7.9

}

change_to_8_1() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 8.1

}

change_to_8_2() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 8.2

}

change_to_8_3() {

cd ~/vswitchperf/systems/rhel
cp -r 7.3 8.3

}

build_vsperf_without_upstream_builds() {
set -x
cd ~/vswitchperf
sed -i s/'    make || die "Make failed"'/'#     make || die "Make failed"'/ systems/build_base_machine.sh
cd systems
echo "VERSION_ID is: $VERSION_ID"
echo "OS_NAME is: $OS_NAME"
echo "Updating rhel/$OS_NAME/build_base_machine.sh to reflect rh-python36..."
sed -i 's/rh-python34/rh-python36/g' rhel/$OS_NAME/build_base_machine.sh
echo "Updating rhel/$OS_NAME/prepare_python_env.sh to reflect rh-python36..."
sed -i 's/rh-python34/rh-python36/g' rhel/$OS_NAME/prepare_python_env.sh
./build_base_machine.sh >> ${CASE_PATH}/buildvsperf.log
}

make_trex(){
pushd /root/vswitchperf/src/trex/
#make
#if [ $? -ne 0 ]; then
wget http://netqe-bj.usersys.redhat.com/share/mhou/v2.86.tar.gz
tar -zxvf v2.86.tar.gz
mv v2.86 trex
#else
#  sleep 1
#fi
popd
}

download_vnf_image() {

echo "start to down load vnf image..."
# down load the rhel image for guest
if [ "$QCOW_LOC" == "China" ]
    then
    SERVER="netqe-bj.usersys.redhat.com/share/tli/vsperf_img"
elif [ "$QCOW_LOC" == "Westford" ]
    then
    SERVER="netqe-infra01.knqe.eng.rdu2.dc.redhat.com/vm"
elif [ "$QCOW_LOC" == "Westford_rt" ]
    then
    SERVER="netqe-infra01.knqe.eng.rdu2.dc.redhat.com/vm/rt_vm"
elif [ "$QCOW_LOC" == "Chine_rt" ]; then
    SERVER="netqe-bj.usersys.redhat.com/share/mhou/image"
fi

if [ "${RT_TEST}" == "NO" ];then

  if [ "${GUEST_IMG}" == "7.2" ];then
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf.qcow2 > /dev/null 2>&1
  elif [ "${GUEST_IMG}" == "7.3" ];then
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-1Q.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-2Q.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-4Q.qcow2 > /dev/null 2>&1
  else
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-1Q-noviommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-2Q-noviommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-4Q-noviommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-1Q-viommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-2Q-viommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-4Q-viommu.qcow2 > /dev/null 2>&1
  fi

else

  if [ "${GUEST_IMG}" == "7.2" ];then
    wget -P ~/vswitchperf/ http://$SERVER/rt-image/rhel${GUEST_IMG}-vsperf.qcow2 > /dev/null 2>&1
  elif [ "${GUEST_IMG}" == "7.3" ];then
    wget -P ~/vswitchperf/ http://$SERVER/rt-image/rhel${GUEST_IMG}-vsperf-1Q.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rt-image/rhel${GUEST_IMG}-vsperf-2Q.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rt-image/rhel${GUEST_IMG}-vsperf-4Q.qcow2 > /dev/null 2>&1
  else
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-1Q-noviommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-2Q-noviommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-4Q-noviommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-1Q-viommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-2Q-viommu.qcow2 > /dev/null 2>&1
    wget -P ~/vswitchperf/ http://$SERVER/rhel${GUEST_IMG}-vsperf-4Q-viommu.qcow2 > /dev/null 2>&1
  fi
fi

#change guest port name to eth0 and eth1 for rhel8
if (($(bc <<< "$VERSION_ID >= 8")));then
    chmod 777 /root/
    local udev_file_viommu=60-persistent-net.rules
    pushd /root/
    touch $udev_file_viommu
    cat > $udev_file_viommu <<EOF
ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:02:00.0", NAME:="eth0"
ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:03:00.0", NAME:="eth1"
EOF
  if [ $VERSION_ID == '8.2' ]; then
    LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-1Q-viommu.qcow2 /root/$udev_file_viommu /etc/udev/rules.d/
    LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-2Q-viommu.qcow2 /root/$udev_file_viommu /etc/udev/rules.d/
    LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-4Q-viommu.qcow2 /root/$udev_file_viommu /etc/udev/rules.d/
  else
    virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-1Q-viommu.qcow2 /root/$udev_file_viommu /etc/udev/rules.d/
    virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-2Q-viommu.qcow2 /root/$udev_file_viommu /etc/udev/rules.d/
    virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-4Q-viommu.qcow2 /root/$udev_file_viommu /etc/udev/rules.d/
  fi
    local udev_file_noviommu=60-persistent-net.rules
    touch $udev_file_noviommu
    cat > $udev_file_noviommu <<EOF
ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:00:03.0", NAME:="eth0"
ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:00:04.0", NAME:="eth1"
EOF
  if [ $VERSION_ID == '8.2' ]; then
    LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-1Q-noviommu.qcow2 /root/$udev_file_noviommu /etc/udev/rules.d/
    LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-2Q-noviommu.qcow2 /root/$udev_file_noviommu /etc/udev/rules.d/
    LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-4Q-noviommu.qcow2 /root/$udev_file_noviommu /etc/udev/rules.d/
  else
    virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-1Q-noviommu.qcow2 /root/$udev_file_noviommu /etc/udev/rules.d/
    virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-2Q-noviommu.qcow2 /root/$udev_file_noviommu /etc/udev/rules.d/
    virt-copy-in -a /root/vswitchperf/rhel${GUEST_IMG}-vsperf-4Q-noviommu.qcow2 /root/$udev_file_noviommu /etc/udev/rules.d/
    popd
  fi
fi
}


download_Xena2544() {
    echo "start to download xena2544.exe to xena folder..."
    #download xena2544.exe to the test machine
    #wget -P /root/vswitchperf/tools/pkt_gen/xena/ http://netqe-infra01.knqe.eng.rdu2.dc.redhat.com/Xena2544.exe > /dev/null 2>&1
	if [ "$QCOW_LOC" == "Westford" ]
	then
		wget -P /root/vswitchperf/tools/pkt_gen/xena/ http://netqe-infra01.knqe.eng.rdu2.dc.redhat.com/Xena2544.exe > /dev/null 2>&1
		\cp ${CASE_PATH}/beaker_ci_conf/baseconfig.x2544 /root/vswitchperf/tools/pkt_gen/xena/profiles/baseconfig.x2544
	else
		if [ ${NetScout_speed} == "100" ] && [ ${TRAFFIC_GEN} == "xena" ]	
		then
			wget -P /root/vswitchperf/tools/pkt_gen/xena/ http://netqe-bj.usersys.redhat.com/share/tli/xena/Valkyrie2544.exe > /dev/null 2>&1
			mv /root/vswitchperf/tools/pkt_gen/xena/Valkyrie2544.exe /root/vswitchperf/tools/pkt_gen/xena/Xena2544.exe
			\cp ${CASE_PATH}/beaker_ci_conf/baseconfig.x2544 /root/vswitchperf/tools/pkt_gen/xena/profiles/baseconfig.x2544
		else
			wget -P /root/vswitchperf/tools/pkt_gen/xena/ http://netqe-bj.usersys.redhat.com/share/tli/xena/Xena2544.exe > /dev/null 2>&1
		fi
	fi
}

:<<!
install_mono_rpm() {
        #install mono rpm
        echo "start to install mono rpm..."
        yum install yum-utils -y
        rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"
        yum-config-manager --add-repo http://download.mono-project.com/repo/centos/
        yum -y install mono-complete
        yum-config-manager --disable download.mono-project.com_repo_centos_
        yum-config-manager --enable download.mono-project.com_repo_centos_
        rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"
        yum-config-manager --add-repo http://download.mono-project.com/repo/centos/
        yum -y install mono-complete
        echo "check mono install"
        rpm -qa|grep mono
}

install_mono_rpm() {
    #install mono rpm
    echo "start to install mono rpm..."
    rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF" >> ${CASE_PATH}/mono_install.log
    yum-config-manager --add-repo http://download.mono-project.com/repo/centos/ >> ${CASE_PATH}/mono_install.log
    yum -y install mono-complete >> ${CASE_PATH}/mono_install.log
    yum-config-manager --disable download.mono-project.com_repo_centos_ >> ${CASE_PATH}/mono_install.log
}
!
install_mono_rpm(){
	#rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"
	#yum-config-manager --add-repo http://download.mono-project.com/repo/centos/
	yum clean all
	#fix install mono fail issue on dell51
	yum remove -y giflib-5.1.4-2.el8.x86_64
	su -c 'curl https://download.mono-project.com/repo/centos7-stable.repo | tee /etc/yum.repos.d/mono-centos7-stable.repo'
	sleep 5
	yum -y install mono-complete-5.8.0.127-0.xamarin.3.epel7.x86_64
	#yum clean all
	#rm -f /etc/yum.repos.d/download.mono-project.com_repo_centos_.repo 
	#yum-config-manager --add-repo http://download.mono-project.com/repo/centos/
	#yum -y install mono-complete-5.8.0.127-0.xamarin.3.epel7.x86_64
	#yum-config-manager --disable download.mono-project.com_repo_centos_
}

install_rpms_ovs() {

# these need to be changed to by dynamic based on the beaker recipe
echo "start to install ovs rpm in host"
yum install -y git yum-utils openssl python-twisted-core python-twisted-web libibverbs
ping -w 1 -c 10 download-node-02.eng.bos.redhat.com
cat /etc/resolv.conf 
install_selinux_policy
#wget ${OVS_URL} -O ovs.rpm && rpm -ivh ovs.rpm 
yum install -y ${OVS_URL} > /dev/null 2>&1
rpm -qa|grep openvswitch
}

install_rpms_dpdk() {

#install dpdk in host
echo "start to install dpdk rpms in host..."
ping -w 1 -c 10 download-node-02.eng.bos.redhat.com
wget ${OVS_HOST_URL} -O dpdk.rpm && rpm -ivh dpdk.rpm
yum install -y ${DPDK_HOST_URL} > /dev/null 2>&1
yum install -y ${DPDK_TOOL_HOST_URL} > /dev/null 2>&1
rpm -qa|grep dpdk
if [ $? != 0 ];then
	rpm -ivh ${DPDK_HOST_URL} 
	rpm -ivh ${DPDK_TOOL_HOST_URL} 
fi
rpm -qa|grep dpdk
if [ $? != 0 ];then
	exit
fi
}


install_driverctl() {
yum install -y http://download.devel.redhat.com/brewroot/packages/driverctl/0.95/1.el7fdparch/noarch/driverctl-0.95-1.el7fdparch.noarch.rpm
}

change_to_driverctl(){
    \cp ${CASE_PATH}/beaker_ci_conf/dpdk_driverctl.py /root/vswitchperf/src/dpdk/dpdk.py
}

add_trafficgen_custom_conf() {
    #add the xena info to the traffic.conf
    echo "start to add the trafficgen info to the 03_traffic.conf"
    trafficgen=$1
    if [ "$trafficgen" == "xena" ]
    then
        cat >> /root/vswitchperf/conf/03_traffic.conf <<  EOF
TRAFFICGEN = 'Xena'
TRAFFICGEN_XENA_IP = '$XENA_IP'
TRAFFICGEN_XENA_PORT1 = '$XENA_PORT1'
TRAFFICGEN_XENA_PORT2 = '$XENA_PORT2'
TRAFFICGEN_XENA_USER = '$XENA_USER'
TRAFFICGEN_XENA_PASSWORD = '$XENA_PASSWORD'
TRAFFICGEN_XENA_MODULE1 = '$XENA_MODULE1'
TRAFFICGEN_XENA_MODULE2 = '$XENA_MODULE2'
TRAFFICGEN_XENA_2544_LATENCY_START_VALUE = '$LATENCY_START_VALUE'
TRAFFICGEN_XENA_2544_LATENCY_STEP_VALUE = '$LATENCY_STEP_VALUE'
TRAFFICGEN_XENA_2544_LATENCY_END_VALUE = '$LATENCY_END_VALUE'
EOF
    elif [ "$trafficgen" == "trex" ]
    then
        cat >> /root/vswitchperf/conf/03_traffic.conf <<  EOF
TRAFFICGEN = 'Trex'
TRAFFICGEN_TREX_HOST_IP_ADDR = '$TREX_IP'
TRAFFICGEN_TREX_USER = '$TREX_USER'
TRAFFICGEN_TREX_BASE_DIR = '$TREX_PATH'
TRAFFICGEN_TREX_PORT1 = '$TREX_PORT1'
TRAFFICGEN_TREX_PORT2 = '$TREX_PORT2'
TRAFFICGEN_TREX_LINE_SPEED_GBPS = '$TREX_SPEED'
TRAFFICGEN_TREX_LATENCY_PPS = $TREX_LATENCY
TRAFFICGEN_TREX_RFC2544_TPUT_THRESHOLD = $TREX_THRESHOLD
TRAFFICGEN_TREX_PORT_SPEED = $TREX_PORT_SPEED
TRAFFICGEN_TREX_FORCE_PORT_SPEED = ${TREX_FORCE_PORT_SPEED}
TRAFFICGEN_TREX_RFC2544_START_RATE = ${TREX_RFC2544_START_RATE}
TRAFFICGEN_TREX_VERIFICATION_MODE = True
TRAFFICGEN_TREX_VERIFICATION_DURATION = 60
TRAFFICGEN_TREX_MAXIMUM_VERIFICATION_TRIALS = 10
TRAFFICGEN_TREX_LEARNING_MODE = True
TRAFFICGEN_TREX_LEARNING_DURATION = 10
EOF
    fi
}


add_rte_version() {
    #copy the rte_version.sh to the folder
    echo "copy the rte_version.sh to the /usr/share/dpdk/lib/librte_eal/common/include/"
    mkdir -p /usr/share/dpdk/lib/librte_eal/common/include/
    #wget -P /usr/share/dpdk/lib/librte_eal/common/include/ http://netqe-infra01.knqe.eng.rdu2.dc.redhat.com/vsperf/rte_version.h
    wget -P /usr/share/dpdk/lib/librte_eal/common/include/ http://netqe-bj.usersys.redhat.com/share/tli/test_conf/rte_version.h
    cp /usr/share/dpdk/lib/librte_eal/common/include/rte_version.h /usr/share/dpdk/x86_64-native-linuxapp-gcc/
}

modify_guest_rhel_common() {
echo "start to modify the code about the redhat guest..."
#modify the code to make the guest use the redhat kernel and rpms
sed -i "s/scsi/ide/g"  /root/vswitchperf/conf/04_vnf.conf

#modify the redhat guest password
sed -i '/GUEST_PASSWORD =/c\GUEST_PASSWORD = ["redhat"]' /root/vswitchperf/conf/04_vnf.conf

}


change_xena(){
        sed -i '/LearningRatePercent/c\      "LearningRatePercent": 3.0,' /root/vswitchperf/tools/pkt_gen/xena/profiles/baseconfig.x2544
        sed -i '/LearningDuration/c\      "LearningDuration": 180000.0' /root/vswitchperf/tools/pkt_gen/xena/profiles/baseconfig.x2544
}

create_vm(){
        yum install libvirt* virt-install -y >> ${CASE_PATH}/libvirt_install.log 
        systemctl restart libvirtd
        pushd /root/
	if [ "$QCOW_LOC" == "Westford" ];then
		download_server="http://download.devel.redhat.com"
		sleep_time="1200"
		vmcreate="vmcreate"
	elif [ "$QCOW_LOC" == "China" ];then
		download_server="http://download.eng.pnq.redhat.com"
		sleep_time="10800"
		vmcreate="bj_vmcreate"
	fi
	chmod 777 ${CASE_PATH}/vmcreate.sh
        if [ "$4" == "NOVIOMMU" ]; then
                image=rhel${1}-vsperf-${2}-noviommu.qcow2
	elif [ "$4" == "VIOMMU" ];then
                image=rhel${1}-vsperf-${2}-viommu.qcow2
        fi
        
        if [ "$4" == "NOVIOMMU" ];then
                ${CASE_PATH}/vmcreate.sh -c ${3} -V ${1}
                sleep ${sleep_time}
        elif [ "$4" == "VIOMMU" ];then
                ${CASE_PATH}/vmcreate.sh -v -c ${3} -V ${1}
                sleep ${sleep_time}
        fi
        du -sh /var/lib/libvirt/images/master.qcow2
        mv /var/lib/libvirt/images/master.qcow2 /root/vswitchperf/$image
        sleep 300
        du -sh /root/vswitchperf/$image
        popd
}

modify_custom_conf(){
	sed -i '/TRAFFICGEN =/d'  /root/vswitchperf/conf/10_custom.conf
}

modify_06fwd_conf() {
    echo "start to modify 06_pktfwd.conf..."
    sed -i "/TESTPMD_FWD_MODE =/c\TESTPMD_FWD_MODE = 'io'" /root/vswitchperf/conf/06_pktfwd.conf
    sed -i "/PIDSTAT_MONITOR =/c\PIDSTAT_MONITOR = ['ovs-vswitchd', 'ovsdb-server', 'qemu-system-x86_64', 'vpp', 'qemu-kvm', 'testpmd']" /root/vswitchperf/conf/06_pktfwd.conf
}

modify_05collector_conf() {
    echo "start to modify 05_collector.conf..."
    sed -i "/PIDSTAT_MONITOR =/c\PIDSTAT_MONITOR = ['ovs-vswitchd', 'ovsdb-server', 'qemu-system-x86_64', 'vpp', 'qemu-kvm', 'testpmd']" /root/vswitchperf/conf/05_collector.conf
}

install_python34() {
    cd /root
    wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz > /dev/null 2>&1
    tar zxvf Python-3.4.3.tgz > /dev/null 2>&1
    cd Python-3.4.3
    ./configure > /dev/null 2>&1
    make > /dev/null 2>&1
    make install > /dev/null 2>&1
}

install_python36() {
	$dbg_flag
	if [[ -e /root/Python-3.6.8 ]] && [[ $(/root/Python-3.6.8/python -V) == "Python 3.6.8" ]]; then
		echo "Python-3.6.8 is already installed."
		return 0
	else
		echo "Installing Python-3.6.8..."
		cd /root
		wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz > /dev/null 2>&1
		tar zxvf Python-3.6.8.tgz > /dev/null 2>&1
		cd Python-3.6.8
		./configure > /dev/null 2>&1
		make > /dev/null 2>&1
		make install > /dev/null 2>&1
	fi
}

configure_xena() {
$dbg_flag
# Comment out installation of python34 to use python36 instead
# install_python34
install_python36
pushd /root/ 1>/dev/null
git clone https://github.com/ctrautma/NetScout.git
pushd /root/NetScout 1>/dev/null
#cp ${CASE_PATH}/settings.cfg .
chmod 777 NSConnect.py
if [ "$NetScout_speed" == "10" ];then
if [ "$QCOW_LOC" == "China" ];then
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuNzMuODguOQ==
EOF
else
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuMTkuMTUuNjU=
EOF
fi
else
if [ "$QCOW_LOC" == "China" ];then
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuNzMuODguOA==
EOF
else
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuMTkuMTUuMTAy
EOF
fi
fi
echo "start to switch machine connect to xena..."
# comment out references to Python-3.4.3 and instead point to Python-3.6.8
#/root/Python-3.4.3/python /root/NetScout/NSConnect.py --connect XENA_M${XENA_MODULE1}P${XENA_PORT1} ${NetScout_nic1}
#/root/Python-3.4.3/python /root/NetScout/NSConnect.py --connect XENA_M${XENA_MODULE1}P${XENA_PORT2} ${NetScout_nic2}
/root/Python-3.6.8/python /root/NetScout/NSConnect.py --connect XENA_M${XENA_MODULE1}P${XENA_PORT1} ${NetScout_nic1}
/root/Python-3.6.8/python /root/NetScout/NSConnect.py --connect XENA_M${XENA_MODULE1}P${XENA_PORT2} ${NetScout_nic2}

popd 1>/dev/null

}

configure_trex() {
$dbg_flag
# Comment out installation of python34 to use python36 instead
# install_python34
install_python36
pushd /root/ 1>/dev/null
git clone https://github.com/ctrautma/NetScout.git
pushd /root/NetScout 1>/dev/null
#cp ${CASE_PATH}/settings.cfg .
chmod 777 NSConnect.py
if [ "$NetScout_speed" == "10" ];then
if [ "$QCOW_LOC" == "China" ];then
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuNzMuODguOQ==
EOF
else
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuMTkuMTUuNjU=
EOF
fi
elif [ "$NetScout_speed" == "100" ];then
if [ "$QCOW_LOC" == "China" ];then
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuNzMuODguOA==
EOF
else
cat >> /root/NetScout/settings.cfg <<  EOF
[INFO] 
password = bmV0c2NvdXQx
username = YWRtaW5pc3RyYXRvcg==
port = NTMwNTg=
host = MTAuMTkuMTUuMTAy
EOF
fi
fi
echo "start to switch machine connect to xena..."
# comment out references to Python-3.4.3 and instead point to Python-3.6.8
#/root/Python-3.4.3/python /root/NetScout/NSConnect.py --connect ${Trex_nic1} ${NetScout_nic1}
#/root/Python-3.4.3/python /root/NetScout/NSConnect.py --connect ${Trex_nic2} ${NetScout_nic2}
/root/Python-3.6.8/python /root/NetScout/NSConnect.py --connect ${Trex_nic1} ${NetScout_nic1}
/root/Python-3.6.8/python /root/NetScout/NSConnect.py --connect ${Trex_nic2} ${NetScout_nic2}
popd 1>/dev/null

}


configure_ssh_trex() {
    expect -c "
    spawn ssh-keygen -b 2048 -t rsa
    expect \"file in which to save the key\"
    send \"\n\r\"
    expect \"Enter passphrase\"
    send \"\n\r\"
    expect \"Enter same passphrase again\"
    send \"\n\r\"
    expect eof
    spawn ssh-copy-id ${TREX_IP}
    expect \"Are you sure you want to\"
    send \"yes\n\r\"
    expect \"password:\"
    send \"${passwd}\n\r\"
    expect eof
"
}


copy_module_manager(){
    \cp ${CASE_PATH}/beaker_ci_conf/module_manager.py /root/vswitchperf/tools/module_manager.py
}

create_vsperf_img(){
if [ "${RUN_JOB}" == "nightly" ];then
    rlRun "create_vm ${GUEST_IMG} 1Q 3 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 2Q 5 NOVIOMMU"
elif [ "${RUN_JOB}" == "weekly" ];then
    rlRun "create_vm ${GUEST_IMG} 1Q 3 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 2Q 5 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 4Q 9 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 1Q 3 VIOMMU"
    rlRun "create_vm ${GUEST_IMG} 2Q 5 VIOMMU"
    rlRun "create_vm ${GUEST_IMG} 4Q 9 VIOMMU"
elif [ "${RUN_JOB}" == "gating" ];then
    rlRun "create_vm ${GUEST_IMG} 1Q 3 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 2Q 5 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 4Q 9 NOVIOMMU"
    rlRun "create_vm ${GUEST_IMG} 1Q 3 VIOMMU"
    rlRun "create_vm ${GUEST_IMG} 2Q 5 VIOMMU"
    rlRun "create_vm ${GUEST_IMG} 4Q 9 VIOMMU"
fi
}

copy_guest_dpdk(){
    yum install libguestfs-tools -y
    systemctl start libvirtd
    export LIBGUESTFS_BACKEND=direct
    wget -P /root/guest_dpdk_rpms/ ${DPDK_GUEST_URL}  > /dev/null 2>&1
    wget -P /root/guest_dpdk_rpms/ ${DPDK_TOOL_GUEST_URL}  > /dev/null 2>&1
    dir=`ls /root/vswitchperf/ | grep qcow2`
    for i in $dir
    do
      if [ $VERSION_ID == "8.2" ]; then
        LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/$i /root/guest_dpdk_rpms/dpdk*.rpm /root/dpdkrpms/
      else
        LIBGUESTFS_MEMSIZE=2048 virt-copy-in -a /root/vswitchperf/$i /root/guest_dpdk_rpms/dpdk*.rpm /root/dpdkrpms/
      fi
    done
}

rlJournalStart
rlPhaseStartSetup
rlRun "clone_and_checkout_vsperf"
OS_NAME_NEW=`echo $OS_NAME|awk -F '.' '{printf $1"_"$2}'`
change_to_${OS_NAME_NEW}

cp ${CASE_PATH}/beaker_ci_conf/prepare_python_env.sh /root/vswitchperf/systems/rhel/${OS_NAME}/prepare_python_env.sh
rlRun "build_vsperf_without_upstream_builds"
rlRun "make_trex"
if [ ${image_method} == "download" ];then
	rlRun "download_vnf_image"
elif [ ${image_method} == "create" ];then
	rlRun "create_vsperf_img"
fi
if [ ${copy_dpdk} == "yes" ];then
	rlRun "copy_guest_dpdk"
fi
rlRun "modify_06fwd_conf"
rlRun "modify_05collector_conf"
source ${CASE_PATH}/beaker_ci_conf/install_mono.sh
if [ ${TRAFFIC_GEN} == "xena" ];then
	if (($(bc <<< "$OS_NAME >= 8"))); then
		rlRun "install_mono_without_rebuild" 
	else
		rlRun "install_mono_rpm"
	fi
fi
rlRun "install_rpms_ovs"
rlRun "install_rpms_dpdk"
rlRun "del_custom_conf_traffic"
rlRun "add_trafficgen_custom_conf ${TRAFFIC_GEN}"
rlRun "modify_guest_rhel_common"
rlRun "modify_custom_conf"
rlRun "modify_testcase"
rlRun "modify_latency_test"
rlRun "add_rte_version"
rlRun "enable_ovs_debug"
if [ ${TRAFFIC_GEN} == "xena" ];then
	rlRun "download_Xena2544"
	rlRun "configure_xena"
	rlRun "change_xena"
elif [ ${TRAFFIC_GEN} == "trex" ];then
	rlRun "configure_trex"
	rlRun "configure_ssh_trex"
fi
rlRun "copy_ovsvanilla_openvswitch"
rlRun "copy_module_manager"
rlRun "install_driverctl"
rlRun "change_to_driverctl"
rlPhaseEnd
rlJournalEnd
