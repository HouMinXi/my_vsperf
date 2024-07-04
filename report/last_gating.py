#!/usr/bin/python
from google_http import GoogleHttp
from pprint import pprint
import format
import time
import config_gating
import data
import gating_report
from common import *
import config

tbl1 = [-1, -1, -1,-1, -1, -1,'64_vlan', -1,-1,'128_vlan',-1,-1,'256_vlan',-1,-1,'1500_vlan',-1,-1,-1,-1,-1,-1,-1,-1]
"""
tbl1 = [-1 for i in range(24)]
tbl1[6] = '64_vlan'
tbl1[9] = '128_vlan'
tbl1[12] = '256_vlan'
tbl1[15] = '1500_vlan'
"""
tbl2 = [-1, -1, -1,-1, -1,-1,-1,'64_enableviommu',-1,-1,'128_enableviommu',-1,-1,'256_enableviommu',-1,-1,'1500_enableviommu',-1,-1,-1,-1,-1,-1,-1]

tbl3 = [-1, -1, -1,-1, -1, '64_novlan',-1,-1,-1,-1,-1,-1,-1,-1,	'1500_novlan',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

tbl4 = [-1, -1, -1,-1, -1, -1,-1,-1,'128_novlan',-1,-1,'256_novlan',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]


def updateFirstSheet(spreadsheetId, data):
    """
    """
    def position(index, data):
        if index == 0:
            return 0
        else:
            return position(index - 1, data) + len(data[index - 1].values()[0]) + 2

    pos = {}
    newData = []
    for i in range(0, len(data)):
        pos[data[i].keys()[0]] = position(i, data)
        for k, v in data[i].iteritems():
            newData.append([k])
            for item in v:
                newData.append([item])
            newData.append([''])

    updateVar(spreadsheetId, newData, config_gating.base_template_sheettitle[0] + '!A1:A')

    for k, v in pos.iteritems():
        setFont(spreadsheetId, rowIndex = v, columnIndex = 0, value = k)

def updateSecSheet(spreadsheetId, data):
    updateVar(spreadsheetId, data, config_gating.base_template_sheettitle[0] + '!G1:I')
   
def update_sheet(spreadsheetId, data1, data2, data3, data4, byte):
    i = tbl1.index(byte)
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[i] + '!A1:D2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[i] + '!F1:I4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[i] + '!M1:P2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[i] + '!F20:I23')

def update_sheet_enableviommu(spreadsheetId, data1, data2, data3, data4, byte):
    i = tbl2.index(byte)
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[i] + '!A1:D2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[i] + '!F1:I4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[i] + '!M1:P2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[i] + '!F20:I23')

def update_sheet_novlan_64and1500(spreadsheetId, data1, data2, data3, data4, byte):
    i = tbl3.index(byte)
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[i] + '!A1:F2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[i] + '!H1:M4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[i] + '!O1:T2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[i] + '!H20:M23')

def update_sheet_novlan_128and256(spreadsheetId, data1, data2, data3, data4, byte):
    i = tbl4.index(byte)
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[i] + '!A1:E2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[i] + '!G1:K4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[i] + '!M1:Q2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[i] + '!G20:K23')

def update_sheet_enablebuf(spreadsheetId, data1, data2, data3, data4, data5, data6):
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[17] + '!A1:E2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[17] + '!G1:K4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[18] + '!A1:E2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[18] + '!G1:K4')
    updateVar(spreadsheetId, data5, config_gating.base_template_sheettitle[17] + '!M1:O2')
    updateVar(spreadsheetId, data6, config_gating.base_template_sheettitle[18] + '!M1:O2')

def update_sheet_testpmd_as_switch(spreadsheetId, data1, data2):
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[4] + '!A1:B2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[4] + '!G1:H4')

def update_sheet_jumbo(spreadsheetId, data1, data2, data3, data4, data5, data6):
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[19] + '!A1:C2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[19] + '!G1:I4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[20] + '!A1:C2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[20] + '!G1:I4')
    updateVar(spreadsheetId, data5, config_gating.base_template_sheettitle[19] + '!M1:O2')
    updateVar(spreadsheetId, data6, config_gating.base_template_sheettitle[20] + '!M1:O2')

def update_sheet_highflows(spreadsheetId, data1, data2, data3, data4, data5, data6):
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[21] + '!A1:D2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[21] + '!G1:J4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[22] + '!A1:D2')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[22] + '!G1:J4')             
    updateVar(spreadsheetId, data5, config_gating.base_template_sheettitle[21] + '!M1:P2')
    updateVar(spreadsheetId, data6, config_gating.base_template_sheettitle[22] + '!M1:P2')
 
def update_sheet_vanilla_testpmd(spreadsheetId, data1, data2, data3, data4):
    updateVar(spreadsheetId, data1, config_gating.base_template_sheettitle[23] + '!A1:C2')
    updateVar(spreadsheetId, data2, config_gating.base_template_sheettitle[23] + '!G1:I4')
    updateVar(spreadsheetId, data3, config_gating.base_template_sheettitle[23] + '!A23:C24')
    updateVar(spreadsheetId, data4, config_gating.base_template_sheettitle[23] + '!G23:I26')


