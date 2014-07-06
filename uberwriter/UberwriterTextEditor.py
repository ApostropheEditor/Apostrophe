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
    import re
except:
    print("couldn't load depencies")


class TextEditor( Gtk.TextView ):
    """TextEditor encapsulates management of TextBuffer and TextIter for
    common functionality, such as cut, copy, paste, undo, redo, and 
    highlighting of text.

    """

    def __init__(self):
        """Create a TextEditor

        """

        Gtk.TextView.__init__(self)
        self.undo_max = None
        self._highlight_strings = []
        found_tag = Gtk.TextTag(name="highlight")
        found_tag.set_property("background","yellow")
        self.get_buffer().get_tag_table().add(found_tag)

        self.insert_event = self.get_buffer().connect("insert-text",self._on_insert)
        self.delete_event = self.get_buffer().connect("delete-range",self._on_delete)
        self.change_event = self.get_buffer().connect("changed",self._on_text_changed)
        self._auto_bullet = None
        self.auto_bullets = False
        display = self.get_display()
        self.clipboard = Gtk.Clipboard.get_for_display(display, Gdk.SELECTION_CLIPBOARD)

        self.fflines = 0

        self.undos = []
        self.redos = []

    @property
    def text(self):
        """text - a string specifying all the text currently 
        in the TextEditor's buffer.

        This property is read/write.

        """
        start_iter = self.get_buffer().get_iter_at_offset(0)
        end_iter =  self.get_buffer().get_iter_at_offset(-1)
        return self.get_buffer().get_text(start_iter,end_iter, False)

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

    def add_highlight(self, text):
        """add_highlight: add string to be highlighted when entered in the
        buffer.

        arguments:
        text - a string to be highlighted

        """ 

        if text not in self._highlight_strings:
            self._highlight_strings.append(text)
        self._highlight()

    def clear_highlight(self, text):
        """clear_highlight: stops a string from being highlighted in the 
        buffer.

        arguments:
        text - the string to stop highlighting. If the string is not currently
        being highlighted, the function will be ignored.

        """

        if text in self._highlight_strings:
            del(self._highlight_strings[text])
        self._highlight()

    def clear_all_highlights(self):
        """clear_all_highlight: stops highlighting all strings in the buffer.
        The TextEditor will forget about all strings specified for highlighting.
        If no strings are currently set for highlighting, the function will be
        ignored.

        """


        self._highlight_strings = []

        self._highlight()

    def _highlight(self):
        """_highlight: internal method to trigger highlighting.
        Do not call directly.

        """

        start_iter = self.get_buffer().get_iter_at_offset(0)
        end_iter =  self.get_buffer().get_iter_at_offset(-1)
        text = self.get_buffer().get_text(start_iter,end_iter, False)
        self.get_buffer().remove_tag_by_name('highlight', start_iter, end_iter)
        for s in self._highlight_strings:
            hits = [match.start() for match in re.finditer(re.escape(s), text)]
            for hit in hits:
                start_iter = self.get_buffer().get_iter_at_offset(hit)
                end_iter = self.get_buffer().get_iter_at_offset(hit + len(s))
                self.get_buffer().apply_tag_by_name("highlight",start_iter,end_iter)                 

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
        """undo: revert (undo) the last action.
        This function can be called as a function, or assigned as a signal
        handler.

        """

        if len(self.undos) == 0:
            return

        self.get_buffer().disconnect(self.delete_event)
        self.get_buffer().disconnect(self.insert_event)

        undo = self.undos[-1]
        redo = self._do_action(undo)
        self.redos.append(redo)
        del(self.undos[-1])

        self.insert_event = self.get_buffer().connect("insert-text",self._on_insert)
        self.delete_event = self.get_buffer().connect("delete-range",self._on_delete)
        self._highlight()

    def _do_action(self, action):
        if action["action"] == "delete":
            offset = action["offset"] + self.fflines
            start_iter = self.get_buffer().get_iter_at_offset(offset)
            end_iter =  self.get_buffer().get_iter_at_offset(offset + len(action["text"]))
            self.get_buffer().delete(start_iter, end_iter)
            action["action"] = "insert"

        elif action["action"] == "insert":
            offset = action["offset"] + self.fflines            
            start_iter = self.get_buffer().get_iter_at_offset(offset)
            self.get_buffer().insert(start_iter, action["text"])
            action["action"] = "delete"

        return action

    def redo(self, widget=None, data=None):
        """redo: revert (undo) the last revert (undo) action.
        This function can be called as a function, or assigned as a signal
        handler.

        """

        if len(self.redos) == 0:
            return

        self.get_buffer().disconnect(self.delete_event)
        self.get_buffer().disconnect(self.insert_event)

        redo = self.redos[-1]
        undo = self._do_action(redo)
        self.undos.append(undo)
        del(self.redos[-1])
        
        self.insert_event = self.get_buffer().connect("insert-text",self._on_insert)
        self.delete_event = self.get_buffer().connect("delete-range",self._on_delete)

        self._highlight()

    def _on_text_changed(self, buff):
        if self._auto_bullet is not None:
            self.get_buffer().disconnect(self.change_event)
            buff.insert_at_cursor(self._auto_bullet)
            self._auto_bullet = None
            self.change_event = self.get_buffer().connect("changed",self._on_text_changed)

    def _on_insert(self, text_buffer, iter, text, length, data=None):
        """_on_insert: internal function to handle programatically inserted
        text. Do not call directly.

        """

        self._highlight()
        offset = iter.get_offset() - self.fflines
        cmd = {"action":"delete","offset": offset,"text":text}
        self._add_undo(cmd)
        self.redos = []
        if text == "\n" and self.auto_bullets:
            cur_line = iter.get_line()
            prev_line_iter = self.get_buffer().get_iter_at_line(cur_line)
            pl_offset = prev_line_iter.get_offset()
            pl_text = self.get_buffer().get_text(prev_line_iter, iter, False)
            if pl_text.strip().find("*") == 0:
                ws = ""
                if not pl_text.startswith("*"):
                    ws = (pl_text.split("*")[0])
                self._auto_bullet = ws + "* "
                
    def _on_delete(self, text_buffer, start_iter, end_iter, data=None):
        """_on_insert: internal function to handle delete
        text. Do not call directly.

        """
        self._highlight()
        text = self.get_buffer().get_text(start_iter,end_iter, False)    
        offset = start_iter.get_offset() - self.fflines    
        cmd = {"action":"insert","offset": offset,"text":text}
        self._add_undo(cmd)

    def _add_undo(self, cmd):
        """internal function to capture current state to add to undo stack.
        Do not call directly.

        """

        #delete the oldest undo if undo maximum is in effect
        if self.undo_max is not None and len(self.undos) >= self.undo_max:
            del(self.undos[0])
        self.undos.append(cmd)

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
        self.editor.add_highlight("his")
        self.editor.clear_all_highlights()
        self.editor.add_highlight("some")
        self.editor.undo_max = 100
        self.editor.auto_bullets = True
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

