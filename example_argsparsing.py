#!/usr/bin/python

import argparse
# Argument Parsing
parser = argparse.ArgumentParser()

# Group for quiet/verbose mutually exclusivity 
argsgroup = parser.add_mutually_exclusive_group()
argsgroup.add_argument("-v ", "--verbose", action="store_true",
                    help="increase output verbosity in stdout" )
argsgroup.add_argument("-q ", "--quiet", action="store_true",
                    help="stop any output in stdout" )

parser.add_argument("square", type=int,
                    help="show square of given number" )
args = parser.parse_args()

result = args.square**2

if args.verbose:
    print "The square of %s is equal to %s" % (args.square,result)
elif args.quiet:
    exit()
else:
    print result
