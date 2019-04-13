class UndoableInsert:
    """Something has been inserted into text_buffer"""

    def __init__(self, text_iter, text, length):
        self.offset = text_iter.get_offset()
        self.text = text
        self.length = length
        self.mergeable = not bool(self.length > 1 or self.text in ("\r", "\n", " "))


class UndoableDelete:
    """Something has been deleted from text_buffer"""

    def __init__(self, text_buffer, start_iter, end_iter):
        self.text = text_buffer.get_text(start_iter, end_iter, False)
        self.start = start_iter.get_offset()
        self.end = end_iter.get_offset()
        # Find out if backspace or delete were used to not mess up redo
        insert_iter = text_buffer.get_iter_at_mark(text_buffer.get_insert())
        self.delete_key_used = bool(insert_iter.get_offset() <= self.start)
        self.mergeable = not bool(self.end - self.start > 1 or self.text in ("\r", "\n", " "))


class UndoRedoHandler:
    """Manages undo/redo for a given text_buffer.

    Methods can be called directly, as well as be used as signal callbacks."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.not_undoable_action = False
        self.undo_in_progress = False

    def undo(self, text_view, _data=None):
        """Undo insertions or deletions. Undone actions are moved to redo stack.

        This method can be registered to a custom undo signal, or used independently."""

        if not self.undo_stack:
            return
        self.__begin_not_undoable_action()
        self.undo_in_progress = True
        undo_action = self.undo_stack.pop()
        self.redo_stack.append(undo_action)
        text_buffer = text_view.get_buffer()
        if isinstance(undo_action, UndoableInsert):
            offset = undo_action.offset
            start = text_buffer.get_iter_at_offset(offset)
            stop = text_buffer.get_iter_at_offset(
                offset + undo_action.length
            )
            text_buffer.place_cursor(start)
            text_buffer.delete(start, stop)
        else:
            start = text_buffer.get_iter_at_offset(undo_action.start)
            text_buffer.insert(start, undo_action.text)
            if undo_action.delete_key_used:
                text_buffer.place_cursor(start)
            else:
                stop = text_buffer.get_iter_at_offset(undo_action.end)
                text_buffer.place_cursor(stop)
        self.__end_not_undoable_action()
        self.undo_in_progress = False

    def redo(self, text_view, _data=None):
        """Redo insertions or deletions. Redone actions are moved to undo stack

        This method can be registered to a custom redo signal, or used independently."""

        if not self.redo_stack:
            return
        self.__begin_not_undoable_action()
        self.undo_in_progress = True
        redo_action = self.redo_stack.pop()
        self.undo_stack.append(redo_action)
        text_buffer = text_view.get_buffer()
        if isinstance(redo_action, UndoableInsert):
            start = text_buffer.get_iter_at_offset(redo_action.offset)
            text_buffer.insert(start, redo_action.text)
            new_cursor_pos = text_buffer.get_iter_at_offset(
                redo_action.offset + redo_action.length)
            text_buffer.place_cursor(new_cursor_pos)
        else:
            start = text_buffer.get_iter_at_offset(redo_action.start)
            stop = text_buffer.get_iter_at_offset(redo_action.end)
            text_buffer.delete(start, stop)
            text_buffer.place_cursor(start)
        self.__end_not_undoable_action()
        self.undo_in_progress = False

    def clear(self):
        self.undo_stack = []
        self.redo_stack = []

    def on_insert_text(self, _text_buffer, text_iter, text, _length):
        """Registers a text insert. Refer to TextBuffer's "insert-text" signal.

        This method must be registered to TextBuffer's "insert-text" signal, or called manually."""

        def can_be_merged(prev, cur):
            """Check if multiple insertions can be merged

            can't merge if prev and cur are not mergeable in the first place
            can't merge when user set the input bar somewhere else
            can't merge across word boundaries"""

            whitespace = (' ', '\t')
            if not cur.mergeable or not prev.mergeable:
                return False
            if cur.offset != (prev.offset + prev.length):
                return False
            if cur.text in whitespace and prev.text not in whitespace:
                return False
            if prev.text in whitespace and cur.text not in whitespace:
                return False
            return True

        if not self.undo_in_progress:
            self.redo_stack = []
        if self.not_undoable_action:
            return

        undo_action = UndoableInsert(text_iter, text, len(text))
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
        """Registers a range deletion. Refer to TextBuffer's "delete-range" signal.

        This method must be registered to TextBuffer's "delete-range" signal, or called manually."""

        def can_be_merged(prev, cur):
            """Check if multiple deletions can be merged

            can't merge if prev and cur are not mergeable in the first place
            can't merge if delete and backspace key were both used
            can't merge across word boundaries"""

            whitespace = (' ', '\t')
            if not cur.mergeable or not prev.mergeable:
                return False
            if prev.delete_key_used != cur.delete_key_used:
                return False
            if prev.start != cur.start and prev.start != cur.end:
                return False
            if cur.text not in whitespace and \
                    prev.text in whitespace:
                return False
            if cur.text in whitespace and \
                    prev.text not in whitespace:
                return False
            return True

        if not self.undo_in_progress:
            self.redo_stack = []
        if self.not_undoable_action:
            return
        undo_action = UndoableDelete(text_buffer, start_iter, end_iter)
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
            if prev_delete.start == undo_action.start:  # delete key used
                prev_delete.text += undo_action.text
                prev_delete.end += (undo_action.end - undo_action.start)
            else:  # Backspace used
                prev_delete.text = "%s%s" % (undo_action.text,
                                             prev_delete.text)
                prev_delete.start = undo_action.start
            self.undo_stack.append(prev_delete)
        else:
            self.undo_stack.append(prev_delete)
            self.undo_stack.append(undo_action)

    def __begin_not_undoable_action(self):
        """Toggle to stop recording actions"""

        self.not_undoable_action = True

    def __end_not_undoable_action(self):
        """Toggle to start recording actions"""

        self.not_undoable_action = False
