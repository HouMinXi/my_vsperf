#!/usr/bin/python
import csv
import os
import sys

#get the rx pps
def get_rx_pps(path, param, gen_type):
    if param == 'pvp_tput' and gen_type == 'trex':
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $4}'").read()
    if param == 'pvp_tput' and gen_type == 'xena':
        rx=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $1}'").read()

    return rx

#get the min latency
def get_min_latency(path, param, gen_type):
    if param == 'pvp_tput' and gen_type == 'trex':
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $10}'").read()
    if param == 'pvp_tput' and gen_type == 'xena':
        min_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $7}'").read()

    return min_latency


#get the max latency
def get_max_latency(path, param, gen_type):

    if param == 'pvp_tput' and gen_type == 'trex':
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $11}'").read()
    if param == 'pvp_tput' and gen_type == 'xena':
        max_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $8}'").read()
    
    return max_latency


#get the avg latency
def get_avg_latency(path, param, gen_type):

    if param == 'pvp_tput' and gen_type == 'trex':
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $12}'").read()
    if param == 'pvp_tput' and gen_type == 'xena':
        avg_latency=os.popen("cat "+path+"| grep pvp_tput | awk -F ',' '{print $9}'").read()

    
    return avg_latency

def get_min_latency_half(path, param, gen_type):
    if param == 'pvp_latency' and gen_type == 'trex':
        min_latency=os.popen("cat "+path+"| grep pvp_latency | awk -F ',' '{print $1}'").read()
    if param == 'pvp_latency' and gen_type == 'xena':
        min_latency=os.popen("cat "+path+"| grep pvp_latency | awk -F ',' '{print $1}'").read()

    return min_latency

def get_max_latency_half(path, param, gen_type):
    if param == 'pvp_latency' and gen_type == 'trex':
        max_latency=os.popen("cat "+path+"| grep pvp_latency | awk -F ',' '{print $2}'").read()
    if param == 'pvp_latency' and gen_type == 'xena':
        max_latency=os.popen("cat "+path+"| grep pvp_latency | awk -F ',' '{print $2}'").read()

    return max_latency

def get_avg_latency_half(path, param, gen_type):
    if param == 'pvp_latency' and gen_type == 'trex':
        avg_latency=os.popen("cat "+path+"| grep pvp_latency | awk -F ',' '{print $3}'").read()
    if param == 'pvp_latency' and gen_type == 'xena':
        avg_latency=os.popen("cat "+path+"| grep pvp_latency | awk -F ',' '{print $3}'").read()

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

def get_avg_pmd(path):
    path = path + '/pmd.log'
    avg_pmd = os.popen("cat "+path+"|grep 'avg processing cycles per packet'|awk '{print $6}'|awk 'BEGIN{sum=0;num=0}{sum+=$1;num+=1}END{print sum/num}'").read()
    return avg_pmd
    
