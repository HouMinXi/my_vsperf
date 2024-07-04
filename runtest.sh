#!/bin/bash
# Include Beaker environment
. /mnt/tests/kernel/networking/common/include.sh || exit 1

# source mem_set_baseline
. /mnt/tests/kernel/networking/openvswitch/common/ovs_mem_set_baseline.sh || exit 1

set -x

PACKAGE="kernel"
VSPERF="/root/vswitchperf/vsperf"
CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/common.sh
. /etc/os-release


run_one_time "install_python3_pkt"
run_one_time "install_googlesheet"
run_one_time "create_config"

if (($(bc <<< "$VERSION_ID >= 8"))); then
    bash ${CASE_PATH}/run_vsperf.sh
else
    scl enable rh-python36 "bash ${CASE_PATH}/run_vsperf.sh"
fi
