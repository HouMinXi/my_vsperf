import sys
import os
import config
from csv_help import get_rx_pps,get_min_latency,get_max_latency,get_avg_latency,get_avg_pmd


def get_pps(pkt_size):
    title_list = [ pkt_size + ' Bytes 1k flows', 'SR-IOV Passthrough', 'OVS-DPDK 2 PMD', 'OVS-DPDK 4 PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/nightly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency(pkt_size):
    title_list = [ pkt_size + ' Bytes 1k flows',  'SR-IOV Passthrough', 'OVS-DPDK 2 PMD', 'OVS-DPDK 4 PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min')
    min_latency_result_list.append(get_min_latency('/tmp/nightly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max')
    max_latency_result_list.append(get_max_latency('/tmp/nightly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg')
    avg_latency_result_list.append(get_avg_latency('/tmp/nightly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd(pkt_size):
    title_list = [ pkt_size + ' Bytes 1k flows',  '', 'OVS-DPDK 2 PMD', 'OVS-DPDK 4 PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append('')
    pmd_result_list.append((get_avg_pmd('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN)).strip())
    pmd_result_list.append((get_avg_pmd('/tmp/nightly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN)).strip())
    result = [title_list,pmd_result_list]
    return result
