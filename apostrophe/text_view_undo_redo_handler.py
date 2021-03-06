import logging

LOGGER = logging.getLogger('apostrophe')


class UndoableInsert:
    """Something has been inserted into text_buffer"""

    def __init__(self, text_iter, text, length):
        self.offset = text_iter.get_offset()
        self.text = text
        self.length = length
        self.mergeable = not bool(
            self.length > 1 or self.text in (
                "\r", "\n", " "))

    def undo(self, text_buffer):
        offset = self.offset
        start = text_buffer.get_iter_at_offset(offset)
        stop = text_buffer.get_iter_at_offset(offset + self.length)
        text_buffer.place_cursor(start)
        text_buffer.delete(start, stop)

    def redo(self, text_buffer):
        start = text_buffer.get_iter_at_offset(self.offset)
        text_buffer.insert(start, self.text)
        new_cursor_pos = text_buffer.get_iter_at_offset(
            self.offset + self.length)
        text_buffer.place_cursor(new_cursor_pos)

    def merge(self, next_action):
        """Merge a following action into this insert, if possible

        can't merge if prev is not another insert
        can't merge if prev and cur are not mergeable in the first place
        can't merge when user set the input bar somewhere else
        can't merge across word boundaries"""

        if not isinstance(next_action, UndoableInsert):
            return False
        if not self.mergeable or not next_action.mergeable:
            return False
        if self.offset + self.length != next_action.offset:
            return False
        whitespace = (' ', '\t')
        if self.text in whitespace != next_action.text in whitespace:
            return False

        self.length += next_action.length
        self.text += next_action.text
        return True


class UndoableDelete:
    """Something has been deleted from text_buffer"""

    def __init__(self, text_buffer, start_iter, end_iter):
        self.text = text_buffer.get_text(start_iter, end_iter, False)
        self.start = start_iter.get_offset()
        self.end = end_iter.get_offset()
        # Find out if backspace or delete were used to not mess up redo
        insert_iter = text_buffer.get_iter_at_mark(text_buffer.get_insert())
        self.delete_key_used = bool(insert_iter.get_offset() <= self.start)
        self.mergeable = not bool(
            self.end -
            self.start > 1 or self.text in (
                "\r",
                "\n",
                " "))

    def undo(self, text_buffer):
        start = text_buffer.get_iter_at_offset(self.start)
        text_buffer.insert(start, self.text)
        if self.delete_key_used:
            text_buffer.place_cursor(start)
        else:
            stop = text_buffer.get_iter_at_offset(self.end)
            text_buffer.place_cursor(stop)

    def redo(self, text_buffer):
        start = text_buffer.get_iter_at_offset(self.start)
        stop = text_buffer.get_iter_at_offset(self.end)
        text_buffer.delete(start, stop)
        text_buffer.place_cursor(start)

    def merge(self, next_action):
        """Check if this delete can be merged with a previous action

        can't merge if prev is not another delete
        can't merge if prev and cur are not mergeable in the first place
        can't merge if delete and backspace key were both used
        can't merge across word boundaries"""

        if not isinstance(next_action, UndoableDelete):
            return False
        if not self.mergeable or not next_action.mergeable:
            return False
        if self.delete_key_used != next_action.delete_key_used:
            return False
        if self.start != next_action.start and self.start != next_action.end:
            return False
        whitespace = (' ', '\t')
        if self.text in whitespace != next_action.text in whitespace:
            return False

        if self.delete_key_used:
            self.text += next_action.text
            self.end += (next_action.end - next_action.start)
        else:
            self.text = "%s%s" % (next_action.text, self.text)
            self.start = next_action.start
        return True


class UndoableGroup(list):
    """A list of undoable actions, usually corresponding to a single user action"""

    def undo(self, text_buffer):
        for undoable in reversed(self):
            undoable.undo(text_buffer)

    def redo(self, text_buffer):
        for undoable in self:
            undoable.redo(text_buffer)

    def merge(self, next_action):
        if len(self) == 1:
            return self[0].merge(next_action)
        else:
            return False


class UndoRedoHandler:
    """Manages undo/redo for a given text_buffer.

    Methods can be called directly, as well as be used as signal callbacks."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.current_undo_group = None
        self.undo_in_progress = False

    def undo(self, text_view, _data=None):
        """Undo insertions or deletions. Undone actions are moved to redo stack.

        This method can be registered to a custom undo signal,
        or used independently."""

        if not self.undo_stack:
            return
        self.undo_in_progress = True
        undo_action = self.undo_stack.pop()
        self.redo_stack.append(undo_action)
        undo_action.undo(text_view.get_buffer())
        self.undo_in_progress = False

    def redo(self, text_view, _data=None):
        """Redo insertions or deletions. Redone actions are moved to undo stack

        This method can be registered to a custom redo signal,
        or used independently."""

        if not self.redo_stack:
            return
        self.undo_in_progress = True
        redo_action = self.redo_stack.pop()
        self.undo_stack.append(redo_action)
        redo_action.redo(text_view.get_buffer())
        self.undo_in_progress = False

    def clear(self):
        self.undo_stack = []
        self.redo_stack = []

    def on_begin_user_action(self, _text_buffer):
        """Start of a user action.
        Refer to TextBuffer's "begin-user-action" signal.

        This method must be registered to TextBuffer's
        "begin-user-action" signal, or called
        manually followed by on_end_user_action."""

        self.current_undo_group = UndoableGroup()

    def on_end_user_action(self, _text_buffer):
        """End of a user action.
        Refer to TextBuffer's "end-user-action" signal.

        This method must be registered to TextBuffer's
        "end-user-action" signal, or called
        manually preceded by on_start_user_action."""

        if self.current_undo_group:
            self.undo_stack.append(self.current_undo_group)
        self.current_undo_group = None

    def on_insert_text(self, _text_buffer, text_iter, text, _length):
        """Records a text insert.
        Refer to TextBuffer's "insert-text" signal.

        This method must be registered to TextBuffer's
         "insert-text" signal, or called manually
        in between on_begin_user_action and on_end_user_action."""

        self.__record_undoable(UndoableInsert(text_iter, text, len(text)))

    def on_delete_range(self, text_buffer, start_iter, end_iter):
        """Records a range deletion.
        Refer to TextBuffer's "delete-range" signal.

        This method must be registered to TextBuffer's
         "delete-range" signal, or called manually
        in between on_begin_user_action and on_end_user_action."""

        self.__record_undoable(
            UndoableDelete(
                text_buffer,
                start_iter,
                end_iter))

    def __record_undoable(self, undoable):
        """Records a change, merging it to a previous one if possible."""

        if not self.undo_in_progress:
            self.redo_stack = []
        else:
            return

        prev_group_undoable = self.current_undo_group[-1] if self.current_undo_group else None
        prev_stack_undoable = self.undo_stack[-1] if self.undo_stack else None

        if prev_group_undoable:
            merged = prev_group_undoable.merge(undoable)
        elif prev_stack_undoable:
            merged = prev_stack_undoable.merge(undoable)
        else:
            merged = False

        if not merged:
            if self.current_undo_group is None:
                LOGGER.warning("Recording a change without a user action.")
                self.undo_stack.append(undoable)
            else:
                self.current_undo_group.append(undoable)
