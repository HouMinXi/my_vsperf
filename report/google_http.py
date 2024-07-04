from __future__ import print_function
import httplib2
import os
import argparse
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class GoogleHttp(object):
    def __init__(self, api = ''):
        #self.url = 'https://sheets.googleapis.com/v4/spreadsheets/'
        self.api = api
        pass
    
    def get_credentials(self):
        try:
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
  
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        #SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        #SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'mhou'
        
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags, tools.argparser.parse_args(args=['--noauth_local_webserver']))
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store, tools.argparser.parse_args(args=['--noauth_local_webserver']))
            print('Storing credentials to ' + credential_path)
        return credentials
    
    def GET(self):
        pass
    
    def POST(self):
        pass
    
    def handler(self):
        """
        Return a httplib2 handler with credentials to do GET or POST
        """
        credentials = self.get_credentials()
        return credentials.authorize(httplib2.Http())
    
    def service(self):
        http = self.get_credentials().authorize(httplib2.Http())
        if self.api == 'sheet':
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
            return discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)
        elif self.api == 'drive':
            return discovery.build('drive', 'v3', http=http)
        

        
        
