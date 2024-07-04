#!/bin/bash
# Include Beaker environment
. /mnt/tests/kernel/networking/common/include.sh || exit 1

CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
. /etc/os-release
if (($(bc <<< "$VERSION_ID >= 8"))); then
VSPERF_CMD="/usr/libexec/platform-python /root/vswitchperf/vsperf"
else
VSPERF_CMD="/root/vswitchperf/vsperf"
fi
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/common.sh

nic_info_file="${CASE_PATH}/nic_info.conf"
if [ -f "$nic_info_file" ]; then
    source $nic_info_file
fi

set -x


run_pvp_tput_sriov(){
	ip link set ${NIC1} up
        ip link set ${NIC2} up
	mkdir -p /usr/share/dpdk/x86_64-native-linuxapp-gcc/app/
	cp /usr/bin/dpdk-testpmd /usr/share/dpdk/x86_64-native-linuxapp-gcc/app/
	#if [ ${NIC_DRIVER} == "bnxt_en" ];then	
	#	bug1572840
	#	bnxt_patch	
	if [ ${NIC_DRIVER} == "mlx5_core" ] ||  [ ${NIC_DRIVER} == "mlx4_en" ];then
		mlx_patch_sriov	
	elif [ ${NIC_DRIVER} == "qede" ];then
                qede_patch_sriov
	        \cp ${CASE_PATH}/beaker_ci_conf/trex_qede.py /root/vswitchperf/tools/pkt_gen/trex/trex.py	
	else
		ixgbe_patch
	fi
	for i in 64 128 256 1500
        do
	pushd /root/vswitchperf/
	${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_baseline_guest_${1}.conf --vswitch=none --vnf QemuPciPassthrough --test-params "TRAFFICGEN_DURATION=60;TRAFFICGEN_LOSSRATE=${LOSSRATE};TRAFFICGEN_PKT_SIZES=(${i},);TRAFFICGEN_RFC2544_TESTS=1"
	move_result "gating_baseline_guest_pvp_tput_${i}_0.00_${TRAFFIC_GEN}_${1}"
	popd
	done
	\cp ${CASE_PATH}/beaker_ci_conf/trex.py /root/vswitchperf/tools/pkt_gen/trex/trex.py
}

run_pvp_tput_testpmd_as_switch(){
        # echo 0 > /proc/sys/kernel/nmi_watchdog
        # echo aa,aaaaaaaa,aaaaaaaa > /sys/bus/workqueue/devices/writeback/cpumask
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_baseline_testpmd_as_switch.conf --vswitch=none --fwdapp=TestPMD --test-params "TRAFFICGEN_DURATION=60;TRAFFICGEN_LOSSRATE=${LOSSRATE};TRAFFICGEN_PKT_SIZES=(64,);TRAFFICGEN_RFC2544_TESTS=1"
        popd
        move_result "gating_baseline_testpmd_as_switch_pvp_tput_64_0.00_${TRAFFIC_GEN}"
}


run_pvp_tput_1q_2pmd(){
 	for i in 64 128 256 1500
        do
	if [ ${1} == "enableviommu" ];then
		sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf
		\cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
	fi
        pushd /root/vswitchperf/
	${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}"
	popd
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
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
        done
}


run_pvp_tput_2q_4pmd(){
	for i in 64 128 256 1500
        do
        if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2q_testpmd_4pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_2-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
	done
}

run_pvp_tput_4q_8pmd(){
	for i in 64 128 256 1500
        do
        if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4q_testpmd_8pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4q_testpmd_8pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_4-Queue_${i}_0.00_UseCase-1A_8pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
	done
}

get_half_pps(){
        if [ ${NetScout_speed} == '10' ];then
                linespeed64=14880000
                linespeed128=8440000
                linespeed256=4520000
                linespeed1500=820000
	elif [ ${NetScout_speed} == '100' ];then
		linespeed64=148800000
                linespeed128=84400000
                linespeed256=45200000
                linespeed1500=8200000
	elif [ ${NetScout_speed} == '25' ];then
                linespeed64=37200000
                linespeed128=21100000
                linespeed256=11300000
                linespeed1500=2050000
	fi
        path=$1
        if [ $TRAFFIC_GEN == 'trex' ];then
                rx_pps=`cat $path| grep pvp_tput | awk -F ',' '{print $4}'`
        elif [ $TRAFFIC_GEN == 'xena' ];then
                rx_pps=`cat $path| grep pvp_tput | awk -F ',' '{print $1}'`
        fi
	if [ $2 == '64' ]; then
		line_speed=$linespeed64
	elif [ $2 == '128' ];then
		line_speed=$linespeed128
	elif [  $2 == '256' ];then
		line_speed=$linespeed256
	elif [  $2 == '1500' ];then
		line_speed=$linespeed1500
	fi
	rx_pps=$(echo "${rx_pps}*100/4"|bc)
	half_pps_percent=$(echo "$rx_pps/${line_speed}"|bc)
        echo  $half_pps_percent
}

run_pvp_latency_half_1q_2pmd(){
	for i in 64 128 256 1500
	do
	        if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
	half_pps_percent=`get_half_pps "/tmp/gating_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}/result*/*.csv" ${i}`
        replace="'frame_rate': ${half_pps_percent},"
        echo $half_pps_percent
        if [ $TRAFFIC_GEN == 'trex' ];then
                sed -i "/frame_rate/c\    ${replace}"  $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf
        elif [ $TRAFFIC_GEN == 'xena' ];then
                cat >> $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf << EOF
TRAFFICGEN_XENA_2544_LATENCY_START_VALUE='${half_pps_percent}'
TRAFFICGEN_XENA_2544_LATENCY_END_VALUE='${half_pps_percent}'
EOF
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_latency --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}_latency"
        popd
        done
}

