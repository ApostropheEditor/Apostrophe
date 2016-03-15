from gi.repository import Gtk, Gio

from . import bibtexparser
from . import fuzzywuzzy

from .gi_composites import GtkTemplate


@GtkTemplate(ui='/home/wolfv/Programs/uberwriter/uberwriter/plugins/bibtex/bibtex_item.glade')
class BibTexItem(Gtk.Box):

    __gtype_name__ = 'BibTexItem'

    title_label = GtkTemplate.Child()
    author_label = GtkTemplate.Child()
    other_label = GtkTemplate.Child()

    def __init__(self, data): 
        super(Gtk.Box, self).__init__()
        # This must occur *after* you initialize your base
        self.init_template()
        self.title_label.set_text(data['title'])
        self.author_label.set_text(data.get('author'))
        self.other_label.set_text(data.get('year') if data.get('year') else 'N/A')


class BibTex(object):
    """docstring for Handler"""

    def open_bibtex(self, event, *args):
        self.match()
        self.window.show_all()
        # self.window.set_transient(True)
        # self.window.set_modal(True)

    def get_widget_for_box(self, word):
        return Gtk.Label(word)

    def real_row_activated(self, row, data=None):
        print("A row was activated!!")
        self.app.TextBuffer.insert_at_cursor('[@' + data + ']')
        self.close()
        print(data)

    def row_activated(self, widget, row, data=None):
        # row.activate()
        return

    def match(self, word=None):
        self.rows = []
        for i in self.bib_db.entries:
            row  = Gtk.ListBoxRow()
            item = BibTexItem(i)
            row.add(item)
            row.set_activatable(True)
            row.connect('activate', self.real_row_activated, i['ID'])
            self.rows.append(row)
            self.listview.add(row)

        # self.listview.add(Gtk.Label('test'))
        # self.listview.bind_model(a, self.get_widget_for_box)
        self.listview.show_all()

    def __init__(self, app):
        self.app = app
        self.app.connect('toggle_bibtex', self.open_bibtex)
        with open('/home/wolfv/ownCloud/Studium/Semester Project/Report/listb.bib') as f:
            self.bib_db = bibtexparser.load(f)

        builder = Gtk.Builder()
        builder.add_from_file('/home/wolfv/Programs/uberwriter/uberwriter/plugins/bibtex/bibtex.glade')
        self.window = builder.get_object('bibtex_window')
        self.window.set_transient_for(self.app)
        self.window.set_modal(True)
        self.listview = builder.get_object('listbox')