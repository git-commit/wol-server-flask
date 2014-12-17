# ieeemac.py
# Copyright (C) 2007, 2008 Justin Azoff JAzoff@uamail.albany.edu
#               2014, Maximilian Berger
#
# This module is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Parses, finds, and converts MAC addresses between the following formats:
 bare:    001122334455
 windows: 00-11-22-33-44-55
 unix?:   00:11:22:33:44:55
 cisco:   0011.2233.4455

>>> from ieeemac import Mac, ismac
>>> ismac("00:11:22:33:44:55")
True
>>> ismac("00:11:22:33:44:5f")
True
>>> ismac("00:11:22:33:44:5g")
False
>>> m=Mac("00:11:22:33:44:5f")
>>> m.to_cisco
'0011.2233.445f'
>>> m.to_windows
'00-11-22-33-44-5f'
>>> m=Mac("00:01:02:03:04:05")
>>> m.to_windows
'00-01-02-03-04-05'
"""

import sys
import re

SEGMENT = "[0-9a-fA-F]{2}"
SIX = ((SEGMENT,)*6)


REGEXES_S = {
    'unix':      '(%s):(%s):(%s):(%s):(%s):(%s)' % SIX,
    'windows':   '(%s)-(%s)-(%s)-(%s)-(%s)-(%s)' % SIX,
    'cisco':     '(%s)(%s)\.(%s)(%s)\.(%s)(%s)' % SIX,
    'bare':      '(%s)(%s)(%s)(%s)(%s)(%s)' % SIX,
    }
ALL_REGEX_S = '|'.join("(?P<%s>%s)" % (name, x) for (name, x) in REGEXES_S.items())
ALL_REGEX_S = "(%s)" % ALL_REGEX_S
ALL_REGEX = re.compile(ALL_REGEX_S)
ALL_REGEX_EXACT = re.compile(ALL_REGEX_S + "$")

FORMATS = {
    'unix':    '%s:%s:%s:%s:%s:%s',
    'windows': '%s-%s-%s-%s-%s-%s',
    'cisco':   '%s%s.%s%s.%s%s',
    'bare':    '%s%s%s%s%s%s',
    }

GROUP_OFFSETS = {}
for idx, group in enumerate(REGEXES_S.keys()):
    GROUP_OFFSETS[group] = 2 + idx*7

REGEXES = {}
for t, r in REGEXES_S.items():
    REGEXES[t] = re.compile(r + '$')


class Mac:

    def __init__(self, mac):
        if not mac:
            raise ValueError("Invalid mac address: None")
        mac = mac.lower()
        ret = ALL_REGEX_EXACT.match(mac)
        if not ret:
            raise ValueError("Invalid mac address: %s" % mac)

        for re_type, m in ret.groupdict().items():
            if m:
                self.format = re_type
                go = GROUP_OFFSETS[re_type]
                self.groups = ret.groups()[go:go+6]
                #don't fix the groups here, most times I just want to init
                #the object to see if the mac is valid
                self.groups_need_fixing = True
                return

    def _formats(self):
        return FORMATS.keys()
    formats = property(_formats)

    def to_format(self, format):
        if self.groups_need_fixing:
            self.groups = tuple(["%02x" % int(x, 16) for x in self.groups])
            self.groups_need_fixing = False
        return FORMATS[format] % self.groups

    def __getattr__(self, attr):
        if attr.startswith("to_"):
            format = attr[3:]
            return self.to_format(format)
        else:
            raise AttributeError

    def __str__(self):
        return self.to_format(self.format)

    def __repr__(self):
        return "Mac(%s)" % self

    def __eq__(self, other):
        if isinstance(other, str):
            return self.to_bare == Mac(other).to_bare
        else:
            return self.to_bare == other.to_bare

mac = Mac

def is_mac(mac):
    if not mac:
        return False
    mac = mac.lower()
    ret = ALL_REGEX_EXACT.match(mac)
    if not ret:
        return False
    return True

def is_mac_legacy(s):
    try:
        Mac(s)
        return True
    except ValueError:
        return False


def find_macs(text):
    """return any MAC addresses found in the text"""
    stuff = []
    for x in ALL_REGEX.finditer(text):
        x = x.group()
        m = Mac(x)
        stuff.append(m)
    return stuff


def main():
    if len(sys.argv) == 1:
        print("Usage: %s mac_address" % sys.argv[0])
        sys.exit(1)

    m = Mac(sys.argv[1])

    print("Input mac address in %s format" % m.format)

    for f in m.formats:
        print("%-10s %s" % (f, m.to_format(f)))

__all__ = ["Mac", "mac", "ismac", "find_macs", "main"]