run_pvp_latency_half_1q_4pmd(){
  # due to run_pvp_tput_1q_4pmd just run 64 and 1500 bytes, so latency just test 64 and 1500 bytes.
        for i in 64  1500
        do
                if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1
q_testpmd_4pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        half_pps_percent=`get_half_pps "/tmp/gating_1-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}/result*/*.csv" ${i}`
        replace="'frame_rate': ${half_pps_percent},"
        echo $half_pps_percent
        if [ $TRAFFIC_GEN == 'trex' ];then
                sed -i "/frame_rate/c\    ${replace}"  $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf
        elif [ $TRAFFIC_GEN == 'xena' ];then
                cat >> $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf << EOF
TRAFFICGEN_XENA_2544_LATENCY_START_VALUE='${half_pps_percent}'
TRAFFICGEN_XENA_2544_LATENCY_END_VALUE='${half_pps_percent}'
EOF
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_latency --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60
; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}_latency"
        popd
        done
}

run_pvp_latency_half_2q_4pmd(){
        for i in 64 128 256 1500
        do
                if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2
q_testpmd_4pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        half_pps_percent=`get_half_pps "/tmp/gating_2-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}/result*/*.csv" ${i}`
        replace="'frame_rate': ${half_pps_percent},"
        echo $half_pps_percent
        if [ $TRAFFIC_GEN == 'trex' ];then
                sed -i "/frame_rate/c\    ${replace}"  $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2q_testpmd_4pmd_${1}.conf
        elif [ $TRAFFIC_GEN == 'xena' ];then
                cat >> $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2q_testpmd_4pmd_${1}.conf << EOF
TRAFFICGEN_XENA_2544_LATENCY_START_VALUE='${half_pps_percent}'
TRAFFICGEN_XENA_2544_LATENCY_END_VALUE='${half_pps_percent}'
EOF
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_latency --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_2q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60
; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_2-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}_latency"
        popd
        done
}

