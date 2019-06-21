import mimetypes
import urllib

from gi.repository import Gtk

(TARGET_URI, TARGET_TEXT) = range(2)


class DragDropHandler:
    TARGET_URI = None

    def __init__(self, text_view, *targets):
        super().__init__()

        self.target_list = Gtk.TargetList.new([])
        if TARGET_URI in targets:
            self.target_list.add_uri_targets(TARGET_URI)
        if TARGET_TEXT in targets:
            self.target_list.add_text_targets(TARGET_TEXT)

        text_view.drag_dest_set_target_list(self.target_list)
        text_view.connect_after('drag-data-received', self.on_drag_data_received)

    def on_drag_data_received(self, text_view, drag_context, _x, _y, data, info, time):
        """Handle drag and drop events"""

        text_buffer = text_view.get_buffer()
        if info == TARGET_URI:
            uris = data.get_uris()
            for uri in uris:
                mime = mimetypes.guess_type(uri)

                if mime[0] is not None and mime[0].startswith('image'):
                    text = "![Image caption](%s)" % uri
                    limit_left = 2
                    limit_right = 23
                else:
                    text = "[Link description](%s)" % uri
                    limit_left = 1
                    limit_right = 22
                text_buffer.place_cursor(text_buffer.get_iter_at_mark(
                    text_buffer.get_mark('gtk_drag_target')))
                text_buffer.insert_at_cursor(text)
                insert_mark = text_buffer.get_insert()
                selection_bound = text_buffer.get_selection_bound()
                cursor_iter = text_buffer.get_iter_at_mark(insert_mark)
                cursor_iter.backward_chars(len(text) - limit_left)
                text_buffer.move_mark(insert_mark, cursor_iter)
                cursor_iter.forward_chars(limit_right)
                text_buffer.move_mark(selection_bound, cursor_iter)

        elif info == TARGET_TEXT:
            text_buffer.place_cursor(text_buffer.get_iter_at_mark(
                text_buffer.get_mark('gtk_drag_target')))
            text_buffer.insert_at_cursor(data.get_text())

        Gtk.drag_finish(drag_context, True, True, time)
        text_view.get_toplevel().present_with_time(time)
        return False
