#!/bin/bash 
RUN_JOB=${RUN_JOB:-"nightly"}
QEMU_VER=${QEMU_VER:-"custom"}
QCOW_LOC=${QCOW_LOC:-"Westford"}
TUNED_VER=${TUNED_VER:-"28"}
ENABLE_HT=${ENABLE_HT:-"no"}
#VSPERF_COMMIT=${VSPERF_COMMIT:-"8d528f2b4c66d94ea8760053f9bc75c595630056"}
#VSPERF_COMMIT=${VSPERF_COMMIT:-"9d2900035923bf307477c5b4b8dc423ba1b2086f"}
VSPERF_COMMIT=${VSPERF_COMMIT:-"91e0985be7ca2b2654f89928315431228b7ecc56"}
#VSPERF_COMMIT=${VSPERF_COMMIT:-"90ef48d4342a983c7733b8c21bb902d1dab2685a"}
NAY=${NAY:-"yes"}
PVT=${PVT:-"no"}
NIC_NUM=${NIC_NUM:-2}
NIC_DRIVER=${NIC_DRIVER:-"ixgbe"}
NIC1=${NIC1:-"p6p1"}
NIC2=${NIC2:-"p6p2"}
XENA_IP=${XENA_IP:-"10.19.15.19"}
XENA_PORT1=${XENA_PORT1:-0}
XENA_PORT2=${XENA_PORT2:-1}
XENA_USER=${XENA_USER:-"vsperf"}
XENA_PASSWORD=${XENA_PASSWORD:-"xena"}
XENA_MODULE1=${XENA_MODULE1:-7}
XENA_MODULE2=${XENA_MODULE2:-7}
XENA_SPEED=${XENA_SPEED:-10}
TRAFFIC_GEN=${TRAFFIC_GEN:-"xena"}
TREX_IP=${TREX_IP:-10.73.130.109}
TREX_USER=${TRAFFICGEN_TREX_USER:-root}
TREX_PATH=${TREX_PATH:-/root/trex-core/scripts/}
TREX_PORT1=${TREX_PORT1:-a0:36:9f:78:f5:58} 
TREX_PORT2=${TREX_PORT2:-a0:36:9f:78:f5:5a}
TREX_SPEED=${TREX_SPEED:-10}
TREX_LATENCY=${TREX_LATENCY:-1000}
TREX_THRESHOLD=${TREX_THRESHOLD:-0.05}
TREX_PORT_SPEED=${TREX_PORT_SPEED:-1000000}
TREX_FORCE_PORT_SPEED=${TREX_FORCE_PORT_SPEED:-True}
TREX_RFC2544_START_RATE=${TRAFFICGEN_TREX_RFC2544_START_RATE:-1}
LATENCY_START_VALUE=${LATENCY_START_VALUE:-'50'}
LATENCY_STEP_VALUE=${LATENCY_STEP_VALUE:-'50'}
LATENCY_END_VALUE=${LATENCY_END_VALUE:-'50'}
#OVS_URL=${OVS_URL:-http://download.devel.redhat.com/brewroot/packages/openvswitch/2.7.0/1.git20170516.el7fdb/x86_64/openvswitch-2.7.0-1.git20170516.el7fdb.x86_64.rpm}
#DPDK_HOST_URL=${DPDK_HOST_URL:-http://download.eng.pek2.redhat.com/brewroot/packages/dpdk/16.11/5.el7fdb/x86_64/dpdk-16.11-5.el7fdb.x86_64.rpm}
#DPDK_TOOL_HOST_URL=${DPDK_TOOL_HOST_URL:-http://download.eng.pek2.redhat.com/brewroot/packages/dpdk/16.11/5.el7fdb/x86_64/dpdk-tools-16.11-5.el7fdb.x86_64.rpm}
#DPDK_HOST_URL=${DPDK_HOST_URL:-http://download.devel.redhat.com/brewroot/packages/dpdk/16.11.2/4.el7/x86_64/dpdk-16.11.2-4.el7.x86_64.rpm}
#DPDK_TOOL_HOST_URL=${DPDK_TOOL_HOST_URL:-http://download.devel.redhat.com/brewroot/packages/dpdk/16.11.2/4.el7/x86_64/dpdk-tools-16.11.2-4.el7.x86_64.rpm}
OVS_URL=${OVS_URL:-http://download.devel.redhat.com/brewroot/packages/openvswitch/2.9.0/0.2.20171212git6625e43.el7fdb/x86_64/openvswitch-2.9.0-0.2.20171212git6625e43.el7fdb.x86_64.rpm}
DPDK_HOST_URL=${DPDK_HOST_URL:-http://download.devel.redhat.com/brewroot/packages/dpdk/17.11/2.el7fdb/x86_64/dpdk-17.11-2.el7fdb.x86_64.rpm}
DPDK_TOOL_HOST_URL=${DPDK_TOOL_HOST_URL:-http://download.devel.redhat.com/brewroot/packages/dpdk/17.11/2.el7fdb/x86_64/dpdk-tools-17.11-2.el7fdb.x86_64.rpm}
DPDK_GUEST_URL=${DPDK_GUEST_URL:-http://download.devel.redhat.com/brewroot/packages/dpdk/18.11.2/1.el7/x86_64/dpdk-18.11.2-1.el7.x86_64.rpm}
DPDK_TOOL_GUEST_URL=${DPDK_TOOL_GUEST_URL:-http://download.devel.redhat.com/brewroot/packages/dpdk/18.11.2/1.el7/x86_64/dpdk-tools-18.11.2-1.el7.x86_64.rpm}
Z_STREAM=${Z_STREAM:-""}
ISOLCPUS=${ISOLCPUS:-2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70}
#ISOLCPUS=${ISOLCPUS:-2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46}
GUEST_IMG=${GUEST_IMG:-"7.4"}
JOBID=$JOBID
TRAFFICGEN_GATING=${TRAFFICGEN_GATING:-"xena"}
TRAFFICGEN_NIGHTLY=${TRAFFICGEN_NIGHTLY:-"xena"}
TRAFFICGEN_WEEKLY=${TRAFFICGEN_WEEKLY:-"xena"}
RHEL=${RHEL:-"74"}
CUSTOM_CONF=${CUSTOM_CONF:-custom_conf}
#CUSTOM_CONF=${CUSTOM_CONF:-custom_conf_dell50}
VIOMMU=${VIOMMU:-"NO"}
OVS_TYPE=${OVS_TYPE:-"OVS_DPDK"}
image_method=${image_method:-"create"}
verification=${verification:-"yes"}
#guest_dpdk_version=${guest_dpdk_version:-"1711"}
PYTHON_ENV=${PYTHON_ENV:-"33"}
COMMIT=${COMMIT:-"yes"}
VANILLA_TGEN_PORT1_MAC=${VANILLA_TGEN_PORT1_MAC:-"3c:fd:fe:ad:bc:e8"}
VANILLA_TGEN_PORT2_MAC=${VANILLA_TGEN_PORT2_MAC:-"3c:fd:fe:ad:bc:e9"}
NIC1_MAC=${NIC1_MAC:-"00:15:4d:13:08:ad"}
NIC2_MAC=${NIC2_MAC:-"00:15:4d:13:08:ae"}
NetScout_nic1=${NetScout_nic1:-"Netqe23_p6p1"}
NetScout_nic2=${NetScout_nic2:-"Netqe23_p6p2"}
Trex_nic1=${Trex_nic1:-"Netqe23_p6p1"}
Trex_nic2=${Trex_nic2:-"Netqe23_p6p2"}
LOSSRATE=${LOSSRATE:-"0.0"}
cpu_custom=${cpu_custom:-"no"}
hugepage_num=${hugepage_num:-"48"}
copy_dpdk=${copy_dpdk:-"yes"}
selinux_policy_rpm=${selinux_policy_rpm:-"http://download.devel.redhat.com/brewroot/packages/openvswitch-selinux-extra-policy/1.0/3.el7fdp/noarch/openvswitch-selinux-extra-policy-1.0-3.el7fdp.noarch.rpm"}
rxq_assign=${rxq_assign:-"flase"}
nightly_viommu=${nightly_viommu:-"disable"}
NetScout_speed=${NetScout_speed:-10}
passwd=${passwd:-"QwAo2U6GRxyNPKiZaOCx"}
sriov_only=${sriov_only:-"no"}
RT_TEST=${RT_TEST:-"NO"}
QEMU_KVM_RHEV=${QEMU_KVM_RHEV:-"http://download.devel.redhat.com/brewroot/packages/qemu-kvm-rhev/2.12.0/41.el7/x86_64/qemu-kvm-rhev-2.12.0-41.el7.x86_64.rpm"}
QEMU_KVM_COMMON_RHEV=${QEMU_KVM_COMMON_RHEV:-"$(dirname $QEMU_KVM_RHEV)/qemu-kvm-common-rhev-$(basename $QEMU_KVM_RHEV | sed 's/^qemu-kvm-rhev-\(.*\)/\1/')"}
QEMU_IMG_RHEV=${QEMU_IMG_RHEV:-"$(dirname $QEMU_KVM_RHEV)/qemu-img-rhev-$(basename $QEMU_KVM_RHEV | sed 's/^qemu-kvm-rhev-\(.*\)/\1/')"}
QEMU_KVM_TOOLS_RHEV=${QEMU_KVM_TOOLS_RHEV:-"$(dirname $QEMU_KVM_RHEV)/qemu-kvm-tools-rhev-$(basename $QEMU_KVM_RHEV | sed 's/^qemu-kvm-rhev-\(.*\)/\1/')"}