run_pvp_latency_half_4q_8pmd(){
        for i in 64 128 256 1500
        do
                if [ ${1} == "enableviommu" ];then
                sed -i 's/VSWITCHD_DPDK_CONFIG = {/VSWITCHD_DPDK_CONFIG = {"vhost-iommu-support":"true",/g' $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4
q_testpmd_8pmd_${1}.conf
                \cp ${CASE_PATH}/beaker_ci_conf/qemu_dpdk_vhost_user_viommu.py /root/vswitchperf/vnfs/qemu/qemu_dpdk_vhost_user.py
        fi
        half_pps_percent=`get_half_pps "/tmp/gating_4-Queue_${i}_0.00_UseCase-1A_8pmd_testpmd_${TRAFFIC_GEN}_${1}/result*/*.csv" ${i}`
        replace="'frame_rate': ${half_pps_percent},"
        echo $half_pps_percent
        if [ $TRAFFIC_GEN == 'trex' ];then
                sed -i "/frame_rate/c\    ${replace}"  $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4q_testpmd_8pmd_${1}.conf
        elif [ $TRAFFIC_GEN == 'xena' ];then
                cat >> $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4q_testpmd_8pmd_${1}.conf << EOF
TRAFFICGEN_XENA_2544_LATENCY_START_VALUE='${half_pps_percent}'
TRAFFICGEN_XENA_2544_LATENCY_END_VALUE='${half_pps_percent}'
EOF
        fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_latency --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_4q_testpmd_8pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60
; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_4-Queue_${i}_0.00_UseCase-1A_8pmd_testpmd_${TRAFFIC_GEN}_${1}_latency"
        popd
        done
}


run_jumbo_case(){
	for i in 2000 9000
        do
	pushd /root/vswitchperf/
	echo "${i}" > /sys/class/net/${NIC1}/mtu
        echo "${i}" > /sys/class/net/${NIC2}/mtu        
	${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}_${i}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}"
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}_${i}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}"
	popd
	done
}

run_enablebuf_case(){
        for i in 64 1500
        do
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}"
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_4pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_4pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
	done
}

run_higher_flow_case(){
        for i in 64 1500
        do
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_dpdk_1q_testpmd_2pmd_${1}.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=${LOSSRATE}; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.00_UseCase-1A_2pmd_testpmd_${TRAFFIC_GEN}_${1}"
        popd
        done
}

configure_tuna_host() {
    yum install -y tuna
    ip link set ${NIC1} up
    ip link set ${NIC2} up
    tuna -q "${NIC1}*" -c $(python2 ${case_path}/get_pmd.py --cmd last_skip_cpu --nic ${NIC1} --cpu 4 --skip 2) -m -x
    tuna -q "${NIC2}*" -c $(python2 ${case_path}/get_pmd.py --cmd last_skip_cpu --nic ${NIC2} --cpu 4 --skip 4) -m -x
}

run_vanilla_linuxbridge_case(){
	configure_tuna_host
	for i in 64 1500
        do
		if (($(bc <<< "$VERSION_ID >= 8"))); then
		\cp ${CASE_PATH}/beaker_ci_conf/qemu_ovsvanilla.py /root/vswitchperf/vnfs/qemu/qemu.py
	fi
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_ovsvanilla_1q_linuxbridge.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.002; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.002_UseCase-2A_vanilla_linuxbridge"
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_ovsvanilla_2q_linuxbridge.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.002; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_2-Queue_${i}_0.002_UseCase-2A_vanilla_linuxbridge"
        popd
        done
}


run_vanilla_testpmd_case(){
        for i in 64 1500
        do
        \cp ${CASE_PATH}/beaker_ci_conf/qemu_viommu.py /root/vswitchperf/vnfs/qemu/qemu.py
	\cp ${CASE_PATH}/beaker_ci_conf/qemu_virtio_net.py /root/vswitchperf/vnfs/qemu/qemu_virtio_net.py
        pushd /root/vswitchperf/
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_ovsvanilla_1q_testpmd.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.002; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_1-Queue_${i}_0.002_UseCase-2A_vanilla_testpmd"
        ${VSPERF_CMD} pvp_tput --conf-file $CASE_PATH/${CUSTOM_CONF}/10_custom_ovsvanilla_2q_testpmd.conf --test-params "TRAFFICGEN_DURATION=60; TRAFFICGEN_PKT_SIZES=(${i},); TRAFFICGEN_LOSSRATE=0.002; TRAFFICGEN_RFC2544_TESTS=1"
        sleep 1
        move_result "gating_2-Queue_${i}_0.002_UseCase-2A_vanilla_testpmd"
        popd
        done
}


