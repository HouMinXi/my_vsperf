#!/bin/bash


yum install -y virt-install libvirt
systemctl start libvirtd
yum install -y qemu-kvm

enforce_status=`getenforce`

setenforce permissive

SYS_ARCH=$(uname -m)
SERVER=download-node-02.eng.bos.redhat.com
ALT_FLAG=$(grep DISTRO /etc/motd | awk -F '=' '{print $2}' | awk -F '-' '{print $2}')
# we can only define the os-version in the same arch and kernel version.
OS_VERSION=${OS_VERSION:-"$(grep VERSION_ID /etc/os-release | awk -F '"' '{print $2}')"}
	
CPUS=3
DEBUG="NO"
VIOMMU="NO"
DPDK_BUILD="NO"

progname=$0

function usage () {
   cat <<EOF
Usage: $progname [-c cpus] [-l url to compose] [-v enable viommu] [-d debug output to screen]
	[-V OS Version Range 7.4 ~ 7.6] [-u enable use of upstream DPDK]
Example: ./vmcreate.sh -c 3 -l http://example.redhat.com/compose -v -d
	 ./vmcreate.sh -c 4 -V 7.6 -v -d
EOF
   exit 0
}

while getopts c:l:V:dhvu FLAG; do
   case $FLAG in

   c)  echo "Creating VM with $OPTARG cpus" 
       CPUS=$OPTARG
       ;;
   l)  echo "Using Location for VM install $OPTARG"
       DISTRO=$OPTARG
       ;;
   v)  echo "VIOMMU is enabled"
       VIOMMU="YES";;
   u)  echo "Building upstream DPDK"
       DPDK_BUILD="YES";;
   d)  echo "debug enabled" 
       DEBUG="YES";;
   V)  echo "The OS Version for VM install $OPTARG"
       OS_VERSION=$OPTARG
       ;;
   h)  echo "found $opt" ; usage ;;
   \?)  usage ;;
   esac
done


if [ "$ALT_FLAG" = "ALT" ];then
	release_branch=released/RHEL-ALT-7
else
	release_branch=released/RHEL-7
fi
case $OS_VERSION in
	7.2)	DISTRO=${DISTRO:-"http://$SERVER/$release_branch/$OS_VERSION/Server/$SYS_ARCH/os"}
			;;
	7.3)    DISTRO=${DISTRO:-"http://$SERVER/$release_branch/$OS_VERSION/Server/$SYS_ARCH/os"}
			;;
	7.4)	DISTRO=${DISTRO:-"http://$SERVER/$release_branch/$OS_VERSION/Server/$SYS_ARCH/os"}
			;;
	7.5)	DISTRO=${DISTRO:-"http://$SERVER/$release_branch/$OS_VERSION/Server/$SYS_ARCH/os"}
			;;
	7.6)	if [ "$ALT_FLAG" = "ALT" ];then
			release_branch=rel-eng/latest-RHEL-ALT
			DISTRO=${DISTRO:-"http://$SERVER/$release_branch-$OS_VERSION/compose/Server/$SYS_ARCH/os"}
		else
			release_branch=rel-eng/latest-RHEL
			DISTRO=${DISTRO:-"http://$SERVER/$release_branch-$OS_VERSION/compose/Server/$SYS_ARCH/os"}
		fi
			;;
	*)      echo "Not a valid OS Release Version" ;;
esac

#echo $CPUS
#echo $DISTRO
#echo $VIOMMU
#echo $DPDK_BUILD
#echo $DEBUG
#echo $OS_VERSION
#
## COnfig for vm location url
#echo $ALT_FLAG
#echo $release_branch
#echo $SYS_ARCH

shift $(($OPTIND - 1))

# vm config
vm=master
bridge=virbr0
master_image=master.qcow2
image_path=/var/lib/libvirt/images/
dist=rhel$OS_VERSION
location=$DISTRO

extra="ks=file:/$dist-vm.ks console=ttyS0,115200"

master_exists=`virsh list --all | awk '{print $2}' | grep master`
if [ -z $master_exists ]; then
    master_exists='None'
fi

