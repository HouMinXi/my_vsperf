#!/usr/bin/python
import csv
import os
import sys
import config

def get_rx_var_name(pkt_size, loss_rate):
    return 'baseline_FPS_RX_' + pkt_size + 'B_' + loss_rate

def get_rx_var(var_name, uuid):
    csvReader = csv.reader(open('/mnt/tests/kernel/networking/rt-kernel/vsperf/vsperf_CI/report/baseline.csv', 'rb'))
    row = col = 0
    rlt = None
    for i in csvReader:
        if row == 0:
            firstline = i
        if i[1] != uuid:
            row += 1
        else:
            rlt = i
            break

    for i in firstline:
        if i != var_name:
            col += 1
        else:
            break

    return rlt[col]

#get the tx pps
def get_tx_pps(path, param, gen_type):

    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $2}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $2}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $2}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $4}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $4}'").read()
    
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $2}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $2}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $2}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $4}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $4}'").read()
 
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $2}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $2}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $2}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $4}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        tx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $4}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        tx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $4}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        tx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $4}'").read()

    return tx

#get the rx pps
def get_rx_pps(path, param, gen_type):
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $1}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $1}'").read()
    
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $1}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $1}'").read()

    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $1}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $1}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        rx=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $1}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $1}'").read()

    return rx

#get the min latency
def get_min_latency(path, param, gen_type):
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $13}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $13}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $13}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $7}'").read()
  
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $13}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $13}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $13}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $7}'").read() 
    
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $13}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $13}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $13}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $7}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        min_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $7}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $7}'").read()

    return min_latency


#get the max latency
def get_max_latency(path, param, gen_type):

    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $14}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $14}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $14}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $8}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $8}'").read()
    
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $14}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $14}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $14}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $8}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $8}'").read()
    
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $14}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $14}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $14}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $8}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $8}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        max_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $8}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $8}'").read()
    
    return max_latency


#get the avg latency
def get_avg_latency(path, param, gen_type):

    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $15}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $15}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $15}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $9}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'nightly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $9}'").read()
   
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $15}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $15}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $15}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $9}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'weekly' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $9}'").read()

    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_cont_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $15}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvp_tput_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_cont_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $15}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_phy2phy_tput_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $15}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'xena':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_cont_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_cont | awk -F ',' '{print $9}'").read()
    if param == 'pvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvp_tput_pvp.csv'
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_cont_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_cont | awk -F ',' '{print $9}'").read()
    if param == 'phy2phy_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_phy2phy_tput_p2p.csv'
        avg_latency=os.popen("cat "+path+"| grep phy2phy_tput | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_cont' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_cont_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_cont | awk -F ',' '{print $9}'").read()
    if param == 'pvvp_tput' and config.RUN_JOB == 'gating' and gen_type == 'moongen':
        path = path + 'result_pvvp_tput_pvvp.csv'
        rx=os.popen("cat "+path+"| grep pvvp_tput | awk -F ',' '{print $9}'").read()    

    
    return avg_latency


def get_data(queue_dict, param_dict, gen_type):
    rlt = {}

    for k,v in queue_dict.iteritems():
        path = "/tmp/" + v + '/result*/'
        param = param_dict[k]
        if k.find("FPS_TX") >= 0:
            if get_tx_pps(path, param, gen_type).strip() == '':
                rlt[k] = 0
            else:
                rlt[k] = round(float(get_tx_pps(path, param, gen_type).strip()) / 1000000, 6)
        elif k.find("FPS_RX") >= 0:
            if get_rx_pps(path, param, gen_type).strip() == '':
                rlt[k] = 0
            else:
                rlt[k] = round(float(get_rx_pps(path, param, gen_type).strip()) / 1000000, 6)
        elif k.find("MIN_LATENCY") >= 0:
            if get_min_latency(path, param, gen_type).strip() == '':
                rlt[k] = 0
            else:
                rlt[k] = round(float(get_min_latency(path, param, gen_type).strip()) / 1000, 6)
        elif k.find("MAX_LATENCY") >= 0:
            if get_max_latency(path, param, gen_type).strip() == '':
                rlt[k] = 0
            else:
                rlt[k] = round(float(get_max_latency(path, param, gen_type).strip()) / 1000, 6)
        elif k.find("AVG_LATENCY") >= 0:
            if get_avg_latency(path, param, gen_type).strip() == '':
                rlt[k] = 0
            else:
                rlt[k] = round(float(get_avg_latency(path, param, gen_type).strip()) / 1000, 6)
    return rlt
