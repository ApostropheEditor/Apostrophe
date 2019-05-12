from queue import Queue
from threading import Thread

from gi.repository import GLib

from uberwriter import helpers
from uberwriter.theme import Theme


class PreviewConverter:
    """Converts markdown to html using a background thread."""

    def __init__(self):
        super().__init__()

        self.queue = Queue()
        worker = Thread(target=self.__do_convert, name="preview-converter")
        worker.daemon = True
        worker.start()

    def convert(self, text, callback, *user_data):
        """Converts text to html, calling callback when done.

        The callback argument contains the result."""

        self.queue.put((text, callback, user_data))

    def stop(self):
        """Stops the background worker. PreviewConverter shouldn't be used after this."""

        self.queue.put((None, None))

    def __do_convert(self):
        while True:
            while True:
                (text, callback, user_data) = self.queue.get()
                if text is None and callback is None:
                    return
                if self.queue.empty():
                    break

            args = ['--standalone',
                    '--mathjax',
                    '--css=' + Theme.get_current().web_css_path,
                    '--lua-filter=' + helpers.get_script_path('relative_to_absolute.lua'),
                    '--lua-filter=' + helpers.get_script_path('task-list.lua')]
            text = helpers.pandoc_convert(text, to="html5", args=args)

            GLib.idle_add(callback, text, *user_data)
