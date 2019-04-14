# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

"""
Base class for callbacks.

"""

from __future__ import absolute_import, unicode_literals

class Callback(object):
    """
    Base class for callbacks.

    """

    def __init__(self):
        self.stream = ""
        self.empty = ""

    def past_stream(self):
        return self.stream

    def future_stream(self):
        return self.empty

    def update(self, character):
        if character == "\b" and len(stream) > 0:
            self.stream[:-1]
        else:
            self.stream += character