def main():
    spreadsheetId = config_gating.base_template_spreadsheetId
    result_name = config.NIC_DRIVER + '_Gating_' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    result = create_doc(title = result_name)
    destSpreadsheetId = result['spreadsheetId']
    noneSheetId = result['sheets'][0]['properties']['sheetId']
    copyTo(spreadsheetId, destSpreadsheetId)
    sheetlist = sheetid(destSpreadsheetId)
    deleteSheet(destSpreadsheetId, sheetlist[0])
    del sheetlist[0]
    updateSheetTitle(destSpreadsheetId, sheetlist, config_gating.base_template_sheettitle)
    updateFirstSheet(destSpreadsheetId, data.ver_setup_data())
    updateSecSheet(destSpreadsheetId, data.core_data())
    update_sheet_testpmd_as_switch(destSpreadsheetId, gating_report.get_pps_testpmd_as_switch('64'), gating_report.get_latency_testpmd_as_switch('64'))
    update_sheet_jumbo(destSpreadsheetId, gating_report.get_pps_jumbo('2000', 'novlan'), gating_report.get_latency_jumbo('2000', 'novlan'),gating_report.get_pps_jumbo('9000', 'novlan'), gating_report.get_latency_jumbo('9000', 'novlan'),gating_report.get_pmd_jumbo('2000', 'novlan'),gating_report.get_pmd_jumbo('9000', 'novlan'))

    update_sheet_highflows(destSpreadsheetId, gating_report.get_pps_highflows('64'), gating_report.get_latency_highflows('64'),gating_report.get_pps_highflows('1500'), gating_report.get_latency_highflows('1500'),gating_report.get_pmd_highflows('64'),gating_report.get_pmd_highflows('1500'))    

    update_sheet_vanilla_testpmd(destSpreadsheetId, gating_report.get_pps_vanilla_testpmd('64'), gating_report.get_latency_vanilla_testpmd('64'),gating_report.get_pps_vanilla_testpmd('1500'), gating_report.get_latency_vanilla_testpmd('1500'))

    update_sheet_enablebuf(destSpreadsheetId, gating_report.get_pps_enablebuf('64', 'enablebuf'), gating_report.get_latency_enablebuf('64', 'enablebuf'),gating_report.get_pps_enablebuf('1500', 'enablebuf'), gating_report.get_latency_enablebuf('1500', 'enablebuf'),gating_report.get_pmd_enablebuf('64', 'enablebuf'),gating_report.get_pmd_enablebuf('1500', 'enablebuf'))
   
 
    print "------------Test case google sheet link is as follow------------\n https://docs.google.com/spreadsheets/d/%s" % destSpreadsheetId

    print tbl1
    for t1 in tbl1:
        if t1 == -1:
            continue
        byte, test_type = t1.split('_')
        update_sheet(destSpreadsheetId, gating_report.get_pps_vlan(byte, test_type), gating_report.get_latency_vlan(byte , test_type), gating_report.get_pmd_vlan(byte , test_type),gating_report.get_latency_half(byte, test_type), t1)

    print tbl2
    for t2 in tbl2:
        if t2 == -1:
            continue
        byte, test_type = t2.split('_')
        update_sheet_enableviommu(destSpreadsheetId, gating_report.get_pps_iommu(byte, test_type), gating_report.get_latency_iommu(byte , test_type),gating_report.get_pmd_iommu(byte , test_type),gating_report.get_latency_half(byte, test_type), t2)
    time.sleep(5) 
    print tbl3
    for t3 in tbl3:
        if t3 == -1:
            continue
        byte, test_type = t3.split('_')
        update_sheet_novlan_64and1500(destSpreadsheetId, gating_report.get_pps_novlan_64and1500(byte, test_type), gating_report.get_latency_novlan_64and1500(byte , test_type),gating_report.get_pmd_novlan_64and1500(byte , test_type),gating_report.get_latency_half_novlan_64and1500(byte, test_type), t3)
        time.sleep(10)
    print tbl4
    for t4 in tbl4:
        if t4 == -1:
            continue
        byte, test_type = t4.split('_')
        update_sheet_novlan_128and256(destSpreadsheetId, gating_report.get_pps_novlan_128and256(byte, test_type), gating_report.get_latency_novlan_128and256(byte , test_type), gating_report.get_pmd_novlan_128and256(byte , test_type),gating_report.get_latency_half_novlan_128and256(byte, test_type), t4)
 
    ovs_folder_name = get_ovs_version()
    dpdk_folder_name = get_dpdk_version()
    folder_id =  mkUniqueDir(dir = [ "vsperf_CI_report", ovs_folder_name, "gating"])
    mvFileToDir(fileId = destSpreadsheetId, folderId = folder_id[2])
    print permissionCreate(folder_id[0])
    with open("/tmp/googlesheet_id",'wt') as f:
        f.write("googlesheet_id=" + destSpreadsheetId)

if __name__ == '__main__':
    print run_shell('ping -w 1 -c 4 sheets.googleapis.com')
    """
    try:
        main()
    except httplib2.ServerNotFoundError, e:
        time.sleep(5)
        print run_shell('ping -w 1 -c 4 sheets.googleapis.com')
        main()
    """

    for i in range(3):
        try:
            main()
        except httplib2.ServerNotFoundError, e:
            time.sleep(5)
            print run_shell('ping -w 1 -c 4 sheets.googleapis.com')
            continue
        except Exception, e:
            print(e)
            print("update google sheet failed, try it after 60s")
            time.sleep(60)
            break
        else:
            break
            
