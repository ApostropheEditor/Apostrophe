from gettext import gettext as _
from gettext import ngettext

from gi.repository import GLib, Gio, Gtk

from apostrophe.settings import Settings
from apostrophe.stats_counter import StatsCounter


class StatsHandler:
    """Shows a default statistic on the stats button,
    and allows the user to toggle which one."""

    # Must match the order/index defined in gschema.xml
    CHARACTERS = 0
    WORDS = 1
    SENTENCES = 2
    PARAGRAPHS = 3
    READ_TIME = 4

    def __init__(self, stats_button, text_view):
        super().__init__()

        self.stats_button = stats_button
        self.stats_button.connect("clicked", self.on_stats_button_clicked)
        self.stats_button.connect("destroy", self.on_destroy)

        self.text_view = text_view
        self.text_view.get_buffer().connect("changed", self.on_text_changed)

        self.popover = None

        self.characters = 0
        self.words = 0
        self.sentences = 0
        self.paragraphs = 0
        self.read_time = (0, 0, 0)

        self.settings = Settings.new()

        self.stats_counter = StatsCounter(self.update_stats)

        self.update_default_stat()

    def on_stats_button_clicked(self, _button):
        self.stats_button.set_state_flags(Gtk.StateFlags.CHECKED, False)

        menu = Gio.Menu()
        stats = self.settings.props.settings_schema.get_key(
            "stat-default").get_range()[1]
        for i, stat in enumerate(stats):
            menu_item = Gio.MenuItem.new(self.get_text_for_stat(i), None)
            menu_item.set_action_and_target_value(
                "app.stat_default", GLib.Variant.new_string(stat))
            menu.append_item(menu_item)
        self.popover = Gtk.Popover.new_from_model(self.stats_button, menu)
        self.popover.connect('closed', self.on_popover_closed)
        self.popover.popup()

    def on_popover_closed(self, _popover):
        self.stats_button.unset_state_flags(Gtk.StateFlags.CHECKED)

        self.popover = None
        self.text_view.grab_focus()

    def on_text_changed(self, buf):
        self.stats_counter.count(
            buf.get_text(
                buf.get_start_iter(),
                buf.get_end_iter(),
                False))

    def get_text_for_stat(self, stat):
        if stat == self.CHARACTERS:
            return ngettext("{:n} Character", "{:n} Characters", self.characters).format(self.characters)
        elif stat == self.WORDS:
            return ngettext("{:n} Word", "{:n} Words", self.words).format(self.words)
        elif stat == self.SENTENCES:
            return ngettext("{:n} Sentence", "{:n} Sentences", self.sentences).format(self.sentences)
        elif stat == self.PARAGRAPHS:
            return ngettext("{:n} Paragraph", "{:n} Paragraphs", self.paragraphs).format(self.paragraphs)
        elif stat == self.READ_TIME:
            return _("{:d}:{:02d}:{:02d} Read Time").format(*self.read_time)
        else:
            raise ValueError("Unknown stat {}".format(stat))

    def update_stats(self, stats):
        (characters, words, sentences, paragraphs, read_time) = stats
        self.characters = characters
        self.words = words
        self.sentences = sentences
        self.paragraphs = paragraphs
        self.read_time = read_time
        self.update_default_stat(False)

    def update_default_stat(self, close_popover=True):
        stat = self.settings.get_enum("stat-default")
        text = self.get_text_for_stat(stat)
        self.stats_button.set_label(text)
        if close_popover and self.popover:
            self.popover.popdown()

    def on_destroy(self, _widget):
        self.stats_counter.stop()
