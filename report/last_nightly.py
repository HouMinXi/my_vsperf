from google_http import GoogleHttp
from pprint import pprint
import format
import time
import config_nightly
import data
import nightly_report
from common import *   
import config

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

    updateVar(spreadsheetId, newData, config_nightly.base_template_sheettitle[0] + '!A1:A')

    for k, v in pos.iteritems():
        setFont(spreadsheetId, rowIndex = v, columnIndex = 0, value = k)

def updateSecSheet(spreadsheetId, data):
    updateVar(spreadsheetId, data, config_nightly.base_template_sheettitle[0] + '!G1:I')
   

def updatelastSheet(spreadsheetId, data1, data2, data3, data4):
    updateVar(spreadsheetId, data1, config_nightly.base_template_sheettitle[3] + '!A1:D2')
    updateVar(spreadsheetId, data2, config_nightly.base_template_sheettitle[3] + '!G1:J4')
    updateVar(spreadsheetId, data3, config_nightly.base_template_sheettitle[3] + '!A23:D24')
    updateVar(spreadsheetId, data4, config_nightly.base_template_sheettitle[3] + '!G23:J26')

def updatepmdSheet(spreadsheetId, data1, data2):
    updateVar(spreadsheetId, data1, config_nightly.base_template_sheettitle[4] + '!A1:D2')
    updateVar(spreadsheetId, data2, config_nightly.base_template_sheettitle[4] + '!A23:D24')
              
def main():
    spreadsheetId = config_nightly.base_template_spreadsheetId
    #result_name = 'OVS-Nightly-NOVIOMMU-' + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))
    result_name = config.NIC_DRIVER + '_Nightly_' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    result = create_doc(title = result_name)
    destSpreadsheetId = result['spreadsheetId']
    noneSheetId = result['sheets'][0]['properties']['sheetId']
    copyTo(spreadsheetId, destSpreadsheetId)
    sheetlist = sheetid(destSpreadsheetId)
    deleteSheet(destSpreadsheetId, sheetlist[0])
    del sheetlist[0]
    updateSheetTitle(destSpreadsheetId, sheetlist, config_nightly.base_template_sheettitle)
    updateFirstSheet(destSpreadsheetId, data.ver_setup_data())
    updateSecSheet(destSpreadsheetId, data.core_data())
    updatelastSheet(destSpreadsheetId, nightly_report.get_pps('64'),nightly_report.get_latency('64'),nightly_report.get_pps('1500'),nightly_report.get_latency('1500'))
    updatepmdSheet(destSpreadsheetId,nightly_report.get_pmd('64'),nightly_report.get_pmd('1500'))
    print "------------Test case google sheet link is as follow------------\n https://docs.google.com/spreadsheets/d/%s" % destSpreadsheetId
    ovs_folder_name = get_ovs_version()
    dpdk_folder_name = get_dpdk_version()
    folder_id =  mkUniqueDir(dir = [ "vsperf_CI_report", ovs_folder_name, "nightly"])
    mvFileToDir(fileId = destSpreadsheetId, folderId = folder_id[2])
    #print permissionCreate(f3.get("id")) 
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
