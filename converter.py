import sys
import os
import csv
import getopt
import getpass
from pprint import pprint


CV_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__)))
os.environ['CV_HOME'] = str(CV_HOME)
sys.path.append(os.path.join(CV_HOME, 'lib'))

import cvtools
import requests
import simplexml

def main(argv):
    opts = cvtools.readinputs(argv)
        
    username = None
    password = None
    if not opts.get('username') and not opts.get('password'):
        try:
            # Prompt the user for the credentials
            username = raw_input("Qualys Username: ")
            password = getpass.getpass("Qualys Password: ")
        except KeyboardInterrupt, e:
            cvtools.usage()
            sys.exit()
    else:
        username, password = opts['username'], opts['password']


    print("Downloading User List - this might take a minute...")
    ul_dl = cvtools.download_userlist(username, password)

    if ul_dl:
        print("User List has been downloaded...")
        print("Converting user list XML to CSV - this might also take a few minutes...")
        cvtools.convert_userlist()

    print "All done! The converted User List is located in: %s" % ( os.path.join(CV_HOME, 'userlist.csv'))

if __name__ == "__main__":
    main(sys.argv[1:])
