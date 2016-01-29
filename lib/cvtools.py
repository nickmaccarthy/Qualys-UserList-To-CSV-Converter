import sys
import os
import csv
import getopt
from pprint import pprint

import requests
from requests.auth import HTTPDigestAuth
import simplexml
import cvtools

from collections import OrderedDict

CV_HOME = os.environ.get('CV_HOME')

''' fixes errant non ascii issues that come from the kb '''
def sanitize_dict(dictionary):
    print dictionary
    if not dictionary:
        return {}
    retd = {}
    for k,v in dictionary.iteritems():
        if v is not None:
            try:
                retd[k] = v.encode('ascii', 'ignore')
            except Exception, e:
                print("unable to encode: %s, reason %s" % (v, e))
    return retd

''' read inputs from CLI '''    
def readinputs(argv):
    #try:
    #    optlist, args = getopt.getopt(argv, '', ['username=', 'password='])
    #except getopt.GetoptError, e:
    #    usage(e)
    #    sys.exit(2)

    optlist, args = getopt.getopt(argv, '', ['username=', 'password='])
    #if len(optlist) < 2:
    #    usage()
    #    sys.exit(2)
    
    returnDict = {}
    for name, value in optlist:
       returnDict[name[2:]] = value.strip()

    return returnDict

def download_userlist(username, password):
    ''' Downloads the qualys user list via API v1 '''
    try:
        r = requests.post("https://qualysapi.qualys.com/msp/user_list.php", auth=(username, password), stream=True)
        with open(os.path.join(CV_HOME, 'ul.xml'), 'wb') as fd:
            for chunk in r.iter_content(10):
                fd.write(chunk)
    except Exception, e:
        print("Unable to download user_list: Reason: %s" % (e))
        sys.exit(2)

    return True

def convert_userlist():
    with open(os.path.join(CV_HOME, 'ul.xml'), 'r') as f, open(os.path.join(CV_HOME, 'userlist.csv'), 'wb') as w:
        ulx = simplexml.loads(f.read())

        users = []

        for eu in ulx['USER_LIST_OUTPUT']['USER_LIST']['USER']:

            ul = OrderedDict() 
            ul['USER_LOGIN'] = eu['USER_LOGIN']
            ul['USER_STATUS'] = eu['USER_STATUS']
            ul['CREATION_DATE'] = eu['CREATION_DATE']
            ul['LAST_LOGIN_DATE'] = eu['LAST_LOGIN_DATE']

                
            # Contact Info
            ul['FIRSTNAME'] = eu['CONTACT_INFO']['FIRSTNAME']
            ul['LASTNAME'] = eu['CONTACT_INFO']['LASTNAME']
            ul['TITLE'] = eu['CONTACT_INFO']['TITLE']
            ul['PHONE'] = eu['CONTACT_INFO']['PHONE']
            ul['EMAIL'] = eu['CONTACT_INFO']['EMAIL']
            ul['COMPANY'] = eu['CONTACT_INFO']['COMPANY']
            ul['TIME_ZONE_CODE'] = eu['CONTACT_INFO']['TIME_ZONE_CODE']
            ul['ADDRESS1'] = eu['CONTACT_INFO']['ADDRESS1']
            ul['ADDRESS2'] = eu['CONTACT_INFO']['ADDRESS2']
            ul['CITY'] = eu['CONTACT_INFO']['CITY']
            ul['COUNTRY'] = eu['CONTACT_INFO']['COUNTRY']
            ul['STATE'] = eu['CONTACT_INFO']['STATE']
            ul['ZIP_CODE'] = eu['CONTACT_INFO']['ZIP_CODE']

            ul['BUSINESS_UNIT'] = eu['BUSINESS_UNIT']
            ul['UI_INTERFACE_STYLE'] = eu['UI_INTERFACE_STYLE']

            # Permissions
            ul['PERMISSIONS_CREATE_OPTION_PROFILES'] = eu['PERMISSIONS']['CREATE_OPTION_PROFILES']
            ul['PERMISSIONS_PURGE_INFO'] = eu['PERMISSIONS']['PURGE_INFO']
            ul['PERMISSIONS_ADD_ASSETS'] = eu['PERMISSIONS']['ADD_ASSETS']
            ul['PERMISSIONS_EDIT_REMEDIATION_POLICY'] = eu['PERMISSIONS']['EDIT_REMEDIATION_POLICY']
            ul['PERMISSIONS_EDIT_AUTH_RECORDS'] = eu['PERMISSIONS']['EDIT_AUTH_RECORDS']

            # Notifications
            ul['NOTIFY_LATEST_VULN'] = eu['NOTIFICATIONS']['LATEST_VULN']
            ul['NOTIFY_MAP'] = eu['NOTIFICATIONS']['MAP']
            ul['NOTIFY_SCAN'] = eu['NOTIFICATIONS']['SCAN']
            ul['DAILY_TICKETS'] = eu['NOTIFICATIONS']['DAILY_TICKETS']

            users.append(ul)
        
        csv_headers = users[0].keys()

        dw = csv.DictWriter(w, dialect='excel', fieldnames=csv_headers, quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"', strict=True, doublequote=True, lineterminator='\n', escapechar="\\")
        dw.writeheader()

        for user in users:
            #dw.writerow(cvtools.sanitize_dict(user))
            dw.writerow(user)

def usage():
    print "\n"
    help_def()
    print "\n\n"
    
    print "Usage:"
    print "python converter.py --username=<qualys_useranme> --password=<qualys_password>" 
    print "example: python converter.py --username=myuser --password=mYP4ssw0rd"
    print "\n"

def help_def():
    print "Downloads, parses and converts the Qualys Knowledgebase to CSV"
    print "Outputs a file in %s called 'kb.csv'" % CV_HOME
