import mimetypes
import urllib
from gettext import gettext as _
from os.path import basename
from uberwriter.settings import Settings

from gi.repository import Gtk

(TARGET_URI, TARGET_TEXT) = range(2)


class DragDropHandler:
    TARGET_URI = None

    def __init__(self, text_view, *targets):
        super().__init__()

        self.settings = Settings.new()

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
                name = basename(urllib.parse.unquote_plus(uri))
                mime = mimetypes.guess_type(uri)

                if mime[0] is not None and mime[0].startswith('image/'):
                    basepath = self.settings.get_string("open-file-path")
                    basepath = urllib.parse.quote(basepath)

                    if uri.startswith("file://"):
                        uri = uri[7:]

                    # for handling local URIs we need to substract the basepath
                    # except when it is "/" (document not saved)
                    if uri.startswith(basepath) and basepath != "/":
                        uri = uri[len(basepath)+1:]

                    text = "![{}]({})".format(name, uri)
                    limit_left = 2
                    limit_right = len(name)
                else:
                    text = "[{}]({})".format(name, uri)
                    limit_left = 1
                    limit_right = len(name)

        elif info == TARGET_TEXT:
            text = data.get_text()

            # delete automatically added DnD text
            insert_mark = text_buffer.get_insert()
            cursor_iter_r = text_buffer.get_iter_at_mark(insert_mark)
            cursor_iter_l = cursor_iter_r.copy()
            cursor_iter_l.backward_chars(len(data.get_text()))

            text_buffer.delete(cursor_iter_l, cursor_iter_r)

            if text.startswith(("http://", "https://", "www.")):
                text = "[{}]({})".format(_("web page"), text)
                limit_left = 1
                limit_right = len(_("web page"))
            else:
                limit_left = 0
                limit_right = 0

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

        Gtk.drag_finish(drag_context, True, True, time)
        text_view.get_toplevel().present_with_time(time)
        return False
