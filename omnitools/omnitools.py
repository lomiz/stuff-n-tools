#!/usr/bin/env python
"""
    File name: omnitools.py
    Author: Enrico lomiz Zimol
    Date created: 17/12/2013
    Date last modified: 21/08/2014
    Python Version: 2.7.X
    This module aims to offer a bunch of useful classes and functions for
    scripting inside linux servers
"""
import math
import os
import platform
import logging
import pwd
#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText

__author__ = "Enrico lomiz Zimol"
__credits__ = ["Giampaolo Rodola"]
__license__ = "LGPL"
__version__ = "0.5.2"
__maintainer__ = "Enrico lomiz Zimol"
__email__ = "enricoONEDOTzimolROUNDEDATgmailANOTHERDOTcom"
__status__ = "Prototype"


DICT_CENTOS = {"CentOS": [
               "5", "5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9",
               "6", "6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9",
               "7", "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9"
              ]}

DICT_REDHAT = {"Redhat": [
               "5", "5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9",
               "6", "6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9",
               "7", "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9"
              ]}
DICT_SCIENT = {"Scientific Linux": [
               "5", "5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9",
               "6", "6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9",
               "7", "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9"
              ]}
DICT_UBUNTU = {"Ubuntu": [
               "10", "10.04", "10.10", "11", "11.04", "11.10",
               "12", "12.04", "12.10", "13", "13.04", "13.10"
              ]}


def ensure_dir(dir_path, dir_permissions=0775):
    """
    Ensure directory existence creating it if necessary.

    Arguments
        dir_path: directory to check and create
        dir_permission: permissions for that directory

    Usage
        ensure_dir("dir1/foo/", 0775)
        ensure_dir("./dir2/foo/", 777)
    """

    # if path like /dir1/dir2/file3 it remove the file part
    d = os.path.dirname(dir_path)
    dp = dir_permissions

    if not os.path.exists(d):
        try:
            logging.info("Directory %s does not exist, proceeding with creation", d)
            os.makedirs(d)
            logging.info("Directory %s created", d)
            os.chmod(d, dp)
            logging.info("Permessions %s changed", dp)
        except OSError as e:
            logging.error("Failed creation of %s with the following error:", d)
            logging.error("%s %s", e[0], e[1])
            raise  # Rilancio l'eccezione in modo che l'utilizzatore del modulo decida cosa fare
    else:
        try:
            logging.info("Directory %s existing, setting permissions", d)
            # Forzo i permessi con chmod in quanto su unix
            # c'e' una maschera in fase di creazione
            os.chmod(d, dp)
            logging.info("Permessions %s changed", dp)
        except OSError as e:
            logging.error("Permissions %s not changed for the following error:", dp)
            logging.error("%s %s", e[0], e[1])
            raise  # Rilancio l'eccezione in modo che l'utilizzatore del modulo decida cosa fare


def bytes2human(n, formatter="%(value)i%(symbol)s"):
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
            return formatter % locals()
    return formatter % dict(symbol=symbols[0], value=n)


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
    prefix = {symbols[0]: 1}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    return int(num * prefix[letter])


def uid2username(userid):
    """
    Return username of given UserID
    >>> uid2username(0)
    'root'
    """
    return pwd.getpwuid(userid)[0]


def username2uid(username):
    """
    Return UserID of given username
    >>> username2uid("root")
    0
    """
    return pwd.getpwnam(username)[2]


def get_current_userid():
    """
    Return current UserID
    """
    return os.geteuid()


def is_executed_by_user(u):
    """
    Check if the script was executed by passed user
    Arguments
        userid: userid or username to check
    """
    if isinstance(u, str):
        user = username2uid(u)
    elif isinstance(u, int):
        user = u
    else:
        return False
    if get_current_userid() != user:
        return False
    else:
        return True


def is_executed_by_root():
    """
    Check if the script was executed by root
    """
    return is_executed_by_user(0)


def is_distro(distros=None, dont_check_version=False):
    """
    Check if the current linux distribution is in a specified distros
    dictionary
    Arguments
        distros: a dictionary of distributions or a list of
                 them with which will be made the check
        dont_check_version: if True prevent to checking version
    """
    # Se non e' stato inserito alcun dizionario
    if distros is None:
        return False
    # Se e' un dizionario usiamo quello inserito dall'utente
    elif isinstance(distros, dict):
        distros_dict = distros
    # Se l'utente inserisce una lista di dizionari, usiamo un super dizionario creato dalla somma degli stessi
    elif isinstance(distros, list):
        distros_dict = {}
        for distro in distros:
            distros_dict.update(distro)
    else:
        raise TypeError("distros should be dict or list of dicts")

    # Ottengo tupla dati distribuzione e taglio il non necessario
    current_distro_string = list(platform.linux_distribution())[:2]

    # Primo valore tupla: nome distribuzione
    # Secondo valore tupla: versione distribuzione
    cur_dis_name = current_distro_string[0]
    cur_dis_ver = current_distro_string[1]

    #if distros_dict.has_key(cur_dis_name): "has_key DEPRECATED - better form with "in"
    if cur_dis_name in distros_dict:
    #Se nel dizionario delle distribuzioni valide e' presente quella corrente..
        if dont_check_version or (cur_dis_ver in distros_dict.get(cur_dis_name)):
            # Se non devo controllare la versione OPPURE la versione corrente
            # e' presente  nella lista del dizionario distribuzioni valide
            return True
        else:
            return False
    else:
        return False


