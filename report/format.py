from datetime import datetime

import time

class Color(object):
    def __init__(self):
        pass
    
    @staticmethod
    def red():
        return {
            "red": 1.0,
            "green": 0.9,
            "blue": 0.9
        }
        
    @staticmethod
    def green():
        return {
            "red": 1.0,
            "green": 0.9,
            "blue": 0.9
        }
        
    @staticmethod
    def blue():
        return {
            "red": 1.0,
            "green": 0.9,
            "blue": 0.9
        }    
        
def addsheet():
    """
    add a new sheet
    """
    return { 
      "addSheet" : {
        "properties": {
          "title": "Deposits1",     # the title name of sheet
          "gridProperties": {
            "rowCount": 20,
            "columnCount": 12
           },
                           
          "tabColor": {             # the color of tab sheet
             "red": 1.0,
             "green": 0.9,
             "blue": 0.9
          }
        } 
      }
    }
    

def setHorizontalAlignment(sheetId, rangeNum = 10, horizontalAlignment = "CENTER"):
    """
    update cells to set the background color, context, note of cells
    """
    centor = { "userEnteredFormat": {
                "horizontalAlignment": horizontalAlignment,    
               }
             }
    
    rows = []
    for i in range(rangeNum):
        values = []
        for i in range(rangeNum):
            values.append(centor)
        rows.append({ "values" : values })
    
    return {
      "updateCells": {
        "rows": rows, 
        "fields" : "*",
        "range" : {
          "sheetId": sheetId,
          "startRowIndex": 0,
          "endRowIndex": rangeNum,
          "startColumnIndex": 0,
          "endColumnIndex": rangeNum
        },
      }
    }
    
def updatecells_backup(sheetId):
    """
    update cells to set the background color, context, note of cells
    """
    return {
      "updateCells": {
        "rows": [ {
          "values" : [ 
            {
              "userEnteredFormat": {
                "backgroundColor": {
                  "blue" : 1.0,
                },
                "horizontalAlignment": "CENTER",    
              },
                 
              "userEnteredValue": {
                "stringValue": "stringvalue",
              },
                    
              "note" : "this is a note",
            },
            {
              "userEnteredFormat": {
                "backgroundColor": {
                  "blue" : 0.3,
                  "red" : 0.65,
                  "green" : 0.7
                },
                "horizontalAlignment": "CENTER",
              },
                     
              "userEnteredValue": {
                "stringValue": "stringvalue2",
               },
                     
               "note" : "this is a note",
            }
          ]
        }], 

        "fields" : "*", 
        
        "range" : {
          "sheetId": sheetId,
          "startRowIndex": 0,
          "endRowIndex": 20,
          "startColumnIndex": 0,
          "endColumnIndex": 20
        },
      }
    } 
    
def setFont(sheetId, rowIndex = 0, columnIndex = 0, value = ''):
    """
    set font of one cell
    """
    return {
      "updateCells": {
        "rows": [ {
          "values" : [ 
            {
              "userEnteredFormat": {
                "textFormat" : {
                  "fontSize": 14,
                  "bold" : True
                }
              },
              "userEnteredValue": {
                "stringValue": value,
              },
            }
          ]
        }], 

        "fields" : "*", 
        
        "range" : {
          "sheetId": sheetId,
          "startRowIndex": rowIndex,
          "endRowIndex": rowIndex + 1,
          "startColumnIndex": columnIndex,
          "endColumnIndex": columnIndex + 1
        },
      }
    } 

       
    
def updateDimensionProperties(sheetId, width, startIndex = 0, endIndex = 0):
    """
    set the width or height of cells
    """
    return {
      "updateDimensionProperties": {
        "range": {
          "sheetId": sheetId,
          "dimension": "COLUMNS",
          "startIndex": startIndex,
          "endIndex": endIndex
        },
        "properties": {
          "pixelSize": width
        },
        "fields": "pixelSize"
      }
    }
    
def updateSheet(index, sheetId, title):
    return {
      'updateSheetProperties' : {
          'properties' : {
            'sheetId' : sheetId,
            'title' :  title,
            'index' : index
           },
          'fields' : 'title'
       }
    }
    
def userPermission(email, role = 'writer'):
    expire = str(datetime.now().year + 1) + time.strftime("-%m-%dT23:59:59Z", time.localtime(time.time()))
    return {
      "kind" : "drive#permission",
      "type" : "user",
      "emailAddress" : email,
      "role" : role,
      "expirationTime" : expire,
    }


def domainPermission(domain, role = 'writer'):
    expire = str(datetime.now().year + 1) + time.strftime("-%m-%dT23:59:59Z", time.localtime(time.time()))
    return {
      "kind" : "drive#permission",
      "type" : "domain",
      "domain" : domain,
      "role" : role,
      "expirationTime": expire,
      "allowFileDiscovery" : True
    }

def test_1():
    """
    update cells to set the background color, context, note of cells
    """
    return {
        "updateCells": {
            "rows": [ {
                "values" : [ 
                    {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "blue" : 1.0,
                            },
                            "horizontalAlignment": "CENTER",
                            "padding" : {
                                "top" : 5,
                                "right" : 200,
                                "bottom" : 5,
                                "left" :20
                            },
                        },
                 
                        "userEnteredValue": {
                            "stringValue": "1",
                        },
                    
                        "note" : "this is a note",
                    },
                    {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "blue" : 0.3,
                                "red" : 0.65,
                                "green" : 0.7
                             },
                            "horizontalAlignment": "CENTER" 
                        },
                     
                        "userEnteredValue": {
                            "stringValue": "stringvalue2",
                        },
                     
                         "note" : "this is a note",
                    }
                ]
            }], 
        }
    }
        
    
    
