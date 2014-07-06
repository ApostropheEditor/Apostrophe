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
"""Module for the TextView widgth wich encapsulates management of TextBuffer
and TextIter for common functionality, such as cut, copy, paste, undo, redo, 
and highlighting of text.

Using
#create the TextEditor and set the text
editor = TextEditor()
editor.text = "Text to add to the editor"

#use cut, works the same for copy, paste, undo, and redo
def __handle_on_cut(self, widget, data=None):
    self.editor.cut()

#add string to highlight
self.editor.add_highlight("Ubuntu")
self.editor.add_highlight("Quickly")

#remove highlights
self.editor.clear_highlight("Ubuntu")
self.editor.clear_all_highlight()

Configuring
#Configure as a TextView
self.editor.set_wrap_mode(Gtk.WRAP_CHAR)

#Access the Gtk.TextBuffer if needed
buffer = self.editor.get_buffer()

Extending
A TextEditor is Gtk.TextView

"""


try:
    from gi.repository import Gtk
    from gi.repository import Gdk

except:
    print("couldn't load depencies")

import logging
logger = logging.getLogger('uberwriter')


class UndoableInsert(object):
    """something that has been inserted into our textbuffer"""
    def __init__(self, text_iter, text, length, fflines):
        self.offset = text_iter.get_offset() - fflines
        self.text = text
        self.length = length
        if self.length > 1 or self.text in ("\r", "\n", " "):
            self.mergeable = False
        else:
            self.mergeable = True


class UndoableDelete(object):
    """something that has ben deleted from our textbuffer"""
    def __init__(self, text_buffer, start_iter, end_iter, fflines):
        self.text = text_buffer.get_text(start_iter, end_iter, False)
        self.start = start_iter.get_offset() - fflines
        self.end = end_iter.get_offset() - fflines
        # need to find out if backspace or delete key has been used
        # so we don't mess up during redo
        insert_iter = text_buffer.get_iter_at_mark(text_buffer.get_insert())
        if insert_iter.get_offset() <= self.start:
            self.delete_key_used = True
        else:
            self.delete_key_used = False
        if self.end - self.start > 1 or self.text in ("\r", "\n", " "):
            self.mergeable = False
        else:
            self.mergeable = True