def is_vsdistro():
    """
    Check if current distro is in the Vulcania System distros list
    """
    return is_distro([DICT_CENTOS, DICT_REDHAT, DICT_SCIENT])


# TODO LatencyList
# Using decorators or @propriety force used_latencies to be less or equal of max_width
# http://stackoverflow.com/questions/17330160/python-how-does-the-property-decorator-work


class LatencyList:
    """
    Manages and elaborates a list of latencies
        A list that work with FIFO(First In First Out) logic.
        You can obtain usefull latency information like jitter, average, min, max calculated
        with the lasts N latencies where N is "used_latencies".

    Class Attributes:
        latencies -- a list of lantencies in ms
        max_width -- over this list width old latencies will be discharged to allow new ones (FIFO system)
        used_latencies -- how many recent latencies will be used for calculations

    DocTest
    >>> l = LatencyList([], 8)
    >>> l.max_width = 15
    >>> l.add(42.3)
    >>> l.add(47.432)
    >>> l.add(81)
    >>> l.add(50.19)
    >>> l.add(150.91)
    >>> l.add(40.7)
    >>> l.add(45)
    >>> l.add(69.4)
    >>> l.add(13.43)
    >>> l.add(64.6)
    >>> l.add(None)
    >>> l.add(None)
    >>> l.add(None)
    >>> l.add(44.9123)
    >>> l.add(23.1)
    >>> l.length()
    15
    >>> l.add(44.9123)
    >>> l.add(23.1)
    >>> l.length()
    15
    >>> len(l.get_used_latencies())>=len(l.get_used_latencies(True))
    True
    >>> l.get_packetloss()
    0.375
    >>> round(l.samp_std_dev(),3)
    17.497
    >>> round(l.pop_std_dev(),3)
    15.65
    """

    def __init__(self, latencies=[], used_latencies=15):
        self.latencies = latencies
        self.max_width = 50
        self.used_latencies = used_latencies

    def __str__(self):
        #return str(self.latencies)
        # To obtain only 2 decimal precision
        #l = ["%0.2f" % i for i in self.latencies]
        r = "latencies: " + str(self.get_string_latencies()) + \
            "\nmax_width: " + str(self.max_width) + \
            "\nlength: " + str(self.length()) + \
            "\nused_latencies: " + str(self.used_latencies) + "\n"
        return r

    def get_string_latencies(self, rounding_decimals=2):
        """
        Convert self.latencies elements in strings and trucates off numerical values to N decimals
        where N is rounding_decimals. None value (packet lost) will be translated in "lost".
        This new list isn't suitable for calculation
        """
        # String conversion and float truncation to the new list
        rounded_list = []
        for latency in self.latencies:
            # if number -> truncate decimal and append to list
            if isinstance(latency, int) or isinstance(latency, float):
                rounded_list.append(str(round(latency, rounding_decimals)))
            # if other -> append only
            else:
                rounded_list.append("lost")
        return rounded_list

    def get_used_latencies(self, crop=False):
        """
        Return a list of last N latencies where N is "used_latencies"
        If you need the list for calculation probably you want to enable the cropping
            crop - if True remove every "None" in the list and return list cleaned. Usefull for calculation.
        """
        if crop:
            return self.crop_latencies(self.latencies[-self.used_latencies:])
        else:
            return self.latencies[-self.used_latencies:]

    @staticmethod
    def crop_latencies(lat_list):
        """
        Return "lat_list" with only latencies excluding all None(s)(packets lost)
        """
        cropped_list = []
        for latency in lat_list:
            if latency is not None:
                cropped_list.append(latency)
        return cropped_list

    def get_packetloss(self):
        """
        Return packetloss percentage in used_latencies
        """
        return self.count_packetlost(self.get_used_latencies()) / float(self.used_latencies)

    @staticmethod
    def count_packetlost(lat_list):
        """
        Return None(packetloss) counts in "lat_list"
        """
        counter = 0
        for latency in lat_list:
            if latency is None:
                counter += 1
        return counter

    def add(self, latency):
        if self.length() >= self.max_width:
            self.remove()
        self.latencies.append(latency)

    def remove(self):
        self.latencies.pop(0)

    def average(self):
        return round(reduce(
            lambda x, y: x + y / float(len(self.get_used_latencies(True))), self.get_used_latencies(True),
            0), 5)

    def length(self):
        return len(self.latencies)

    def max(self):
        return max(self.get_used_latencies(True))

    def min(self):
        return min(self.get_used_latencies(True))

    def variations_sum(self):
        sm = 0  # somma scarti
        for variation in self.get_used_latencies(True):
            sm += (variation - self.average())**2
        return sm

    def samp_std_dev(self):
        """
        Standard Deviation of a Sample
        """
        return math.sqrt(self.variations_sum() / (len(self.get_used_latencies(True))-1))

    def pop_std_dev(self):
        """
        Standard Deviation of a Population
        """
        return math.sqrt(self.variations_sum()/len(self.get_used_latencies(True)))

       
if __name__ == "__main__":
    import doctest
    doctest.testmod()

