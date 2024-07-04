#!/usr/bin/python
from google_http import GoogleHttp
from pprint import pprint
import format
import time
import config_weekly
import data
import weekly_report
from common import *
import config

tbl1 = [-1, -1, -1,-1, -1, -1,'64_vlan', '64_enableviommu',-1,'128_vlan','128_enableviommu',-1,'256_vlan','256_enableviommu',-1,'1500_vlan','1500_enableviommu']

tbl2 = [-1, -1, -1,-1, -1,'64_novlan',-1,-1,'128_novlan',-1,-1,'256_novlan',-1,-1,'1500_novlan',-1,-1]

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

    updateVar(spreadsheetId, newData, config_weekly.base_template_sheettitle[0] + '!A1:A')

    for k, v in pos.iteritems():
        setFont(spreadsheetId, rowIndex = v, columnIndex = 0, value = k)

def updateSecSheet(spreadsheetId, data):
    updateVar(spreadsheetId, data, config_weekly.base_template_sheettitle[0] + '!G1:I')
   
def update_sheet(spreadsheetId, data1, data2, data3, byte):
    i = tbl1.index(byte)
    updateVar(spreadsheetId, data1, config_weekly.base_template_sheettitle[i] + '!A1:E2')
    updateVar(spreadsheetId, data2, config_weekly.base_template_sheettitle[i] + '!G1:K4')
    updateVar(spreadsheetId, data3, config_weekly.base_template_sheettitle[i] + '!M1:P2')

def update_sheet_novlan(spreadsheetId, data1, data2, data3, byte):
    j = tbl2.index(byte)
    updateVar(spreadsheetId, data1, config_weekly.base_template_sheettitle[j] + '!A1:E2')
    updateVar(spreadsheetId, data2, config_weekly.base_template_sheettitle[j] + '!G1:K4')
    updateVar(spreadsheetId, data3, config_weekly.base_template_sheettitle[j] + '!M1:P4')

def update_sheet_testpmd_as_switch(spreadsheetId, data1, data2):
    updateVar(spreadsheetId, data1, config_weekly.base_template_sheettitle[4] + '!A1:B2')
    updateVar(spreadsheetId, data2, config_weekly.base_template_sheettitle[4] + '!G1:H4')
              
def main():
    spreadsheetId = config_weekly.base_template_spreadsheetId
    result_name = config.NIC_DRIVER + '_Weekly_' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    result = create_doc(title = result_name)
    destSpreadsheetId = result['spreadsheetId']
    noneSheetId = result['sheets'][0]['properties']['sheetId']
    copyTo(spreadsheetId, destSpreadsheetId)
    sheetlist = sheetid(destSpreadsheetId)
    deleteSheet(destSpreadsheetId, sheetlist[0])
    del sheetlist[0]
    updateSheetTitle(destSpreadsheetId, sheetlist, config_weekly.base_template_sheettitle)
    updateFirstSheet(destSpreadsheetId, data.ver_setup_data())
    updateSecSheet(destSpreadsheetId, data.core_data())
    update_sheet_testpmd_as_switch(destSpreadsheetId, weekly_report.get_pps_testpmd_as_switch('64'), weekly_report.get_latency_testpmd_as_switch('64'))
    print "------------Test case google sheet link is as follow------------\n https://docs.google.com/spreadsheets/d/%s" % destSpreadsheetId

    for t1 in tbl1:
        if t1 == -1:
            continue
        byte, test_type = t1.split('_')
        update_sheet(destSpreadsheetId, weekly_report.get_pps1(byte, test_type), weekly_report.get_latency1(byte , test_type), weekly_report.get_pmd1(byte , test_type), t1)

    for t2 in tbl2:
        if t2 == -1:
            continue
        byte, test_type = t2.split('_')
        update_sheet_novlan(destSpreadsheetId, weekly_report.get_pps_novlan(byte, test_type), weekly_report.get_latency_novlan(byte , test_type),weekly_report.get_pmd_novlan(byte , test_type), t2)

    ovs_folder_name = get_ovs_version()
    dpdk_folder_name = get_dpdk_version()
    folder_id =  mkUniqueDir(dir = [ "vsperf_CI_report", ovs_folder_name, "weekly"])
    mvFileToDir(fileId = destSpreadsheetId, folderId = folder_id[2])
    print permissionCreate(folder_id[0])
    with open("/tmp/googlesheet_id",'wt') as f:
        f.write("googlesheet_id=" + destSpreadsheetId)

if __name__ == '__main__':
    print run_shell('ping -w 1 -c 4 sheets.googleapis.com')
    try:
        main()
    except httplib2.ServerNotFoundError, e:
        time.sleep(5)
        print run_shell('ping -w 1 -c 4 sheets.googleapis.com')
        main()
