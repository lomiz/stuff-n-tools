#!/usr/bin/env python
"""
    File name: omnitools.py
    Author: Enrico lomiz Zimol
    Date created: 17/12/2013
    Date last modified: 21/08/2014
    Python Version: 2.7.X
"""
import math

__author__ = "Enrico lomiz Zimol"
__credits__ = ["Giampaolo Rodola"]
__license__ = "LGPL"
__version__ = "0.5"
__maintainer__ = "Enrico lomiz Zimol"
__email__ = "enricoONEDOTzimolROUNDEDATgmailANOTHERDOTcom"
__status__ = "Prototype"

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
    >>> len(l.get_used_latencies()) >= len(l.get_used_latencies(True))
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

    def crop_latencies(self, lat_list):
        """
        Return "list" with only latencies (exclude all None(s) that mean PacketLoss)
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

    def count_packetlost(self, lat_list):
        """
        Return None(packetloss) counts in "list"
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
        return round(reduce(lambda x, y: x + y / float(len(self.get_used_latencies(True))), self.get_used_latencies(True), 0),5)

    def length(self):
        return len(self.latencies)

    def max(self):
        return max(self.get_used_latencies(True))

    def min(self):
        return min(self.get_used_latencies(True))

    def variations_sum(self):
        sm = 0  # somma scarti
        for variation in self.get_used_latencies(True):
            sm = sm + ( (variation - self.average())**2)
        return sm

    def samp_std_dev(self):
        """
        Standard Deviation of a Sample
        """
        return math.sqrt( self.variations_sum() / (len(self.get_used_latencies(True))-1) )

    def pop_std_dev(self):
        """
        Standard Deviation of a Population
        """
        return math.sqrt(self.variations_sum()/len(self.get_used_latencies(True)))
