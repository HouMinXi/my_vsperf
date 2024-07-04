import sys
import os
from csv_help import get_rx_pps,get_min_latency,get_max_latency,get_avg_latency,get_avg_pmd
import config

def get_pps_novlan(pkt_size,custom_type):
    title_list = ['1k flows', 'SR-IOV', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/weekly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_novlan(pkt_size,custom_type):
    title_list = [' ', 'SR-IOV', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min')
    min_latency_result_list.append(get_min_latency('/tmp/weekly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max')
    max_latency_result_list.append(get_max_latency('/tmp/weekly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_'+ config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg')
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_novlan(pkt_size,custom_type):
    title_list = ['1k flows','1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_testpmd_as_switch(pkt_size):
    title_list = ['1k flows', 'TESTPMD as a switch']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/weekly_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) +'_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_testpmd_as_switch(pkt_size):
    title_list = ['1k flows', 'TESTPMD as a switch']
    min_latency_result_list = []
    min_latency_result_list.append('latency min')
    min_latency_result_list.append(get_min_latency('/tmp/weekly_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max')
    max_latency_result_list.append(get_max_latency('/tmp/weekly_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg')
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pps1(pkt_size,custom_type):
    title_list = ['1k flows', '', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    result_list = []
    result_list.append('fps')
    result_list.append('')
    result_list.append(get_rx_pps('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency1(pkt_size,custom_type):
    title_list = [' ', '', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min')
    min_latency_result_list.append('')
    min_latency_result_list.append(get_min_latency('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max')
    max_latency_result_list.append('')
    max_latency_result_list.append(get_max_latency('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg')
    avg_latency_result_list.append('')
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd1(pkt_size,custom_type):
    title_list = ['1k flows','1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/weekly_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/weekly_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/weekly_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    result = [title_list, pmd_result_list]
    return result