#if [ -z "${REBOOTCOUNT}" ] || [ "${REBOOTCOUNT}" -eq 0 ]; then
if ! ls ${CASE_PATH}/TASK*; then
  swapoff -a
	get_nic_info
        sh $CASE_PATH/install_tune_dpdk.sh
	microcode_rpm=`rpm -qa|grep microcode`
	if [ ${RT_TEST} == "YES" ];then 
		yum install kernel-rt-kvm* -y
		modprobe kvm-intel
		if [ ${VERSION_ID} == "7.8" ];then
		yum install -y http://download.devel.redhat.com/brewroot/packages/kernel-rt/3.10.0/1127.rt56.1093.el7/x86_64/kernel-rt-3.10.0-1127.rt56.1093.el7.x86_64.rpm
		elif  [ ${VERSION_ID} == "7.7" ];then
        	yum install -y http://download.devel.redhat.com/brewroot/packages/kernel-rt/3.10.0/1062.3.1.rt56.1026.el7/x86_64/kernel-rt-3.10.0-1062.3.1.rt56.1026.el7.x86_64.rpm
		fi
	fi
	#rpm -e ${microcode_rpm}
	#rpm -ivh http://download.devel.redhat.com/brewroot/packages/microcode_ctl/2.1/29.el7/x86_64/microcode_ctl-2.1-29.el7.x86_64.rpm
	#rpm -ivh http://perf1.perf.lab.eng.bos.redhat.com/pub/.cve/retpoline/rhel75_retp/kernel-3.10.0-838.el7.final.x86_64.rpm --force
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
ls -l ${CASE_PATH}
#if  [ "${REBOOTCOUNT}" -eq 1 ]; then
if [ -f ${CASE_PATH}/TASK1 ]; then
  swapoff -a
	echo "uname -a"
	uname -a
	echo "cat ibpb_enabled"	
	cat /sys/kernel/debug/x86/ibpb_enabled
	echo "cat ibrs_enabled"
	cat /sys/kernel/debug/x86/ibrs_enabled
	echo "cat retp_enabled"
	cat /sys/kernel/debug/x86/retp_enabled
	echo "cat pti_enabled"
	cat /sys/kernel/debug/x86/pti_enabled
	install_qemu ${QEMU_VER}
	sh $CASE_PATH/install_vsperf.sh
	version=`rpm -qa|grep openvswitch | awk -F '-' '{print $2}'`
	if (($(bc <<< "$VERSION_ID < 8"))); then
        	install_selinux_rpm
	fi
        setenforce 1
	init_conf
	if [ ${cpu_custom} == "yes" ];then
		init_custom_conf
	fi
	if [ ${NIC_DRIVER} == "mlx5_core" ];then
		mlx_patch
	fi
	if [ ${NIC_DRIVER} == "nfp" ];then
                nfp_patch
        fi
	if [ ${NIC_DRIVER} == "mlx4_en" ];then
                mlx4_patch2
        fi
        #if [ ${NIC_DRIVER} == "bnxt_en" ];then
	#	exit
	#fi
	# for ovs vanilla case on qede nic, if use rhel7.5 kernel, performance was low, and should use the test kernel
	. /etc/os-release
	OS_NAME="$VERSION_ID"
	if [ "$OS_NAME" == "7.5" ] && [ ${NIC_DRIVER} == "qede" ];then
		pushd ${CASE_PATH}
		wget ftp://10.19.188.65/kernel-3.10.0-862.el7.bz1558328.x86_64.rpm --ftp-user=user1 --ftp-password=xena
		rpm -ivh kernel-3.10.0-862.el7.bz1558328.x86_64.rpm --nodeps
		popd
	fi
	if [ ${verification} == "yes" ];then
        	add_verification
	fi
	Activate_Python3
        install_qemu ${QEMU_VER}
	modify_qemu_file_enable_viommu
        #bug1378586_workaround ovsdpdkvhost
