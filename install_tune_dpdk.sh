#!/bin/bash
. /mnt/tests/kernel/networking/common/include.sh || exit 1
CASE_PATH="/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI"
source ${CASE_PATH}/env.sh
source ${CASE_PATH}/nic_info.conf
. /etc/os-release

result_pass(){
if [ $? -ne 0 ];then
	echo "run function failed"
	exit 1
fi
}

install_utilities() {
if (($(bc <<< "$VERSION_ID >= 8"))); then
    rpm -ivh http://download.devel.redhat.com/brewroot/packages/tuna/0.13.3/4.el8+7/noarch/tuna-0.13.3-4.el8+7.noarch.rpm
    yum install -y wget nano ftp yum-utils git openssl libpcap sysstat
else
    yum install -y wget nano ftp yum-utils git tuna openssl libpcap sysstat
fi
result_pass
}

install_tuned() {
if [ "$QCOW_LOC" == "China" ]
    then
    SERVER="download.eng.pnq.redhat.com"
elif [ "$QCOW_LOC" == "Westford" ]
    then
    SERVER="download-node-02.eng.bos.redhat.com"
fi

mkdir ~/tuned27 ~/tuned28
wget http://$SERVER/brewroot/packages/tuned/2.7.1/5.el7fdb/noarch/tuned-2.7.1-5.el7fdb.noarch.rpm -P ~/tuned27/.
wget http://$SERVER/brewroot/packages/tuned/2.7.1/5.el7fdb/noarch/tuned-profiles-cpu-partitioning-2.7.1-5.el7fdb.noarch.rpm -P ~/tuned27/.
wget http://$SERVER/brewroot/packages/tuned/2.7.1/5.el7fdb/noarch/tuned-profiles-nfv-2.7.1-5.el7fdb.noarch.rpm -P ~/tuned27/.
wget http://$SERVER/brewroot/packages/tuned/2.7.1/5.el7fdb/noarch/tuned-profiles-realtime-2.7.1-5.el7fdb.noarch.rpm -P ~/tuned27/.

wget http://$SERVER/brewroot/packages/tuned/2.8.0/2.el7fdp/noarch/tuned-2.8.0-2.el7fdp.noarch.rpm  -P ~/tuned28/.
wget http://$SERVER/brewroot/packages/tuned/2.8.0/2.el7fdp/noarch/tuned-profiles-cpu-partitioning-2.8.0-2.el7fdp.noarch.rpm -P ~/tuned28/.
wget http://$SERVER/brewroot/packages/tuned/2.8.0/2.el7fdp/noarch/tuned-profiles-realtime-2.8.0-2.el7fdp.noarch.rpm -P ~/tuned28/.
wget http://$SERVER/brewroot/packages/tuned/2.8.0/2.el7fdp/noarch/tuned-profiles-nfv-2.8.0-2.el7fdp.noarch.rpm -P ~/tuned28/.
wget http://$SERVER/brewroot/packages/tuned/2.8.0/2.el7fdp/noarch/tuned-profiles-nfv-guest-2.8.0-2.el7fdp.noarch.rpm -P ~/tuned28/.
wget http://$SERVER/brewroot/packages/tuned/2.8.0/2.el7fdp/noarch/tuned-profiles-nfv-host-2.8.0-2.el7fdp.noarch.rpm -P ~/tuned28/.

:<<!
if [ "$TUNED_VER" == "27" ]
    then
        rpm -Uvh ~/tuned27/tuned-2.7.1-5.el7fdb.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
        rpm -Uvh ~/tuned27/tuned-profiles-realtime-2.7.1-5.el7fdb.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
        rpm -Uvh ~/tuned27/tuned-profiles-nfv-2.7.1-5.el7fdb.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
        rpm -Uvh ~/tuned27/tuned-profiles-cpu-partitioning-2.7.1-5.el7fdb.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
elif [ "$TUNED_VER" == "28" ]
    then
        rpm -Uvh ~/tuned28/tuned-2.8.0-5.el7.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
	rpm -Uvh ~/tuned28/tuned-profiles-realtime-2.8.0-5.el7.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
	rpm -Uvh ~/tuned28/tuned-profiles-nfv-2.8.0-5.el7.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
        rpm -Uvh ~/tuned28/tuned-profiles-cpu-partitioning-2.8.0-5.el7.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
	rpm -Uvh ~/tuned28/tuned-profiles-nfv-guest-2.8.0-5.el7.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
	rpm -Uvh ~/tuned28/tuned-profiles-nfv-host-2.8.0-5.el7.noarch.rpm --nodeps >> ${CASE_PATH}/tuned_install.log
fi
!
. /etc/os-release

if [ $VERSION_ID == "7.4" ] || [ $VERSION_ID == "7.3" ]
then
	rpm -e tuned-2.8.0-5.el7.noarch
	rpm -Uvh ~/tuned28/tuned-2.8.0-2.el7fdp.noarch.rpm
	rpm -ivh ~/tuned28/tuned-profiles-realtime-2.8.0-2.el7fdp.noarch.rpm
	rpm -ivh ~/tuned28/tuned-profiles-nfv-2.8.0-2.el7fdp.noarch.rpm
	rpm -ivh ~/tuned28/tuned-profiles-cpu-partitioning-2.8.0-2.el7fdp.noarch.rpm
else
	yum install -y tuned-profiles-cpu-partitioning tuned-profiles-nfv
fi
result_pass
}

