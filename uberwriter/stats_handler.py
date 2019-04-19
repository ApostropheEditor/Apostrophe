import math
import re
from gettext import gettext as _
from queue import Queue
from threading import Thread

from gi.repository import GLib, Gio, Gtk

from uberwriter import helpers
from uberwriter.helpers import get_builder
from uberwriter.settings import Settings
from uberwriter.stats_counter import StatsCounter


class StatsHandler:
    """Shows a default statistic on the stats button, and allows the user to toggle which one."""

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
        self.read_time = (0, 0, 0)

        self.settings = Settings.new()
        self.default_stat = self.settings.get_enum("stat-default")

        self.stats_counter = StatsCounter()

        self.update_default_stat()

    def on_stats_button_clicked(self, _button):
        self.stats_button.set_state_flags(Gtk.StateFlags.CHECKED, False)

        menu = Gio.Menu()
        characters_menu_item = Gio.MenuItem.new(self.get_text_for_stat(0), None)
        characters_menu_item.set_action_and_target_value(
            "app.stat_default", GLib.Variant.new_string("characters"))
        menu.append_item(characters_menu_item)
        words_menu_item = Gio.MenuItem.new(self.get_text_for_stat(1), None)
        words_menu_item.set_action_and_target_value(
            "app.stat_default", GLib.Variant.new_string("words"))
        menu.append_item(words_menu_item)
        sentences_menu_item = Gio.MenuItem.new(self.get_text_for_stat(2), None)
        sentences_menu_item.set_action_and_target_value(
            "app.stat_default", GLib.Variant.new_string("sentences"))
        menu.append_item(sentences_menu_item)
        read_time_menu_item = Gio.MenuItem.new(self.get_text_for_stat(3), None)
        read_time_menu_item.set_action_and_target_value(
            "app.stat_default", GLib.Variant.new_string("read_time"))
        menu.append_item(read_time_menu_item)
        self.popover = Gtk.Popover.new_from_model(self.stats_button, menu)
        self.popover.connect('closed', self.on_popover_closed)
        self.popover.popup()

    def on_popover_closed(self, _popover):
        self.stats_button.unset_state_flags(Gtk.StateFlags.CHECKED)

        self.popover = None
        self.text_view.grab_focus()

    def on_text_changed(self, buf):
        self.stats_counter.count(
            buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False),
            self.update_stats)

    def get_text_for_stat(self, stat):
        if stat == 0:
            return _("{:n} Characters".format(self.characters))
        elif stat == 1:
            return _("{:n} Words".format(self.words))
        elif stat == 2:
            return _("{:n} Sentences".format(self.sentences))
        elif stat == 3:
            return _("{:d}:{:02d}:{:02d} Read Time".format(*self.read_time))

    def update_stats(self, stats):
        (characters, words, sentences, read_time) = stats
        self.characters = characters
        self.words = words
        self.sentences = sentences
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
