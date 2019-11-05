from gettext import gettext as _

from uberwriter.helpers import user_action


class FormatInserter:
    """Manages insertion of formatting.

    Methods can be called directly, as well as be used as signal callbacks."""

    def insert_italic(self, text_view, _data=None):
        """Insert italic or mark a selection as bold"""

        self.__wrap(text_view, "_", _("italic text"))

    def insert_bold(self, text_view, _data=None):
        """Insert bold or mark a selection as bold"""

        self.__wrap(text_view, "**", _("bold text"))

    def insert_strikethrough(self, text_view, _data=None):
        """Insert strikethrough or mark a selection as strikethrough"""

        self.__wrap(text_view, "~~", _("strikethrough text"))

    def insert_horizontal_rule(self, text_view, _data=None):
        """Insert horizontal rule"""

        text_buffer = text_view.get_buffer()
        with user_action(text_buffer):
            text_buffer.insert_at_cursor("\n\n---\n")
        text_view.scroll_mark_onscreen(text_buffer.get_insert())

    def insert_list_item(self, text_view, _data=None):
        """Insert list item or mark a selection as list item"""

        text_buffer = text_view.get_buffer()
        if text_buffer.get_has_selection():
            (start, end) = text_buffer.get_selection_bounds()
            if start.starts_line():
                with user_action(text_buffer):
                    text = text_buffer.get_text(start, end, False)
                    if text.startswith(("- ", "* ", "+ ")):
                        delete_end = start.copy()
                        delete_end.forward_chars(2)
                        text_buffer.delete(start, delete_end)
                    else:
                        text_buffer.insert(start, "- ")
        else:
            helptext = _("Item")
            text_length = len(helptext)

            cursor_mark = text_buffer.get_insert()
            cursor_iter = text_buffer.get_iter_at_mark(cursor_mark)

            start_ext = cursor_iter.copy()
            start_ext.backward_lines(3)
            text = text_buffer.get_text(cursor_iter, start_ext, False)
            lines = text.splitlines()

            with user_action(text_buffer):
                for line in reversed(lines):
                    if line and line.startswith(("- ", "* ", "+ ")):
                        if cursor_iter.starts_line():
                            text_buffer.insert_at_cursor(line[:2] + helptext)
                        else:
                            text_buffer.insert_at_cursor("\n" + line[:2] + helptext)
                        break
                    else:
                        if not lines[-1] and not lines[-2]:
                            text_buffer.insert_at_cursor("- " + helptext)
                        elif not lines[-1]:
                            if cursor_iter.starts_line():
                                text_buffer.insert_at_cursor("- " + helptext)
                            else:
                                text_buffer.insert_at_cursor("\n- " + helptext)
                        else:
                            text_buffer.insert_at_cursor("\n\n- " + helptext)
                        break

            self.__select_text(text_view, 0, text_length)

    def insert_ordered_list_item(self, _text_view, _data=None):
        # TODO: implement ordered lists
        pass

    def insert_header(self, text_view, _data=None):
        """Insert header or mark a selection as a list header"""

        text_buffer = text_view.get_buffer()
        with user_action(text_buffer):
            if text_buffer.get_has_selection():
                (start, end) = text_buffer.get_selection_bounds()
                text = text_buffer.get_text(start, end, False)
                text_buffer.delete(start, end)
            else:
                text = _("Header")

            text_buffer.insert_at_cursor("#" + " " + text)

        self.__select_text(text_view, 0, len(text))

    @staticmethod
    def __wrap(text_view, wrap, helptext=""):
        """Inserts wrap format to the selected text (helper text when nothing selected)"""
        text_buffer = text_view.get_buffer()
        with user_action(text_buffer):
            if text_buffer.get_has_selection():
                # Find current highlighting
                (start, end) = text_buffer.get_selection_bounds()
                moved = False
                if (start.get_offset() >= len(wrap) and
                        end.get_offset() <= text_buffer.get_char_count() - len(wrap)):
                    moved = True
                    ext_start = start.copy()
                    ext_start.backward_chars(len(wrap))
                    ext_end = end.copy()
                    ext_end.forward_chars(len(wrap))
                    text = text_buffer.get_text(ext_start, ext_end, True)
                else:
                    text = text_buffer.get_text(start, end, True)

                if moved and text.startswith(wrap) and text.endswith(wrap):
                    text = text[len(wrap):-len(wrap)]
                    new_text = text
                    text_buffer.delete(ext_start, ext_end)
                    move_back = 0
                else:
                    if moved:
                        text = text[len(wrap):-len(wrap)]
                    new_text = text.lstrip().rstrip()
                    text = text.replace(new_text, wrap + new_text + wrap)

                    text_buffer.delete(start, end)
                    move_back = len(wrap)

                text_buffer.insert_at_cursor(text)
                text_length = len(new_text)

            else:
                text_buffer.insert_at_cursor(wrap + helptext + wrap)
                text_length = len(helptext)
                move_back = len(wrap)

        cursor_mark = text_buffer.get_insert()
        cursor_iter = text_buffer.get_iter_at_mark(cursor_mark)
        cursor_iter.backward_chars(move_back)
        text_buffer.move_mark_by_name('selection_bound', cursor_iter)
        cursor_iter.backward_chars(text_length)
        text_buffer.move_mark_by_name('insert', cursor_iter)

    @staticmethod
    def __select_text(text_view, offset, length):
        """Selects text starting at the current cursor minus offset, length characters."""

        text_buffer = text_view.get_buffer()
        cursor_mark = text_buffer.get_insert()
        cursor_iter = text_buffer.get_iter_at_mark(cursor_mark)
        cursor_iter.backward_chars(offset)
        text_buffer.move_mark_by_name('selection_bound', cursor_iter)
        cursor_iter.backward_chars(length)
        text_buffer.move_mark_by_name('insert', cursor_iter)