class TextEditor(Gtk.TextView):
    """TextEditor encapsulates management of TextBuffer and TextIter for
    common functionality, such as cut, copy, paste, undo, redo, and
    highlighting of text.

    """

    def __init__(self):
        """Create a TextEditor

        """

        Gtk.TextView.__init__(self)
        self.undo_max = None

        self.insert_event = self.get_buffer().connect("insert-text", self.on_insert_text)
        self.delete_event = self.get_buffer().connect("delete-range", self.on_delete_range)
        display = self.get_display()
        self.clipboard = Gtk.Clipboard.get_for_display(display, Gdk.SELECTION_CLIPBOARD)

        self.fflines = 0

        self.undo_stack = []
        self.redo_stack = []
        self.not_undoable_action = False
        self.undo_in_progress = False

    @property
    def text(self):
        """
        text - a string specifying all the text currently
        in the TextEditor's buffer.

        This property is read/write.
        """
        start_iter = self.get_buffer().get_iter_at_offset(0)
        end_iter =  self.get_buffer().get_iter_at_offset(-1)
        return self.get_buffer().get_text(start_iter, end_iter, False)

    @property
    def can_undo(self):
        return bool(self.undo_stack)

    @property
    def can_redo(self):
        return bool(self.redo_stack)


    @text.setter
    def text(self, text):
        self.get_buffer().set_text(text)

    def append(self, text):
        """append: appends text to the end of the textbuffer.

        arguments:
        text - a string to add to the buffer. The text will be the
        last text in the buffer. The insertion cursor will not be moved.

        """

        end_iter =  self.get_buffer().get_iter_at_offset(-1)
        self.get_buffer().insert(end_iter, text)

    def prepend(self, text):
        """prepend: appends text to the start of the textbuffer.

        arguments:
        text - a string to add to the buffer. The text will be the
        first text in the buffer. The insertion cursor will not be moved.

        """

        start_iter =  self.get_buffer().get_iter_at_offset(0)
        self.get_buffer().insert(start_iter, text)
        insert_iter = self.get_buffer().get_iter_at_offset(len(text)-1)
        self.get_buffer().place_cursor(insert_iter)

    def cursor_to_end(self):
        """cursor_to_end: moves the insertion curson to the last position
        in the buffer.

        """

        end_iter = self.get_buffer().get_iter_at_offset(-1)
        self.get_buffer().place_cursor(end_iter)

    def cursor_to_start(self):
        """cursor_to_start: moves the insertion curson to the first position
        in the buffer.

        """

        start_iter = self.get_buffer().get_iter_at_offset(0)
        self.get_buffer().place_cursor(start_iter)

    def cut(self, widget=None, data=None):
        """cut: cut currently selected text and put it on the clipboard.
        This function can be called as a function, or assigned as a signal
        handler.

        """

        self.get_buffer().cut_clipboard(self.clipboard, True)

    def copy(self, widget=None, data=None):
        """copy: copy currently selected text to the clipboard.
        This function can be called as a function, or assigned as a signal
        handler.

        """
 
        self.get_buffer().copy_clipboard(self.clipboard)            

    def paste(self, widget=None, data=None):
        """paste: Insert any text currently on the clipboard into the
        buffer.
        This function can be called as a function, or assigned as a signal
        handler.

        """

        self.get_buffer().paste_clipboard(self.clipboard,None,True)

    def undo(self, widget=None, data=None):
        """undo inserts or deletions
        undone actions are being moved to redo stack"""
        if not self.undo_stack:
            return
        self.begin_not_undoable_action()
        self.undo_in_progress = True
        undo_action = self.undo_stack.pop()
        self.redo_stack.append(undo_action)
        buf = self.get_buffer()
        if isinstance(undo_action, UndoableInsert):
            offset = undo_action.offset + self.fflines
            start = buf.get_iter_at_offset(offset)
            stop = buf.get_iter_at_offset(
                offset + undo_action.length
            )
            buf.delete(start, stop)
            buf.place_cursor(start)
        else:
            start = buf.get_iter_at_offset(undo_action.start + self.fflines)
            buf.insert(start, undo_action.text)
            if undo_action.delete_key_used:
                buf.place_cursor(start)
            else:
                stop = buf.get_iter_at_offset(undo_action.end + self.fflines)
                buf.place_cursor(stop)
        self.end_not_undoable_action()
        self.undo_in_progress = False

    def redo(self, widget=None, data=None):
        """redo inserts or deletions

        redone actions are moved to undo stack"""
        if not self.redo_stack:
            return
        self.begin_not_undoable_action()
        self.undo_in_progress = True
        redo_action = self.redo_stack.pop()
        self.undo_stack.append(redo_action)
        buf = self.get_buffer()
        if isinstance(redo_action, UndoableInsert):
            start = buf.get_iter_at_offset(redo_action.offset)
            buf.insert(start, redo_action.text)
            new_cursor_pos = buf.get_iter_at_offset(
                redo_action.offset + redo_action.length
            )
            buf.place_cursor(new_cursor_pos)
        else:
            start = buf.get_iter_at_offset(redo_action.start)
            stop = buf.get_iter_at_offset(redo_action.end)
            buf.delete(start, stop)
            buf.place_cursor(start)
        self.end_not_undoable_action()
        self.undo_in_progress = False

    def on_insert_text(self, textbuffer, text_iter, text, length):
        """
            _on_insert: internal function to handle programatically inserted
            text. Do not call directly.
        """
        def can_be_merged(prev, cur):
            """see if we can merge multiple inserts here

            will try to merge words or whitespace
            can't merge if prev and cur are not mergeable in the first place
            can't merge when user set the input bar somewhere else
            can't merge across word boundaries"""
            WHITESPACE = (' ', '\t')
            if not cur.mergeable or not prev.mergeable:
                return False
            elif cur.offset != (prev.offset + prev.length):
                return False
            elif cur.text in WHITESPACE and not prev.text in WHITESPACE:
                return False
            elif prev.text in WHITESPACE and not cur.text in WHITESPACE:
                return False
            return True

        if not self.undo_in_progress:
            self.redo_stack = []
        if self.not_undoable_action:
            return

        logger.debug(text)
        logger.debug("b: %i, l: %i" % (length, len(text)))
        undo_action = UndoableInsert(text_iter, text, len(text), self.fflines)
        try:
            prev_insert = self.undo_stack.pop()
        except IndexError:
            self.undo_stack.append(undo_action)
            return
        if not isinstance(prev_insert, UndoableInsert):
            self.undo_stack.append(prev_insert)
            self.undo_stack.append(undo_action)
            return
        if can_be_merged(prev_insert, undo_action):
            prev_insert.length += undo_action.length
            prev_insert.text += undo_action.text
            self.undo_stack.append(prev_insert)
        else:
            self.undo_stack.append(prev_insert)
            self.undo_stack.append(undo_action)                
 
    def on_delete_range(self, text_buffer, start_iter, end_iter):
        """
            On delete 
        """
        def can_be_merged(prev, cur):
            """see if we can merge multiple deletions here

            will try to merge words or whitespace
            can't merge if prev and cur are not mergeable in the first place
            can't merge if delete and backspace key were both used
            can't merge across word boundaries"""

            WHITESPACE = (' ', '\t')
            if not cur.mergeable or not prev.mergeable:
                return False
            elif prev.delete_key_used != cur.delete_key_used:
                return False
            elif prev.start != cur.start and prev.start != cur.end:
                return False
            elif cur.text not in WHITESPACE and \
               prev.text in WHITESPACE:
                return False
            elif cur.text in WHITESPACE and \
               prev.text not in WHITESPACE:
                return False
            return True

        if not self.undo_in_progress:
            self.redo_stack = []
        if self.not_undoable_action:
            return
        undo_action = UndoableDelete(text_buffer, start_iter, end_iter, self.fflines)
        try:
            prev_delete = self.undo_stack.pop()
        except IndexError:
            self.undo_stack.append(undo_action)
            return
        if not isinstance(prev_delete, UndoableDelete):
            self.undo_stack.append(prev_delete)
            self.undo_stack.append(undo_action)
            return
        if can_be_merged(prev_delete, undo_action):
            if prev_delete.start == undo_action.start: # delete key used
                prev_delete.text += undo_action.text
                prev_delete.end += (undo_action.end - undo_action.start)
            else: # Backspace used
                prev_delete.text = "%s%s" % (undo_action.text,
                                                     prev_delete.text)
                prev_delete.start = undo_action.start
            self.undo_stack.append(prev_delete)
        else:
            self.undo_stack.append(prev_delete)
            self.undo_stack.append(undo_action)    

    def begin_not_undoable_action(self):
        """don't record the next actions
        
        toggles self.not_undoable_action"""
        self.not_undoable_action = True        

    def end_not_undoable_action(self):
        """record next actions
        
        toggles self.not_undoable_action"""
        self.not_undoable_action = False

