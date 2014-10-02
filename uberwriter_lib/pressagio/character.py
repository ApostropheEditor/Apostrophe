# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

from __future__ import absolute_import, unicode_literals

import unicodedata

blankspaces = " \f\n\r\t\v"
separators = "`~!@#$%^&*()_-+=\\|]}[{'\";:/?.>,<†„“।॥ו–´’‘‚י0123456789ः"

def first_word_character(string):
    for i, ch in enumerate(string):
        if is_word_character(ch):
            return i

    return -1

def last_word_character(string):
    result = first_word_character(string[::-1])
    if result == -1:
        return -1
    return len(string) - result - 1

def is_word_character(char):
    # check for letter category
    if unicodedata.category(char)[0] == "L":
        return True
    return False
