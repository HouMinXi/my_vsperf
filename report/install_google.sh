#!/bin/sh
CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
yum install -y wget

install_pip() {
    #wget "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz#md5=834b2904f92d46aaa333267fb1c922bb" --no-check-certificate
    wget https://files.pythonhosted.org/packages/69/81/52b68d0a4de760a2f1979b0931ba7889202f302072cc7a0d614211bc7579/pip-18.0.tar.gz 
    tar -xzvf pip-18.0.tar.gz >> ${CASE_PATH}/pip_install.log
    pushd pip-18.0
    /usr/bin/python2 ./setup.py install >> ${CASE_PATH}/pip_install.log
    popd
}

echo "start install pip latest version"
install_pip

python2 -m pip install --upgrade google-api-python-client >> ${CASE_PATH}/pip_install.log
python2 -m pip install oauth2client >> ${CASE_PATH}/pip_install.log
mkdir -p /root/.credentials
#wget -P /root/.credentials/ http://netqe-infra01.knqe.eng.rdu2.dc.redhat.com/sheets.googleapis.com-python-quickstart.json
\cp /mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI/report/sheets.googleapis.com-python-quickstart.json /root/.credentials/
