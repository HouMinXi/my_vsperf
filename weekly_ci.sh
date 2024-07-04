#!/bin/bash
# Include Beaker environment
. /mnt/tests/kernel/networking/common/include.sh || exit 1

CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
VSPERF_CMD="/root/vswitchperf/vsperf"
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/common.sh

nic_info_file="${CASE_PATH}/nic_info.conf"
if [ -f "$nic_info_file" ]; then
    source $nic_info_file
fi

set -x
. /etc/os-release
if (($(bc <<< "$VERSION_ID >= 8"))); then
VSPERF_CMD="/usr/libexec/platform-python /root/vswitchperf/vsperf"
else
VSPERF_CMD="/root/vswitchperf/vsperf"
fi

run_pvp_tput_sriov(){
	ip link set ${NIC1} up
        ip link set ${NIC2} up
	mkdir -p /usr/share/dpdk/x86_64-native-linuxapp-gcc/app/
	cp /usr/bin/dpdk-testpmd /usr/share/dpdk/x86_64-native-linuxapp-gcc/app/
        if [ ${NIC_DRIVER} == "mlx5_core" ] || [ ${NIC_DRIVER} == "bnxt_en" ];then
                bnxt_patch
        fi
	for i in 64 128 256 1500
        do
	pushd /root/vswitchperf/
	${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_baseline_guest_${1}.conf --vswitch=none --vnf QemuPciPassthrough --test-params "TRAFFICGEN_DURATION=600;TRAFFICGEN_LOSSRATE=0.00;TRAFFICGEN_PKT_SIZES=(${i},);TRAFFICGEN_RFC2544_TESTS=1"
	move_result "weekly_baseline_guest_pvp_tput_${i}_0.00_${TRAFFIC_GEN}_${1}"
	popd
	done
}

run_pvp_tput_testpmd_as_switch(){
        echo 0 > /proc/sys/kernel/nmi_watchdog
        echo aa,aaaaaaaa,aaaaaaaa > /sys/bus/workqueue/devices/writeback/cpumask
        pushd /root/vswitchperf/
        /root/vswitchperf/vsperf pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_baseline_testpmd_as_switch.conf --vswitch=none --fwdapp=TestPMD --test-params 'TRAFFICGEN_DURATION=600;TRAFFICGEN_LOSSRATE=0.00;TRAFFICGEN_PKT_SIZES=(64,);TRAFFICGEN_RFC2544_TESTS=1'
        popd
        move_result "weekly_baseline_testpmd_as_switch_pvp_tput_64_0.00_${TRAFFIC_GEN}"
}

run_pvp_tput_1q_2pmd(){
 	for i in 64 128 256 1500
        do
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=600; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.00; TRAFFICGEN_RFC2544_TESTS=1"
        move_result "weekly_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}"
	popd
	done
}

run_pvp_tput_2q_4pmd(){
	for i in 64 128 256 1500
        do
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=600; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.00; TRAFFICGEN_RFC2544_TESTS=1"
        move_result "weekly_2-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
	done
}

run_pvp_tput_4q_8pmd(){
	for i in 64 128 256 1500
        do
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4q_testpmd_8pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=600; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.00; TRAFFICGEN_RFC2544_TESTS=1"
        move_result "weekly_4-Queue_${i}_0.00_UseCase-1A_8pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
	done
}


if [ -z "${REBOOTCOUNT}" ] || [ "${REBOOTCOUNT}" -eq 0 ]; then
        get_nic_info
	sh $CASE_PATH/install_tune_dpdk.sh
        rhts-reboot
fi
if  [ "${REBOOTCOUNT}" -eq 1 ]; then
	sh $CASE_PATH/install_vsperf.sh
	if (($(bc <<< "$VERSION_ID < 8"))); then
                install_selinux_rpm
	fi
        setenforce 1
	init_conf
	if [ ${NIC_DRIVER} == "mlx5_core" ];then
                mlx_patch
        fi
        if [ ${NIC_DRIVER} == "nfp" ];then
                nfp_patch
        fi
        if [ ${NIC_DRIVER} == "mlx4_en" ];then
                mlx4_patch2
        fi
        Activate_Python3
        install_qemu ${QEMU_VER}
	modify_qemu_file_enable_viommu
        #bug1378586_workaround ovsdpdkvhost
        run_pvp_tput_sriov novlan
	modify_qemu_file_testpmd_as_switch
	echo "cat /root/vswitchperf/11_beaker.conf"
	cat /root/vswitchperf/conf/11_beaker.conf
	run_pvp_tput_testpmd_as_switch
        rhts-reboot
fi
if  [ "${REBOOTCOUNT}" -eq 2 ]; then
        version=`rpm -qa|grep openvswitch | awk -F '-' '{print $2}'`
        if [[ $version =~ "2.9."[0-9] ]];then
                setenforce 1
        fi
	Activate_Python3
	modify_qemu_file_disable_viommu
        run_pvp_tput_1q_2pmd novlan
	run_pvp_tput_1q_2pmd vlan
        run_pvp_tput_2q_4pmd novlan
        run_pvp_tput_2q_4pmd vlan
	run_pvp_tput_4q_8pmd novlan
        run_pvp_tput_4q_8pmd vlan
	install_qemu ${QEMU_VER}
	modify_qemu_file_enable_viommu	
        run_pvp_tput_1q_2pmd enableviommu
	run_pvp_tput_2q_4pmd enableviommu
	run_pvp_tput_4q_8pmd enableviommu   
fi 
deactivate
run_weekly_report
