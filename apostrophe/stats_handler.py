from gettext import gettext as _
from gettext import ngettext

from gi.repository import Gio, GLib, Gtk

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
        
        self.stats_button.connect("destroy", self.on_destroy)

        self.text_view = text_view
        self.text_view.get_buffer().connect("changed", self.on_text_changed)
        # we don't have a better way to check when a selection changes size
        # so we listen to the cursor position and then check if there's a selection
        self.text_view.get_buffer().connect("notify::cursor-position", self.on_text_selected)

        self.characters = 0
        self.words = 0
        self.sentences = 0
        self.paragraphs = 0
        self.read_time = (0, 0, 0)

        self.selected_characters = 0
        self.selected_words = 0
        self.selected_sentences = 0
        self.selected_paragraphs = 0
        self.selected_read_time = (0, 0, 0)

        self.settings = Settings.new()

        self.stats_counter = StatsCounter(self.update_stats)
        self.selected_stats_counter = StatsCounter(self.update_selection_stats)

        self.popover = Gtk.PopoverMenu.new_from_model(Gio.Menu())
        self.popover.set_halign(Gtk.Align.END)
        self.popover.set_margin_end(6)
        self.popover.set_margin_bottom(6)
        self.popover.set_has_arrow(False)
        self.stats_button.set_popover(self.popover)
        self.popover.connect('closed', self.on_popover_closed)

        self.stats_button.set_direction(Gtk.ArrowType.UP)
        self.stats_button.set_create_popup_func(self.on_stats_button_clicked)

        self.update_default_stat()

    def on_stats_button_clicked(self, *args, **kwargs):
        menu = Gio.Menu()
        stats = self.settings.props.settings_schema.get_key(
            "stat-default").get_range()[1]
        for i, stat in enumerate(stats):
            menu_item = Gio.MenuItem.new(self.get_text_for_stat(i), None)
            menu_item.set_action_and_target_value(
                "app.stat_default", GLib.Variant.new_string(stat))
            menu.append_item(menu_item)

        self.popover.set_menu_model(menu)

    def on_popover_closed(self, _popover):
        self.text_view.grab_focus()

    def on_text_changed(self, buf):
        self.stats_counter.count(
            buf.get_text(
                buf.get_start_iter(),
                buf.get_end_iter(),
                False))

    def on_text_selected(self, buf, *args):
        if buf.get_has_selection():
            (start, end) = buf.get_selection_bounds()
            self.selected_stats_counter.count(
                buf.get_text(
                    start,
                    end,
                    False))

    def get_text_for_stat(self, stat):
        if stat == self.CHARACTERS:
            selection_string = _("{:n} of ").format(self.selected_characters) if self.text_view.get_buffer().get_has_selection() else ""
            return selection_string + ngettext("{:n} Character", "{:n} Characters", self.characters).format(self.characters)
        elif stat == self.WORDS:
            selection_string = _("{:n} of ").format(self.selected_words) if self.text_view.get_buffer().get_has_selection() else ""
            return selection_string + ngettext("{:n} Word", "{:n} Words", self.words).format(self.words)
        elif stat == self.SENTENCES:
            selection_string = _("{:n} of ").format(self.selected_sentences) if self.text_view.get_buffer().get_has_selection() else ""
            return selection_string + ngettext("{:n} Sentence", "{:n} Sentences", self.sentences).format(self.sentences)
        elif stat == self.PARAGRAPHS:
            selection_string = _("{:n} of ").format(self.selected_paragraphs) if self.text_view.get_buffer().get_has_selection() else ""
            return selection_string + ngettext("{:n} Paragraph", "{:n} Paragraphs", self.paragraphs).format(self.paragraphs)
        elif stat == self.READ_TIME:
            selection_string = _("{:d}:{:02d}:{:02d} of ").format(*self.selected_read_time) if self.text_view.get_buffer().get_has_selection() else ""
            return selection_string + _("{:d}:{:02d}:{:02d} Read Time").format(*self.read_time)
        else:
            raise ValueError("Unknown stat {}".format(stat))

    def update_stats(self, stats):
        (self.characters,
         self.words,
         self.sentences,
         self.paragraphs,
         self.read_time) = stats
        self.update_default_stat(False)

    def update_selection_stats(self, stats):
        (self.selected_characters,
         self.selected_words,
         self.selected_sentences,
         self.selected_paragraphs,
         self.selected_read_time) = stats
        self.update_default_stat(False)

    def update_default_stat(self, close_popover=True):
        stat = self.settings.get_enum("stat-default")
        text = self.get_text_for_stat(stat)
        self.stats_button.set_label(text)
        if close_popover and self.popover:
            self.popover.popdown()

    def on_destroy(self, _widget):
        self.stats_counter.stop()
        self.selected_stats_counter.stop()