:<<block
        if [ ${NIC_DRIVER} != "nfp" ];then
        run_pvp_tput_sriov novlan
	modify_qemu_file_testpmd_as_switch
	run_pvp_tput_testpmd_as_switch
        fi
block
        run_pvp_tput_sriov novlan
        modify_qemu_file_testpmd_as_switch
        run_pvp_tput_testpmd_as_switch
        touch ${CASE_PATH}/TASK2
        rm -f ${CASE_PATH}/TASK1
        echo "before the second reboot, check whether has TASK2, and remove TASK1"
        ls -l ${CASE_PATH}
	rhts-reboot
        exit
fi
#if  [ "${REBOOTCOUNT}" -eq 2 ]; then
echo "check whether has TASK2 in after the second reboot"
ls -l ${CASE_PATH}
if [ -f ${CASE_PATH}/TASK2 ]; then
        version=`rpm -qa|grep openvswitch | awk -F '-' '{print $2}'`
        if [[ $version =~ "2.9."[0-9] ]];then
                setenforce 0
        else
		      setenforce 1
	      fi
	swapoff -a
	Activate_Python3
	modify_qemu_file_disable_viommu
	run_pvp_tput_1q_2pmd novlan
	run_pvp_tput_1q_4pmd novlan
	run_pvp_tput_2q_4pmd novlan
	if [[ $ENABLE_HT == "yes" ]]; then
	  run_pvp_tput_4q_8pmd novlan
	else
	  usleep
	fi
	run_pvp_tput_1q_2pmd vlan
  run_pvp_tput_2q_4pmd vlan
  if [[ $ENABLE_HT == "yes" ]]; then
	  run_pvp_tput_4q_8pmd vlan
	else
	  usleep
	fi
	#add pvp latency test with 50% throughtput
	
	run_pvp_latency_half_1q_2pmd novlan
	run_pvp_latency_half_1q_4pmd novlan
  run_pvp_latency_half_2q_4pmd novlan
  if [[ $ENABLE_HT == "yes" ]]; then
    run_pvp_latency_half_4q_8pmd novlan
  else
	  usleep
	fi
  run_pvp_latency_half_1q_2pmd vlan
  run_pvp_latency_half_2q_4pmd vlan
  if [[ $ENABLE_HT == "yes" ]]; then
    run_pvp_latency_half_4q_8pmd vlan
  else
	  usleep
	fi
	run_enablebuf_case enablebuf
	run_jumbo_case novlan 
  run_higher_flow_case 10kflows
	run_higher_flow_case 100kflows
	run_higher_flow_case 1mflows
	#bug1378586_workaround ovsvanilla
	copy_vswitch_vanilla
	disable_ovs_debug	
	run_vanilla_testpmd_case
	install_qemu ${QEMU_VER}
        modify_qemu_file_enable_viommu
	#bug1378586_workaround ovsdpdkvhost
	copy_vswitch_dpdk
  enable_ovs_debug
	run_pvp_tput_1q_2pmd enableviommu
	run_pvp_tput_2q_4pmd enableviommu
	\cp ${CASE_PATH}/beaker_ci_conf/ovs.py /root/vswitchperf/vswitches/ovs.py
	if [[ $ENABLE_HT == "yes" ]]; then
	  run_pvp_tput_4q_8pmd enableviommu
	else
	  usleep
	fi
	# add pvp latency test with 50% throughput 
  run_pvp_latency_half_1q_2pmd enableviommu
  run_pvp_latency_half_2q_4pmd enableviommu
  if [[ $ENABLE_HT == "yes" ]]; then
    run_pvp_latency_half_4q_8pmd enableviommu
  else
	  usleep
	fi
fi
deactivate
run_gating_report
