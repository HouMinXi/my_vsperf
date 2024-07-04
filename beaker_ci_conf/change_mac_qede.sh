#!/bin/sh

if ifconfig $1_1; then
    mac1=$(ifconfig $1_1|grep ether|awk '{print $2}')
    mac2=$(ifconfig $2_1|grep ether|awk '{print $2}')
    if [ $mac1 == "00:00:00:00:00:00" ];then
        mac1="52:54:00:00:00:01"
        mac2="52:54:00:00:00:02"
    fi
    ip link set $1 vf 1 mac $mac1 trust on
    ip link set $2 vf 1 mac $mac2 trust on
elif ifconfig "$1v1"; then
    mac1=$(ifconfig $1v1|grep ether|awk '{print $2}')
    mac2=$(ifconfig $2v1|grep ether|awk '{print $2}')
    if [ $mac1 == "00:00:00:00:00:00" ];then
        mac1="52:54:00:00:00:01"
        mac2="52:54:00:00:00:02"
    fi
    ip link set $1 vf 1 mac $mac1 trust on
    ip link set $2 vf 1 mac $mac2 trust on
else
    echo "FAIELD! the sriov nic name don't like nic_1 or nicv0"
fi
