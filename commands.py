#!/usr/bin/env python

import subprocess
"""
print "\n\nExecuting 'data' command"
subprocess.call("date")

print "\n\nExecuting 'ls' command, printing result"
subprocess.call(["ls", "-la", "/etc/resolv.conf"])
"""
print "\n\nExecuting 'ls' command, storing stdout and print it"
p = subprocess.Popen(["ls", "-la", "/tmp/"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#p = subprocess.Popen(["ls", "-la", "/tmp/"])
output, err = p.communicate()
print "Output %s" % output
print "Error %s" % err