add_osp_profile() {

cat <<EOT >> /etc/yum.repos.d/osp8-rhel.repo
[osp8-rhel7]
name=osp8-rhel7
baseurl=http://download.lab.bos.redhat.com/rel-eng/OpenStack/8.0-RHEL-7/latest/RH7-RHOS-8.0/x86_64/os/
enabled=1
gpgcheck=0
skip_if_unavailable=1
EOT

result_pass

}


identify_isolcpus() {

# Isolated CPU list
NICNUMA=`cat /sys/class/net/$NIC1/device/numa_node`
ISOLCPUS=`lscpu | grep "NUMA node$NICNUMA" | awk '{print $4}'`

if [ `echo $ISOLCPUS | awk /'^0,'/` ]; then
# NUMA node0 CPU(s):   0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46
    ISOLCPUS=`echo $ISOLCPUS | cut -c 3-`
# NUMA node0 CPU(s):   0-19
elif [ `echo $ISOLCPUS | awk /'^0-'/` ]; then
    ISOLCPUS=`echo $ISOLCPUS | awk '{sub(/^0/,"1"); print $1}'`
#echo "ISOLCPUS  = $ISOLCPUS"
fi

result_pass

}

configure_hugepages() {
#config the hugepage
. /etc/os-release
OS_NAME="$VERSION_ID"
if (($(bc <<< "$VERSION_ID < 8"))); then
sed -i 's/\(GRUB_CMDLINE_LINUX.*\)"$/\1/g' /etc/default/grub
if [ ${NIC_DRIVER} == "qede" ];then
sed -i "s/GRUB_CMDLINE_LINUX.*/& nohz=on mitigations=off default_hugepagesz=1G hugepagesz=1G hugepages=${hugepage_num} intel_iommu=on iommu=pt modprobe.blacklist=qedi modprobe.blacklist=qedf modprobe.blacklist=qedr \"/g" /etc/default/grub
else
sed -i "s/GRUB_CMDLINE_LINUX.*/& nohz=on mitigations=off default_hugepagesz=1G hugepagesz=1G hugepages=${hugepage_num} intel_iommu=on iommu=pt \"/g" /etc/default/grub
fi
if [ `hostname | grep -P hpe-netqe-syn480g10-0[0-9]+.knqe.lab.eng.bos.redhat.com` ];then
        grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
else
         grub2-mkconfig -o /boot/grub2/grub.cfg
fi
else
:<<BLOCK
kernelopts=$(grub2-editenv - list | grep kernelopts | sed -e 's/kernelopts=//g')
if [ ${NIC_DRIVER} == "qede" ];then
grub2-editenv - set kernelopts="$kernelopts intel_iommu=on iommu=pt default_hugepagesz=1GB hugepagesz=1G hugepages=${hugepage_num} modprobe.blacklist=qedi modprobe.blacklist=qedf modprobe.blacklist=qedr"
else
grub2-editenv - set kernelopts="$kernelopts intel_iommu=on iommu=pt default_hugepagesz=1GB hugepagesz=1G hugepages=${hugepage_num}"
fi
cat /boot/grub2/grubenv
BLOCK
sed -i "s/GRUB_ENABLE_BLSCFG/#GRUB_ENABLE_BLSCFG/g" /etc/default/grub
sed -i 's/\(GRUB_CMDLINE_LINUX.*\)"$/\1/g' /etc/default/grub
sed -i "s/GRUB_CMDLINE_LINUX.*/& nohz=on isolcpus='"$ISOLCPUS"' default_hugepagesz=1G hugepagesz=1G hugepages=${hugepage_num} intel_iommu=on iommu=pt modprobe.blacklist=qedi modprobe.blacklist=qedf modprobe.blacklist=qedr \"/g" /etc/default/grub
#sed -i "s/GRUB_CMDLINE_LINUX.*/& nohz=on isolcpus='"2-23,26-47"' default_hugepagesz=1G hugepagesz=1G hugepages=${hugepage_num} intel_iommu=on iommu=pt modprobe.blacklist=qedi modprobe.blacklist=qedf modprobe.blacklist=qedr \"/g" /etc/default/grub
if [ `hostname | grep -P hpe-netqe-syn480g10-0[0-9]+.knqe.lab.eng.bos.redhat.com` ];then
	grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg	
else
	 grub2-mkconfig -o /boot/grub2/grub.cfg
fi
fi
echo -e "isolated_cores=$ISOLCPUS" >> /etc/tuned/cpu-partitioning-variables.conf
#echo -e "isolated_cores=2-23,26-47" >> /etc/tuned/realtime-virtual-host-variables.conf
echo -e "isolate_managed_irq=Y" >> /etc/tuned/realtime-virtual-host-variables.conf
tuned-adm profile virtual-host
systemctl stop irqbalance.service
chkconfig irqbalance off
/usr/sbin/swapoff -a
result_pass

}

rlJournalStart
rlPhaseStartSetup
rlRun "install_utilities"
rlRun "install_tuned"
rlRun "add_osp_profile"
rlRun "identify_isolcpus"
rlRun "configure_hugepages"
rlPhaseEnd
rlJournalEnd
