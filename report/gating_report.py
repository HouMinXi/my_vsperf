import sys
import os
from csv_help import get_rx_pps,get_min_latency,get_max_latency,get_avg_latency,get_avg_pmd,get_max_latency_half,get_min_latency_half,get_avg_latency_half
import config

def get_pps_iommu(pkt_size,custom_type):
    title_list = ['1k flows', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_iommu(pkt_size,custom_type):
    title_list = [' ', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_iommu(pkt_size,custom_type):
    title_list = ['1k flows', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    result = [title_list, pmd_result_list]
    return result


def get_pps_testpmd_as_switch(pkt_size):
    title_list = ['1k flows', 'TESTPMD as a switch']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) +'_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_testpmd_as_switch(pkt_size):
    title_list = ['1k flows', 'TESTPMD as a switch']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_testpmd_as_switch(pkt_size):
    title_list = ['1k flows', 'TESTPMD as a switch']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_baseline_testpmd_as_switch_pvp_tput_' + str(pkt_size) +'_0.00_' + config.TRAFFIC_GEN).strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_vlan(pkt_size,custom_type):
    title_list = ['1k flows', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_vlan(pkt_size,custom_type):
    title_list = [' ', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_vlan(pkt_size,custom_type):
    title_list = ['1k flows', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_novlan_64and1500(pkt_size,custom_type):
    title_list = ['1k flows', 'SR-IOV', '1Q 2PMD','1Q 4PMD', '2Q 4PMD', '4Q 8PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_'+ config.TRAFFIC_GEN +'_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_novlan_64and1500(pkt_size,custom_type):
    title_list = [' ', 'SR-IOV', '1Q 2PMD', '1Q 4PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_'+ config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_'+ custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_'+ config.TRAFFIC_GEN +'_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_'+ config.TRAFFIC_GEN +'_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_'+ config.TRAFFIC_GEN +'_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_novlan_64and1500(pkt_size,custom_type):
    title_list = ['1k flows', '', '1Q 2PMD','1Q 4PMD', '2Q 4PMD', '4Q 8PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append('')
    pmd_result_list.append((get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type)).strip())
    pmd_result_list.append((get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type)).strip())
    pmd_result_list.append((get_avg_pmd('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type)).strip())
    pmd_result_list.append((get_avg_pmd('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type)).strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_novlan_128and256(pkt_size,custom_type):
    title_list = ['1k flows', 'SR-IOV','1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_'+ config.TRAFFIC_GEN +'_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_novlan_128and256(pkt_size,custom_type):
    title_list = [' ', 'SR-IOV', '1Q 2PMD','2Q 4PMD', '4Q 8PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_'  + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' +  custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_baseline_guest_pvp_tput_' + str(pkt_size) + '_0.00_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_novlan_128and256(pkt_size,custom_type):
    title_list = ['1k flows', '','1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append('')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_jumbo(pkt_size,custom_type):
    title_list = ['1k flows', '1Q 2PMD', '1Q 4PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_jumbo(pkt_size,custom_type):
    title_list = [' ', '1Q 2PMD', '1Q 4PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_'+ custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_jumbo(pkt_size,custom_type):
    title_list = ['1k flows', '1Q 2PMD', '1Q 4PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type).strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_highflows(pkt_size):
    title_list = ['1Q 2PMD', '10k Flows', '100k Flows', '1 million Flows']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_10kflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_100kflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_1mflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_highflows(pkt_size):
    title_list = ['', '10k Flows', '100k Flows', '1 million Flows']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_10kflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_100kflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_1mflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_10kflows'  + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_100kflows'  + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_1mflows'  + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_10kflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN +'_100kflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_1mflows' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_highflows(pkt_size):
    title_list = ['1Q 2PMD', '10k Flows', '100k Flows', '1 million Flows']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_10kflows').strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_100kflows').strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_'+ config.TRAFFIC_GEN +'_1mflows').strip())
    result = [title_list, pmd_result_list]
    return result

def get_pps_vanilla_testpmd(pkt_size):
    title_list = [pkt_size + ' Bytes 1k flows', '1Q', '2Q']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd'+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd'+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_vanilla_testpmd(pkt_size):
    title_list = [pkt_size + ' Bytes 1k flows', '1Q', '2Q']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd' + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd'+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.002_UseCase-2A_vanilla_testpmd'+ '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pps_enablebuf(pkt_size,custom_type):
    title_list = ['1k Flows', '1Q 2PMD', '1Q 4PMD']
    result_list = []
    result_list.append('fps')
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' +custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result_list.append(get_rx_pps('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' +custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, result_list]
    return result

def get_latency_enablebuf(pkt_size,custom_type):
    title_list = [' ', '1Q 2PMD', '1Q 4PMD']
    min_latency_result_list = []
    min_latency_result_list.append('latency min(us)')
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    min_latency_result_list.append(get_min_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list = []
    max_latency_result_list.append('latency max(us)')
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    max_latency_result_list.append(get_max_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list = []
    avg_latency_result_list.append('latency avg(us)')
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    avg_latency_result_list.append(get_avg_latency('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '/result*/*.csv', 'pvp_tput', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_result_list, max_latency_result_list, avg_latency_result_list]
    return result

def get_pmd_enablebuf(pkt_size,custom_type):
    title_list = ['1k Flows', '1Q 2PMD', '1Q 4PMD']
    pmd_result_list = []
    pmd_result_list.append('avg processing cycles per packet')
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' +custom_type).strip())
    pmd_result_list.append(get_avg_pmd('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' +custom_type).strip())
    result = [title_list, pmd_result_list]
    return result

def get_latency_half(pkt_size,custom_type):
    #half throughtput latency test
    title_list = ['50% throughtput latency', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_half_result_list = []
    min_latency_half_result_list.append('latency min(us)')
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list = []
    max_latency_half_result_list.append('latency max(us)')
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list = []
    avg_latency_half_result_list.append('latency avg(us)')
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_half_result_list, max_latency_half_result_list, avg_latency_half_result_list]
    return result

def get_latency_half_novlan_128and256(pkt_size,custom_type):
    #half throughtput latency test
    title_list = ['50% throughtput latency', '1Q 2PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_half_result_list = []
    min_latency_half_result_list.append('latency min(us)')
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list = []
    max_latency_half_result_list.append('latency max(us)')
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list = []
    avg_latency_half_result_list.append('latency avg(us)')
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_half_result_list, max_latency_half_result_list, avg_latency_half_result_list]
    return result

def get_latency_half_novlan_64and1500(pkt_size,custom_type):
    #half throughtput latency test
    title_list = ['50% throughtput latency', '1Q 2PMD', '1Q 4PMD', '2Q 4PMD', '4Q 8PMD']
    min_latency_half_result_list = []
    min_latency_half_result_list.append('latency min(us)')
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    min_latency_half_result_list.append(get_min_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list = []
    max_latency_half_result_list.append('latency max(us)')
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    max_latency_half_result_list.append(get_max_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list = []
    avg_latency_half_result_list.append('latency avg(us)')
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_2pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_1-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_2-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_4pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    avg_latency_half_result_list.append(get_avg_latency_half('/tmp/gating_4-Queue_' + str(pkt_size) + '_0.00_UseCase-1A_8pmd_testpmd_' + config.TRAFFIC_GEN + '_' + custom_type + '_latency' + '/result*/*.csv', 'pvp_latency', config.TRAFFIC_GEN).strip())
    result = [title_list, min_latency_half_result_list, max_latency_half_result_list, avg_latency_half_result_list]
    return result
