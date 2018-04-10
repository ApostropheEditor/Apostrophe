# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012, Wolf Vollprecht <w.vollprecht@gmail.com>
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


import gettext

import re
from gi.repository import Gtk, Gdk # pylint: disable=E0611
from gi.repository import Pango # pylint: disable=E0611

gettext.textdomain('uberwriter')
gettext.bindtextdomain('uberwriter', 'po')
_ = gettext.gettext


from . MarkupBuffer import MarkupBuffer

class FormatShortcuts():

	def __init__(self, textbuffer, texteditor):
		self.TextBuffer = textbuffer
		self.TextEditor = texteditor

	def rule(self):
		self.TextBuffer.insert_at_cursor("\n\n-------\n")
		self.TextEditor.scroll_mark_onscreen(self.TextBuffer.get_insert())
		self.regex = MarkupBuffer.regex

	def bold(self):
		self.apply_format("**")
	
	def italic(self):
		self.apply_format("*")

	def strikeout(self):
		self.apply_format("~~")

	def apply_format(self, wrap = "*"):
		if self.TextBuffer.get_has_selection():
			## Find current highlighting

			(start, end) = self.TextBuffer.get_selection_bounds()
			moved = False
			if ( 
				start.get_offset() >= len(wrap) and 
				end.get_offset() <= self.TextBuffer.get_char_count() - len(wrap)
				):
				moved = True
				ext_start = start.copy()
				ext_start.backward_chars(len(wrap))
				ext_end = end.copy()
				ext_end.forward_chars(len(wrap))
				text = self.TextBuffer.get_text(ext_start, ext_end, True)
			else:
				text = self.TextBuffer.get_text(start, end, True)
			
			if moved and text.startswith(wrap) and text.endswith(wrap):
				text = text[len(wrap):-len(wrap)]
				new_text = text
				self.TextBuffer.delete(ext_start, ext_end)
				move_back = 0
			else:
				if moved:
					text = text[len(wrap):-len(wrap)]
				new_text = text.lstrip().rstrip()
				text = text.replace(new_text, wrap + new_text + wrap)

				self.TextBuffer.delete(start, end)
				move_back = len(wrap)
			
			self.TextBuffer.insert_at_cursor(text)
			text_length = len(new_text)

		else:
			helptext = ""
			if wrap == "*":
				helptext = _("emphasized text")
			elif wrap == "**":
				helptext = _("strong text")
			elif wrap == "~~":
				helptext = _("striked out text")

			self.TextBuffer.insert_at_cursor(wrap + helptext + wrap)
			text_length = len(helptext)
			move_back = len(wrap)

		cursor_mark = self.TextBuffer.get_insert()
		cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)
		cursor_iter.backward_chars(move_back)
		self.TextBuffer.move_mark_by_name('selection_bound', cursor_iter)
		cursor_iter.backward_chars(text_length)
		self.TextBuffer.move_mark_by_name('insert', cursor_iter)

	def unordered_list_item(self):
		helptext = _("List item")
		text_length = len(helptext)
		move_back = 0
		if self.TextBuffer.get_has_selection():
			(start, end) = self.TextBuffer.get_selection_bounds()
			if start.starts_line():
				text = self.TextBuffer.get_text(start, end, False)
				if text.startswith(("- ", "* ", "+ ")):
					delete_end = start.forward_chars(2)
					self.TextBuffer.delete(start, delete_end)
				else:
					self.TextBuffer.insert(start, "- ")
		else:
			move_back = 0
			cursor_mark = self.TextBuffer.get_insert()
			cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)

			start_ext = cursor_iter.copy()
			start_ext.backward_lines(3)
			text = self.TextBuffer.get_text(cursor_iter, start_ext, False)
			lines = text.splitlines()

			for line in reversed(lines):
				if len(line) and line.startswith(("- ", "* ", "+ ")):
					if cursor_iter.starts_line():
						self.TextBuffer.insert_at_cursor(line[:2] + helptext)
					else:
						self.TextBuffer.insert_at_cursor("\n" + line[:2] + helptext)
					break
				else:
					if len(lines[-1]) == 0 and len(lines[-2]) == 0:
						self.TextBuffer.insert_at_cursor("- " + helptext)
					elif len(lines[-1]) == 0:
						if cursor_iter.starts_line():
							self.TextBuffer.insert_at_cursor("- " + helptext)
						else:
							self.TextBuffer.insert_at_cursor("\n- " + helptext)
					else:
						self.TextBuffer.insert_at_cursor("\n\n- " + helptext)
					break

			self.select_edit(move_back, text_length)

	def ordered_list_item(self):
		pass

	def select_edit(self, move_back, text_length):
		cursor_mark = self.TextBuffer.get_insert()
		cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)
		cursor_iter.backward_chars(move_back)
		self.TextBuffer.move_mark_by_name('selection_bound', cursor_iter)
		cursor_iter.backward_chars(text_length)
		self.TextBuffer.move_mark_by_name('insert', cursor_iter)
		self.TextEditor.scroll_mark_onscreen(self.TextBuffer.get_insert())

	def above(self, linestart = ""):
		if not cursor_iter.starts_line():
			return ""
		else:
			cursor_mark = self.TextBuffer.get_insert()
			cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)

			start_ext = cursor_iter.copy()
			start_ext.backward_lines(2)
			text = self.TextBuffer.get_text(cursor_iter, start_ext, False)
			lines = text.splitlines()

			#if line[-1].startswith

	def get_lines(self, cursor_iter):

		start_ext = cursor_iter.copy()
		start_ext.backward_lines(2)
		text = self.TextBuffer.get_text(cursor_iter, start_ext, False)
		lines = text.splitlines()

		abs_line = cursor_iter.get_line()

		return reversed(lines)

	def heading(self, level = 0):
		helptext = _("Heading")
		before = ""		
		if self.TextBuffer.get_has_selection():
			(start, end) = self.TextBuffer.get_selection_bounds()
			text = self.TextBuffer.get_text(start, end, False)
			self.TextBuffer.delete(start, end)
		else:
			text = helptext

		cursor_mark = self.TextBuffer.get_insert()
		cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)

		#lines = self.get_lines(cursor_iter)

		#if cursor_iter.starts_line():
		#	if lines[1] != '':
		#		before = before + "\n"
		#else:
		#	match = re.match(r'([\#]+ )(.+)', lines[0])
		#	if match: 
		#		if match.group(1):
		#			
		#		print match.group(0)
		#		if len(match.group(0)) < 6:
		#			before = before + "#" * (len(match.group(0)) + 1) 
		#		else:
		#			before = before + "#"
		#	else:
		#		before = before + "\n\n"
		#		
		#	
		#	check_text = self.TextBuffer.get_text(start, cursor_iter, False).decode("utf-8")
		#	print check_text

		self.TextBuffer.insert_at_cursor("#" + " " + text)
		self.select_edit(0, len(text))
