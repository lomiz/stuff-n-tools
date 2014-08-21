#!/usr/bin/python

import os, sys


def checkUserExec(userid=0):
    # Root or GTFO
    if os.geteuid()!=userid:
        sys.exit("\nOnly root can run this script. GTFO.\n")


def checkDistro(distros,release = None):
    #implement me !!!
    return False


checkUserExec(1000)
print "Success"



