source /mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI/env.sh
if [ "$QCOW_LOC" == "China" ]
    then
    SERVER="netqe-bj.usersys.redhat.com/share/tools"
elif [ "$QCOW_LOC" == "Westford" ]
    then
    SERVER="netqe-infra01.knqe.eng.rdu2.dc.redhat.com/mono_rpm_rhel8"
fi


PKG_MONO_SRC=${PKG_MONO_SRC:-"http://${SERVER}/mono-5.8.0.127.src.tar.bz2"}
PKG_LIBGDIPLUS_SRC=${PKG_LIBGDIPLUS_SRC:-"http://${SERVER}/libgdiplus_20181012.src.zip"}
PKG_MONO_AFTER_MAKE=${PKG_MONO_AFTER_MAKE:-"http://${SERVER}/mono-5.8.0.127.rhel8.tar.tgz"}
PKG_LIBGDIPLUS_AFTER_MAKE=${PKG_LIBGDIPLUS_AFTER_MAKE:-"http://${SERVER}/libgdiplus_20181012.rhel8.tar.tgz"}

yum install -y http://download.devel.redhat.com/brewroot/packages/giflib/5.1.4/2.el8/x86_64/giflib-5.1.4-2.el8.x86_64.rpm

install_mono_from_src()
{
    (
      echo [latest-RHEL8-AppStream]
      echo name=AppStream
      echo baseurl=http://download.eng.pek2.redhat.com/pub/rhel/rel-eng/latest-RHEL-8.%2A/compose/AppStream/x86_64/os/
      echo enabled=1
      echo gpgcheck=0
      echo skip_if_unavailable=1
    ) > /etc/yum.repos.d/rhel8_AppStream.repo

    rpm -q cmake &>/dev/null || yum -y install cmake
    rpm -q cairo-devel &/dev/null || yum -y install cairo-devel
    rpm -q libjpeg-turbo-devel &>/dev/null || yum -y install libjpeg-turbo-devel
    rpm -q libtiff-devel &>/dev/null || yum -y install libtiff-devel
    rpm -q giflib-devel &>/dev/null || yum -y install giflib-devel

    mkdir -p libgdiplus
    pushd libgdiplus &>/dev/null
    unzip *.zip
    pushd libgdiplus-*/ &>/dev/null
    ./autogen.sh 
    make -j 8
    make install
    popd &>/dev/null
    popd &>/dev/null

    mkdir -p mono
    pushd mono &>/dev/null
    wget ${PKG_MONO_SRC}
    tar xvf mono-*.tar.bz2 
    pushd mono-*/ &>/dev/null
    ./configure 
    make -j 8
    make install
    popd &>/dev/null
    popd &>/dev/null
}

install_mono_without_rebuild()
{
    (
      echo [latest-RHEL8-AppStream]
      echo name=AppStream
      echo baseurl=http://download.eng.pek2.redhat.com/pub/rhel/rel-eng/latest-RHEL-8.%2A/compose/AppStream/x86_64/os/
      echo enabled=1
      echo gpgcheck=0
      echo skip_if_unavailable=1
    ) > /etc/yum.repos.d/rhel8_AppStream.repo

    rpm -q cmake &>/dev/null || yum -y install cmake
    rpm -q cairo-devel &/dev/null || yum -y install cairo-devel
    rpm -q libjpeg-turbo-devel &>/dev/null || yum -y install libjpeg-turbo-devel
    rpm -q libtiff-devel &>/dev/null || yum -y install libtiff-devel
    rpm -q giflib-devel &>/dev/null || yum -y install giflib-devel

    [ -f $(basename ${PKG_LIBGDIPLUS_AFTER_MAKE}) ] || wget ${PKG_LIBGDIPLUS_AFTER_MAKE}
    mkdir -p /root/libgdiplus/
    tar xvf $(basename ${PKG_LIBGDIPLUS_AFTER_MAKE}) -C /root/libgdiplus/

    [ -f $(basename ${PKG_MONO_AFTER_MAKE}) ] || wget ${PKG_MONO_AFTER_MAKE}
    mkdir -p /root/mono/
    tar xvf $(basename ${PKG_MONO_AFTER_MAKE}) -C /root/mono/

    pushd /root/libgdiplus &>/dev/null
    pushd libgdiplus-*/ &>/dev/null
    make install
    popd &>/dev/null
    popd &>/dev/null

    pushd /root/mono &>/dev/null
    pushd mono-*/ &>/dev/null
    make install
    popd &>/dev/null
    popd &>/dev/null
}