class TestWindow(Gtk.Window):
    """For testing and demonstrating AsycnTaskProgressBox.

    """
    def __init__(self):
        #create a window a VBox to hold the controls
        Gtk.Window.__init__(self)
        self.set_title("TextEditor Test Window")
        windowbox = Gtk.VBox(False, 2)
        windowbox.show()
        self.add(windowbox)
        self.editor = TextEditor()
        self.editor.show()
        windowbox.pack_end(self.editor, True, True, 0)
        self.set_size_request(200,200)
        self.show()
        self.maximize()
  
        self.connect("destroy", Gtk.main_quit)
        self.editor.text = "this is some inserted text"
        self.editor.append("\nLine 3")
        self.editor.prepend("Line1\n")
        self.editor.cursor_to_end()
        self.editor.cursor_to_start()
        self.editor.undo_max = 100
        cut_button = Gtk.Button("Cut")
        cut_button.connect("clicked",self.editor.cut)
        cut_button.show()
        windowbox.pack_start(cut_button, False, False, 0)

        copy_button = Gtk.Button("Copy")
        copy_button.connect("clicked",self.editor.copy)
        copy_button.show()
        windowbox.pack_start(copy_button, False, False, 0)

        paste_button = Gtk.Button("Paste")
        paste_button.connect("clicked",self.editor.paste)
        paste_button.show()
        windowbox.pack_start(paste_button, False, False, 0)

        undo_button = Gtk.Button("Undo")
        undo_button.connect("clicked",self.editor.undo)
        undo_button.show()
        windowbox.pack_start(undo_button, False, False, 0)

        redo_button = Gtk.Button("Redo")
        redo_button.connect("clicked",self.editor.redo)
        redo_button.show()
        windowbox.pack_start(redo_button, False, False, 0)

        print(self.editor.text)


if __name__== "__main__":
    test = TestWindow()
    Gtk.main()

