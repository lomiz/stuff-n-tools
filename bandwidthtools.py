#!/usr/bin/env python
""" Compute hourly, daily and monthly bandwidth alert limits from a montly usable bandwidth value"""
import argparse


#==========================================================
#====COSTANTS==============================================
#==========================================================


BW_MAX=1.0



#==========================================================
#====FUNCTIONS=============================================
#==========================================================

def maxbwpertime(bwbase,trate,tfactor):
    # X_RATE_LIMIT:  Monthly bandwidth alert limit used as base value for the time range (hour,day or month) alert limits
    #                Example: 52% --> 0,52
    # X_TIME_FACTOR:  Factor used to calculate the [hour,day,month] corresponding bandwidth value in a specified X time range: hour, day or month
    MONTH_RATE_LIMIT=0.75
    DAY_RATE_LIMIT=0.8
    HOUR_RATE_LIMIT=0.9
    MONTH_TIME_FACTOR=1.0
    DAY_TIME_FACTOR=1.0/30.0
    HOUR_TIME_FACTOR=1.0/30.0/24.0

    timefactor=1.0
    timerate=1.0  # Default value

    # Time rate checks
    if isinstance(trate,str):
        if trate.upper()=='H':
            timerate=HOUR_RATE_LIMIT
        elif trate.upper()=='D':
            timerate=DAY_RATE_LIMIT
        elif trate.upper()=='M':
            timerate=MONTH_RATE_LIMIT
    elif isinstance(trate,int) or isinstance(trate,float):
        timerate=float(trate)
    else: 
        print "Ne char ne float"

    # Time factor checks
    if isinstance(tfactor,str):
        if tfactor.upper()=='H':
            timefactor=HOUR_TIME_FACTOR
        elif tfactor.upper()=='D':
            timefactor=DAY_TIME_FACTOR
        elif tfactor.upper()=='M':
            timefactor=MONTH_TIME_FACTOR
    elif isinstance(tfactor,int) or isinstance(tfactor,float):
        timefactor=float(tfactor)
    else: 
        print "Ne char ne float"

    return bwbase*timerate*timefactor


def bytes2human(n, format="%(value)i%(symbol)s"):
    """
    Translate bytes values in easy human readable format
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)

def human2bytes(s):
    """
    Translate human readable storage sizes in bytes 
    >>> human2bytes('1M')
    1048576
    >>> human2bytes('1G')
    1073741824
    """
    symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    letter = s[-1:].strip().upper()
    num = s[:-1]
    assert num.isdigit() and letter in symbols
    num = float(num)
    prefix = {symbols[0]:1}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    return int(num * prefix[letter])

#==========================================================
#====MAIN==================================================
#==========================================================
if __name__=="__main__":    
#    import doctest
#    doctest.testmod()

    # Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("bw", type=str,
                        help="The monthly bandwidth limit specified in your ISP/VPS contract.\n\
                        On this basic value we will compute the sundry bandwidth alerts.\n\
                        Examples:\n 1T, 2M, 12.13G ;\n T for Terabytes, G for Gigabytes, M for Megabytes, B for Bytes and so on..")
    args = parser.parse_args()

    BW_MAX = float(human2bytes(args.bw))


    print "Tests vari:"
    print bytes2human(maxbwpertime(BW_MAX,"m","m"))
