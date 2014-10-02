# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

from __future__ import absolute_import, unicode_literals

import pressagio.character

def test_first_word_character():
    assert pressagio.character.first_word_character("8238$§(a)jaj2u2388!") == 7
    assert pressagio.character.first_word_character("123üäö34ashdh") == 3
    assert pressagio.character.first_word_character("123&(/==") == -1

def test_last_word_character():
    assert pressagio.character.last_word_character("8238$§(a)jaj2u2388!") == 13
    assert pressagio.character.last_word_character("123üäö34ashdh") == 12
    assert pressagio.character.last_word_character("123&(/==") == -1

def test_is_word_character():
    assert pressagio.character.is_word_character("ä") == True
    assert pressagio.character.is_word_character("1") == False
    assert pressagio.character.is_word_character(".") == False