if [ $master_exists == "master" ]; then
    virsh destroy $vm
    virsh undefine $vm
fi

echo deleting master image
/bin/rm -f $image_path/$master_image

cat << KS_CFG > $dist-vm.ks
# System authorization information
auth --enableshadow --passalgo=sha512

# Use network installation
url --url=$location

# Use text mode install
text
# Run the Setup Agent on first boot
firstboot --enable
ignoredisk --only-use=vda
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

# Network information
network  --bootproto=dhcp --device=eth0 --ipv6=auto --activate
# Root password
rootpw  redhat
# Do not configure the X Window System
skipx
# System timezone
timezone US/Eastern --isUtc --ntpservers=10.16.31.254,clock.util.phx2.redhat.com,clock02.util.phx2.redhat.com
# System bootloader configuration
bootloader --location=mbr --timeout=5 --append="crashkernel=auto rhgb quiet console=ttyS0,115200"
# Partition clearing information
autopart --type=plain
clearpart --all --initlabel --drives=vda
zerombr

%packages
@base
@core
@network-tools
%end

%post
cat >/etc/yum.repos.d/beaker-Server.repo <<REPO
[beaker-Server]
name=beaker-Server
baseurl=$location
enabled=1
gpgcheck=0
skip_if_unavailable=1
REPO

cat > /etc/yum.repos.d/beaker-tasks.repo << REPO
[beaker-tasks]
name=beaker-tasks
baseurl=http://beaker.engineering.redhat.com/rpms/
enabled=1
gpgcheck=0
skip_if_unavailable=1
REPO

yum install -y tuna git nano ftp wget sysstat 1>/root/post_install.log 2>&1
git clone https://github.com/ctrautma/vmscripts.git /root/vmscripts 1>/root/post_install.log 2>&1
mv /root/vmscripts/* /root/. 1>/root/post_install.log 2>&1
rm -Rf /root/vmscripts 1>/root/post_install.log 2>&1
sed -i "s/intel_iommu=on/intel_iommu=on iommu=pt/g" /root/setup_rpms.sh
if [ "$VIOMMU" == "NO" ] && [ "$DPDK_BUILD" == "NO" ]; then
    /root/setup_rpms.sh 1>/root/post_install.log 2>&1
elif [ "$VIOMMU" == "YES" ] && [ "$DPDK_BUILD" == "NO" ]; then
    /root/setup_rpms.sh -v 1>/root/post_install.log 2>&1
elif [ "$VIOMMU" == "NO" ] && [ "$DPDK_BUILD" == "YES" ]; then
    /root/setup_rpms.sh -u 1>/root/post_install.log 2>&1
elif [ "$VIOMMU" == "YES" ] && [ "$DPDK_BUILD" == "YES" ]; then
    /root/setup_rpms.sh -u -v 1>/root/post_install.log 2>&1
fi

%end

shutdown

KS_CFG

echo creating new master image
qemu-img create -f qcow2 $image_path/$master_image 100G
echo undefining master xml
virsh list --all | grep master && virsh undefine master
echo calling virt-install

if [ $DEBUG == "YES" ]; then
virt-install --name=$vm\
	 --virt-type=kvm\
	 --disk path=$image_path/$master_image,format=qcow2,,size=3,bus=virtio\
	 --vcpus=$CPUS\
	 --ram=4096\
	 --network bridge=$bridge\
	 --graphics none\
	 --extra-args="$extra"\
	 --initrd-inject=$dist-vm.ks\
	 --location=$location\
	 --noreboot\
         --serial pty\
         --serial file,path=/tmp/$vm.console
else
virt-install --name=$vm\
         --virt-type=kvm\
         --disk path=$image_path/$master_image,format=qcow2,,size=3,bus=virtio\
         --vcpus=$CPUS\
         --ram=4096\
         --network bridge=$bridge\
         --graphics none\
         --extra-args="$extra"\
         --initrd-inject=$dist-vm.ks\
         --location=$location\
         --noreboot\
         --serial pty\
         --serial file,path=/tmp/$vm.console &> vminstaller.log
fi

rm $dist-vm.ks

setenforce $enforce_status
