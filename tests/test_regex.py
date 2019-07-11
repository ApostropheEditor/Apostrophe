#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2019, Wolf Vollprecht <w.vollprecht@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import unittest
import re

from uberwriter import markup_regex


class TestRegex(unittest.TestCase):
    """Test cases from Windows CommunityToolkit
       https://github.com/windows-toolkit/WindowsCommunityToolkit/blob/master/UnitTests/Markdown/Parse/

       TODO: use decorators. This needs decorators everywhere
    """

    def test_bold(self):
        test_texts = {
            "**bold**": "bold",
            "__bold__": "bold",
            "This is **bold** text": "bold",
            "This is __bold__ text": "bold",
            "before**middle**end": "middle",
            "before** middle **end": " middle ",
            "before******after": "**"
        }

        for test, result in test_texts.items():
            with self.subTest(name=test):
                match = re.search(markup_regex.BOLD, test)
                if not match:
                    self.assertFalse(result)
                else:
                    self.assertEqual(match.group("text"), result)

    def test_header(self):
        test_texts = {
            "#Header 1": "Header 1",
            "##Header 2": "Header 2",
            "###Header 3": "Header 3",
            "####Header 4": "Header 4",
            "#####Header 5": "Header 5",
            "######Header 6": "Header 6",
            "#######Header 6": "#Header 6",
            "#": "",
            "## # # ##": "# #",
            "#######": "",
            "before\n#Header\nafter": "Header"
        }

        for test, result in test_texts.items():
            with self.subTest(name=test):
                match = re.search(markup_regex.HEADER, test)
                if not match:
                    self.assertFalse(result)
                else:
                    self.assertEqual(match.group("text"), result)

    def test_header_under(self):
        test_texts = {
            "Header 1\n=": "Header 1",
            "Header 1##\n=": "Header 1##",
            "Header 2\n--  \n": "Header 2",
            "Header 1\n=f": None,
            "Header 1\n =": None
        }

        for test, result in test_texts.items():
            with self.subTest(name=test):
                match = re.search(markup_regex.HEADER_UNDER, test)
                if not match:
                    self.assertFalse(result)
                else:
                    self.assertEqual(match.group("text"), result)


if __name__ == '__main__':
    unittest.main()
