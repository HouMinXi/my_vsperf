#!/bin/bash
# Include Beaker environment
. /mnt/tests/kernel/networking/common/include.sh || exit 1

CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
VSPERF_CMD="/root/vswitchperf/vsperf"
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/common.sh

set -x
. /etc/os-release
if (($(bc <<< "$VERSION_ID >= 8"))); then
VSPERF_CMD="/usr/libexec/platform-python /root/vswitchperf/vsperf"
else
VSPERF_CMD="/root/vswitchperf/vsperf"
fi

nic_info_file="${CASE_PATH}/nic_info.conf"
if [ -f "$nic_info_file" ]; then
    source $nic_info_file
fi


run_pvp_tput_sriov(){
	ip link set ${NIC1} up
        ip link set ${NIC2} up
        mkdir -p /usr/share/dpdk/x86_64-native-linuxapp-gcc/app/
        cp /usr/bin/dpdk-testpmd /usr/share/dpdk/x86_64-native-linuxapp-gcc/app/
        #if [ ${NIC_DRIVER} == "bnxt_en" ];then
		#bug1572840
                #bnxt_patch
        if [ ${NIC_DRIVER} == "mlx5_core" ] ||  [ ${NIC_DRIVER} == "mlx4_en" ];then
                mlx_patch_sriov
        else
                ixgbe_patch
        fi
	for i in 64 1500
	do
	pushd /root/vswitchperf/
	${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_baseline_guest_${1}.conf --vswitch=none --vnf QemuPciPassthrough --test-params "TRAFFICGEN_DURATION=600;TRAFFICGEN_LOSSRATE=0.00;TRAFFICGEN_PKT_SIZES=(${i},);TRAFFICGEN_RFC2544_TESTS=1"
	popd
	move_result "nightly_baseline_guest_pvp_tput_${i}_0.00_${TRAFFIC_GEN}"
	done
}

run_pvp_tput_1q_2pmd(){
	for i in 64 1500
        do	
        if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=600; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.00; TRAFFICGEN_RFC2544_TESTS=1"
        popd
	move_result "nightly_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}"
	pushd /root/vswitchperf/
	done
}

run_pvp_tput_1q_4pmd(){
	for i in 64 1500
        do
        if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=600; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.00; TRAFFICGEN_RFC2544_TESTS=1"
        popd
        move_result "nightly_1-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}"
	pushd /root/vswitchperf/
	done
}

if ! ls ${CASE_PATH}/TASK*; then
#if [ -z "${REBOOTCOUNT}" ] || [ "${REBOOTCOUNT}" -eq 0 ]; then
        get_nic_info 
	sh $CASE_PATH/install_tune_dpdk.sh
	if [ ${NIC_DRIVER} == "mlx4_en" ];then
                mlx4_patch1
        fi
        if [ ${NIC_DRIVER} == "qede" ];then
                qede_patch
        fi
        touch ${CASE_PATH}/TASK1
        echo "Before the first reboot, after touch the TASK1, check whether create TASK1"
        ls -l ${CASE_PATH}
        rhts-reboot
        exit
fi
echo "check whether has TASK1 after the first reboot"
if [ -f ${CASE_PATH}/TASK1 ]; then
#if  [ "${REBOOTCOUNT}" -eq 1 ]; then
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
	if [ ${verification} == "yes" ];then
                add_verification
        fi
	Activate_Python3
	install_qemu ${QEMU_VER}
	modify_qemu_file_enable_viommu
        #bug1378586_workaround ovsdpdkvhost
        run_pvp_tput_sriov novlan
        touch ${CASE_PATH}/TASK2
        rm -f ${CASE_PATH}/TASK1
        echo "before the second reboot, check whether has TASK2, and remove TASK1"
        ls -l ${CASE_PATH}
        rhts-reboot
        exit
fi
if [ -f ${CASE_PATH}/TASK2 ] && [ ${sriov_only} == "no" ]; then
#if  [ "${REBOOTCOUNT}" -eq 2 ]; then
        version=`rpm -qa|grep openvswitch | awk -F '-' '{print $2}'`
        if (($version > 2.9));then
                setenforce 1
        fi
	Activate_Python3
	if [ ${nightly_viommu} == "disable" ];then
		modify_qemu_file_disable_viommu
        	run_pvp_tput_1q_2pmd novlan
		run_pvp_tput_1q_4pmd novlan
	else
		modify_qemu_file_enable_viommu
		run_pvp_tput_1q_2pmd enableviommu
		run_pvp_tput_1q_4pmd enableviommu
	fi
fi
deactivate
run_nightly_report
