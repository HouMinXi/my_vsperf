#!/usr/bin/python
from google_http import GoogleHttp
from pprint import pprint
import format
import time
import data
import os
from subprocess import Popen, PIPE
import httplib2
from functools import wraps
import time

service = GoogleHttp(api = "sheet").service()
drive = GoogleHttp(api = "drive").service()
speed_ctl_queue = []

def speed_control(speed, window):
    """
    if speed / window is 100 / 100 , then allow 100 request per 100 seconds.
    speed is 100 requests
    window is 100 seconds
    """
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current = time.time()
            speed_ctl_queue.append(current)
            if len(speed_ctl_queue) >= speed:
                while True:
                    current = time.time()
                    start = speed_ctl_queue[-1 * speed]
                    if current - start <= window:
                        sleep_time = window - (current - start)
                        if sleep_time < 1:
                            sleep_time = 1
                        print("So fast! Need to wait %s seconds, current request queue length %d." % (sleep_time, len(speed_ctl_queue)))
                        time.sleep(sleep_time)
                        continue
                    else:
                        speed_ctl_queue[-1] = current
                        break
            return func(*args, **kwargs)
        return wrapper
    return inner

def run_shell(cmd):
    return Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]

def httplib_get_demo():
    """
    use httplib library to get data from sheet
    """
    spreadsheetId = '1pnQVT2UFtXa8Q4a54SASOS5Yt24Gn8LtcuBmk-hrNlg'
    rangeName = 'Sheet1!A1:B2'
    handler = GoogleHttp().handler()
    url = 'https://sheets.googleapis.com/v4/spreadsheets/' + spreadsheetId + '/values/' + 'Sheet1%21A2%3AE3?majorDimension=COLUMNS'
    response, content = handler.request(url)
    print(response)
    print(content)

@speed_control(5, 100)
def updateVar(spreadsheetId, data, rangeName = 'sheet1!A1:Z'):
    """
    update a array of data to sheet, values like this:
        'values' : [
            ['test2', 'test2', 'test2'],
            ['test3', 'test3', 'test3']
        ]
    """
    value_range_body = {
        'values' : data
    }
    value_input_option = 'USER_ENTERED'
    return service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range=rangeName,
        valueInputOption=value_input_option,
        body=value_range_body).execute()

def create_doc(title):
    """
    create one new table, use spreadsheet_body to set the configuration
    """

    spreadsheet_body = {
      'properties': {
        'locale': 'zh_CN',
        'timeZone': 'Etc/GMT',
        'autoRecalc': 'ON_CHANGE',
        'title': title
       },
    }
    return service.spreadsheets().create(body = spreadsheet_body).execute()

def batchget():
    """
    batch get type to get data
    """
    spreadsheetId = '137YH4gxqCGkoc7CwafMAOF3tnzsABJCq5bFnJaju8mU'
    rangeName = 'Sheet1!A2:E'
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetId, ranges=rangeName).execute()
    values = result.get('values', [])
    print(result)

def setHorizontalAlignment(spreadsheetId):
    '''
    set Horizontal Alignment of cells
    '''

    updatecells = format.setHorizontalAlignment(sheetId = sheetid(spreadsheetId)[0])
    value_range_body = {
        "requests" : [ updatecells ]
    }
    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body=value_range_body).execute()
    values = result.get('values', [])
    print(values)

def updateDimensionProperties(spreadsheetId):
    '''
    update dimension properties
    '''
    updatecells = format.updateDimensionProperties(
                    sheetId = sheetid(spreadsheetId)[0],
                    width = 100,
                    startIndex = 0,
                    endIndex = 20)
    value_range_body = {
        "requests" : [ updatecells ]
    }
    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body=value_range_body).execute()
    values = result.get('values', [])
    print(values)

def dir_demo():
    pass

def format_demo():
    '''
    update a array of data to sheet
    '''
    spreadsheetId = '137YH4gxqCGkoc7CwafMAOF3tnzsABJCq5bFnJaju8mU'
    rangeName = 'Sheet1!A1:E6'

    spreadsheet_body = {
        'properties' : {
            'title' : 'table-4',
            'defaultFormat' : {
                'horizontalAlignment' : 'CENTER',
                'verticalAlignment' : 'MIDDLE',
                'backgroundColor' : {
                    'red' : 1,
                    'green' : 1,
                    'blue' : 1
                }
            }
        },
        'sheets' : [
            {
                'properties' : {
                    'title' : 'sheet1'
                }
            }
        ]
    }

    value_input_option = 'USER_ENTERED'
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetId,
        range = rangeName,
        valueInputOption=value_input_option,
        body=spreadsheet_body).execute()
    #values = result.get('values', [])
    print(result)

def updateSheetTitle(spreadsheetId, sheetlist, titlelist):
    '''
    update a array of data to sheet
    '''
    for i in range(len(sheetlist)):
        updatesheet = format.updateSheet(index = i, sheetId = sheetlist[i], title = titlelist[i])
        sheet_body = {
            "requests" : [ updatesheet ]
        }
        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheetId,
            body=sheet_body).execute()

def get(spreadsheetId):
    return service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()

