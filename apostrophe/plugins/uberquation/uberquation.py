from gi.repository import Gtk, Gdk
import subprocess

import threading
import time
import uuid

import os

from fuzzywuzzy import fuzz, process
FNULL = open(os.devnull, 'w')

objs = {
    "Decorations": [
        {
            "name": "Superscript",
            "tex": "$^{0}"
        },
        {
            "name": "Subscript",
            "tex": "$_{0}"
        }
    ],
    "Greek": [
        {
            "name": "Alpha",
            "tex": "\\alpha"
        },
        {
            "name": "Beta",
            "tex": "\\beta"
        }
     ],
     "Math": [
        {
            "name": "Integral",
            "tex": "\\int_{0}^{1}{2}"
        }
     ],
     "Arrows": [
        {
            "name": "Rightarrow",
            "tex": "\\Rightarrow"
        }
     ]
}

def get_svg(text):
    fn = uuid.uuid4()
    f = open("/tmp/{0}.tex".format(fn), "w+")
    f.write("""%&latex
    \\documentclass{standalone}
    \\pagestyle{empty}
    \\begin{document}
    $""")
    f.write(text)
    f.write("""$
    \\end{document}
    """)
    f.close()

    subprocess.call(['pdftex', '-output-directory=/tmp',
                      '-interaction=nonstopmode', '/tmp/{0}.tex'.format(fn)],stdout=FNULL)
    subprocess.call(['dvisvgm', '--no-fonts', '--scale=2', '/tmp/{0}.dvi'.format(fn),
                     '-o', '/tmp/{0}.svg'.format(fn)],stdout=FNULL)


    return "/tmp/{0}.svg".format(fn)

class Handler:

    def __init__(self, b):
        self.b = b
        self.current_search = ""

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def recompile_image(self, buffer):
        def recomp():
            text = buffer.get_text(buffer.get_start_iter(),
                               buffer.get_end_iter(), False)
            svgfn = get_svg(text)
            im = self.b.get_object("image1")
            im.set_from_file(svgfn)
        self.thread = threading.Thread(target=recomp)
        self.thread.daemon = False
        self.thread.start()

    def alpha_clicked(self, button):
        bf = self.b.get_object("textbuffer1")
        bf.insert_at_cursor("\\alpha")

    def searchentry_changed(self, widget, data=None):
        self.current_search = widget.get_text().lower()
        self.b.get_object("listbox").invalidate_filter()

    def sort_func(self, row_a, row_b, data=None):
        if self.b.get_object("searchentry1").get_text():
            if fuzz.partial_ratio(self.current_search, row_a.entry_name.lower()) > \
                fuzz.partial_ratio(self.current_search, row_b.entry_name.lower()):
                return False
            else:
                return True
        return False

    def filter_func(self, row, data=None):

        if fuzz.partial_ratio(self.current_search, row.entry_name.lower()) < 80:
            return False 
        # if not row.entry_name.startswith(self.b.get_object("searchentry1").get_text()):
        #     return False
        return True



    def textview_key_pressed(self, widget, key, data=None):
        if key.keyval == Gdk.KEY_Tab:
            print("\n\nTAB PRESSED\n\n")

            # Tab Key:
            # Move forward to next open curly bracket and 
            # highlight all text up to the next closing curly bracket

            buf = widget.get_buffer()
            cursor_iter = buf.get_iter_at_mark(buf.get_insert())
            cursor_iter.forward_find_char(lambda x, data: x == "{", None, None)
            bound = cursor_iter.copy()
            bound.forward_chars(3)
            buf.move_mark_by_name("insert", cursor_iter)
            buf.move_mark_by_name("selection_bound", bound)

            return True


    def textview_after_key_pressed(self, widget, key, data=None):
            print("\n\ntestign for context")
            buf = widget.get_buffer()
            cursor_iter = buf.get_iter_at_mark(buf.get_insert())
            start_iter = cursor_iter.copy()
            start_iter.backward_word_start()
            start_iter.backward_cursor_position()
            current_context = buf.get_text(start_iter, cursor_iter, False)
            print("Current Context: ", current_context)
            if current_context.startswith("\\"):
                print("in context!!")
                # we are in some latex specific context so we should try to complete
                # whatever is going on :)
                self.current_search = current_context.lower()[1:]
                self.b.get_object("listbox").invalidate_filter()
                




def create_icons(builder):
    import shutil
    import re
    tb = builder.get_object("textbuffer1")
    menu = Gtk.Menu.new()
    try:
        os.makedirs("./icons")
    except:
        pass

    def insert_tex_snippet(widget, row, data=None):
        tb.insert_at_cursor(row.tex_data)

    lb = builder.get_object("listbox")
    from gi.repository import GObject
    for obj in objs:
        for val in objs[obj]:
            tex_code = val["tex"]
            tex_code = tex_code.format(*"abcdefghijklmn")
            tex_code = re.sub("\$", "x", tex_code)
            icon_fn = "./icons/" + re.sub(r"[\\\$]", "", val["tex"])
            im_exists = os.path.exists(icon_fn)
            if not im_exists:
                svg_filename = get_svg(tex_code)
                shutil.copy(svg_filename, icon_fn)

            bx = Gtk.ListBoxRow.new()
            bx.tex_data = val["tex"]
            bx.entry_name = val["name"]

            hbox =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            hbox.pack_start(Gtk.Image.new_from_file(icon_fn), True, True, 0)
            hbox.pack_start(Gtk.Label(val["tex"]), True, True, 0)
            hbox.show_all()

            bx.add(hbox)
            lb.add(bx)

    lb.connect("row-activated", insert_tex_snippet)
    return menu

    pass


def run():
    builder = Gtk.Builder()
    builder.add_from_file("equation_widget.glade")
    menu = create_icons(builder)
    #menu.show_all()

    l = builder.get_object("listbox")

    window = builder.get_object("window1")
    window.show_all()
    handlers = Handler(builder)
    builder.connect_signals(handlers)
    l.set_filter_func(handlers.filter_func)
    l.set_sort_func(handlers.sort_func)
    Gtk.main()


if __name__ == "__main__":
    run()
