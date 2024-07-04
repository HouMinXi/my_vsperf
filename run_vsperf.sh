#!/bin/bash
# Include Beaker environment
. /mnt/tests/kernel/networking/common/include.sh || exit 1
CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/common.sh
# nic_info come from /networking/common/include.sh
# source ${CASE_PATH}/nic_info.conf

PACKAGE="kernel"
VSPERF="/root/vswitchperf/vsperf"

upload=${upload:- 'no'}
upload=$(echo "$upload" | awk '{print tolower($0)}')

function upload_results(){
    sheetId=$1
    rhel_version=$(cut -f1 -d. /etc/redhat-release | sed 's/[^0-9]//g')
	if [[ $rhel_version == 8 ]]; then
    	    pip3 install --upgrade google-api-python-client oauth2client
	else
    	    easy_install pip
    	    pip install --upgrade google-api-python-client oauth2client
 	fi

    git clone https://github.com/AmitSupugade/ovsqe_results.git
    cd ovsqe_results
    wget http://netqe-infra01.knqe.eng.rdu2.dc.redhat.com/ovs_offload/token.json
    wget http://netqe-infra01.knqe.eng.rdu2.dc.redhat.com/ovs_offload/client_secret.json
    if [ ${RUN_JOB} == "gating" ];then
        python3 GatingReport.py --sheet=$sheetId
    elif [ ${RUN_JOB} == "nightly" ];then
        python3 VSPerf.py --sheet=$sheetId
    fi
}

rlJournalStart
rlPhaseStartSetup
#the pyzmp install failed for requirements.txt in rhel8.1, need run again before vsperf case
rlRun "pip3 install pyzmq"
rlRun "yum install -y numactl"
rlRun "sh ${CASE_PATH}/${RUN_JOB}_ci.sh"

source /tmp/googlesheet_id
echo "The googlesheet result link is https://docs.google.com/spreadsheets/d/$googlesheet_id" >> ${CASE_PATH}/vsperf.txt

#To upload results to nightly report sheet
if [ $upload == 'yes' ]; then
    upload_results $googlesheet_id
fi

rlRun "sos_report"
rlPhaseEnd
rlJournalPrintText
rlJournalEnd