def sheetid(spreadsheetid):
    sheetId = []
    for i in get(spreadsheetid).get("sheets", None):
        sheetId.append(i["properties"]["sheetId"])
    return sheetId

def setFont(spreadsheetId, rowIndex = 0, columnIndex = 0, value = ''):
    '''
    update dimension properties
    '''
    updatecells = format.setFont(sheetId = sheetid(spreadsheetId)[0],
                              rowIndex = rowIndex,
                              columnIndex = columnIndex,
                              value = value)
    value_range_body = {
        "requests" : [ updatecells ]
    }
    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body=value_range_body).execute()
    return result

def copyTo(spreadsheetid, dest_spreadsheet_id):
    """
    copy one spreadsheet to destination spreadsheet
    """
    spreadsheet_body = {
        'destination_spreadsheet_id' : dest_spreadsheet_id,
    }
    for sheetId in sheetid(spreadsheetid):
        service.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheetid,
                                               body=spreadsheet_body,
                                               sheetId=sheetId).execute()

def deleteSheet(spreadsheetid, sheetId):
    '''
    delete sheet 
    '''
    updatecells = {
        "deleteSheet" : {
            "sheetId" : str(sheetId)
        }
    }

    value_range_body = {
        "requests" : [ updatecells ]
    }
    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetid,
        body=value_range_body).execute()
    return result

def mkdir(name, parent = None):
    if parent is None:
        p = []
    else:
        p = [parent]
    file_metadata = {
        'name' : name,
        'mimeType' : 'application/vnd.google-apps.folder',
        'parents' : p

    }
    return drive.files().create(body=file_metadata, fields='id').execute()

def mvFileToDir(fileId, folderId):
    # Retrieve the existing parents to remove
    file = drive.files().get(fileId=fileId,
                                 fields='parents').execute();
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    file = drive.files().update(fileId=fileId,
                                    addParents=folderId,
                                    removeParents=previous_parents,
                                    fields='id, parents').execute()

def permissionCreate(fileId):
    request_body = format.domainPermission(domain = 'redhat.com', role = 'reader')
    return drive.permissions().create(fileId=fileId,
                                   body = request_body).execute()

def searchFile(name, parent = None):
    page_token = None
    query_cmd = ''
    if parent is None:
        query_cmd = "mimeType='application/vnd.google-apps.folder' and name='%s' \
                    and trashed=false" % name
    else:
        query_cmd = "mimeType='application/vnd.google-apps.folder' and name='%s' \
                        and trashed=false \
                        and '%s' in parents" % (name, parent)
    while True:
        response = drive.files().list(q=query_cmd,
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name)',
                                         pageToken=page_token).execute()
        files = response.get('files', [])
        #for f in files:    
        #    print 'Found file: %s (%s)' % (f.get('name'), f.get('id'))
        if files:
            return files
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break;
    return None

def mkUniqueDir(dir, parent=None, create=False, fd_list=[]):
    """
    dir : the name of folder list that need to be created, from parent to child
    parent : the parent folder class object
    create : just created parent folder, so create child foler directly and no need to search 
    return : the last child file class
    """
    if len(dir) == 0:
        return

    if create:
        f = mkdir(name = dir[0], parent = parent)
        fd_id = f.get('id', None)
        fd_list.append(fd_id)
        mkUniqueDir(dir[1:], fd_id , create = True, fd_list = fd_list)
    else:
        f = searchFile(name = dir[0], parent = parent)
        if f is None:
            f = mkdir(name = dir[0], parent = parent)
            fd_id = f.get('id', None)
            fd_list.append(fd_id)
            mkUniqueDir(dir[1:], fd_id, create = True, fd_list = fd_list)
        else:
            if len(f) > 1:
                print("ERROR: More than one same name files %s" % dir[0])
            fd_id = f[0].get('id', None)
            fd_list.append(fd_id)
            mkUniqueDir(dir[1:], fd_id, create = False, fd_list = fd_list)
    return fd_list

def get_ovs_version():
    kernel_version=os.popen('uname -r').read().strip('\n')
    ovs_version_big=os.popen("rpm -qa|grep openvswitch | awk -F '-' '{printf $2}'").read().strip('\n')
    ovs_version_small=os.popen("rpm -qa|grep openvswitch | awk -F '-' '{printf $3}'| awk -F '.' '{printf $1}'").read().strip('\n')
    #ovs_version= 'ovs' + ovs_version_big + '-' + ovs_version_small
    ovs_version=os.popen("rpm -qa|grep openvswitch|awk -F '.x86' '{printf $1}'").read().strip('\n')
    return ovs_version

def get_dpdk_version():
    dpdk_version_big=os.popen("rpm -qa|grep dpdk| head -n 1 | awk -F '-' '{printf $2}'").read().strip('\n')
    dpdk_version_small=os.popen("rpm -qa|grep dpdk| head -n 1 | awk -F '-' '{printf $3}' | awk -F '.' '{printf $1}'").read().strip('\n')
    dpdk_version= 'dpdk' + dpdk_version_big + '-' + dpdk_version_small
    return dpdk_version
