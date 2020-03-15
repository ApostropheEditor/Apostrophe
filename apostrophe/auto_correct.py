# ApostropheAutoCorrect
# The Apostrophe Auto Correct is a auto correction
# mechanism to prevent stupid typos
# CURRENTLY DISABLED

import os
import pickle
import configparser

import xml.etree.ElementTree as ET

from gi.repository import Gtk, Gdk

import enchant

from apostrophe import pressagio
# import apostrophe.pressagio.predictor
# import apostrophe.pressagio.tokenizer
# import apostrophe.pressagio.dbconnector
# import apostrophe.pressagio.context_tracker
# import apostrophe.pressagio.callback

# from Levenshtein import distance

from apostrophe.helpers import get_media_path

# Define and create PresageCallback object
class PressagioCallback(pressagio.callback.Callback):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def past_stream(self):
        return self.buffer

    def future_stream(self):
        return ''

class AutoCorrect:

    def show_bubble(self, iterator, suggestion):
        self.suggestion = suggestion
        if self.bubble:
            self.bubble_label.set_text(suggestion)
        else:
            pos = self.text_view.get_iter_location(iterator)
            pos_adjusted = self.text_view.buffer_to_window_coords(
                Gtk.TextWindowType.TEXT, pos.x, pos.y + pos.height)
            self.bubble_eventbox = Gtk.EventBox.new()
            self.bubble = Gtk.Grid.new()
            self.bubble.set_name("AutoCorrect")
            self.bubble_eventbox.add(self.bubble)
            self.bubble_eventbox.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
            self.bubble_eventbox.connect("button_press_event", self.clicked_bubble)
            self.text_view.add_child_in_window(self.bubble_eventbox,
                                              Gtk.TextWindowType.TEXT,
                                              pos_adjusted[0], pos_adjusted[1])

            self.bubble_label = Gtk.Label.new(suggestion)

            self.bubble.attach(self.bubble_label, 0, 0, 1, 1)
            self.bubble_close_eventbox = Gtk.EventBox.new()
            self.bubble_close_eventbox.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
            self.bubble_close_eventbox.connect("button_press_event", self.clicked_close)
            close = Gtk.Image.new_from_icon_name('dialog-close', Gtk.IconSize.SMALL_TOOLBAR)
            self.bubble_close_eventbox.add(close)
            self.bubble.attach(self.bubble_close_eventbox, 1, 0, 1, 1)
            self.bubble_eventbox.show_all()

    def clicked_bubble(self, _widget, _data=None):
        self.accept_suggestion()

    def clicked_close(self, _widget, _data=None):
        self.destroy_bubble()

    def suggest(self, stump, context):
        if self.enchant_dict.check(stump):
            self.destroy_bubble()
            return

        self.callback.buffer = ' '.join(context) + ' ' + stump
        self.callback.buffer = self.callback.buffer.lstrip().rstrip()
        predictions = []
        if self.use_pressagio:
            predictions = self.prsgio.predict(6, None)
        prediction = None
        if not predictions:
            if self.enchant_dict.check(stump):
                self.destroy_bubble()
                return
            predictions = self.enchant_dict.suggest(stump)
            suggestions_map = []
            for suggestion in predictions:
                if suggestion in self.frequency_dict:
                    suggestions_map.append({'suggestion': suggestion,
                                            'freq': self.frequency_dict[suggestion]})
                else:
                    suggestions_map.append({'suggestion': suggestion, 'freq': 0})

            suggestions_map.sort(key=lambda x: x['freq'])
            suggestions_map.reverse()
            prediction = suggestions_map[0]
            print(predictions)
            prediction = predictions[0]
        else:
            prediction = predictions[0].word
        anchor_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        anchor_iter.backward_visible_word_start()
        if len(stump) >= 1:
            self.show_bubble(anchor_iter, prediction)

    def destroy_bubble(self, *_args):
        if not self.bubble:
            return
        self.bubble.destroy()
        self.bubble = None
        self.suggestion = ''

    def get_frequency_dict(self, _language):
        self.frequency_dict = {}
        pp_pickled = get_media_path("frequency_dict_" + self.language + ".pickle")
        if pp_pickled and os.path.isfile(pp_pickled):
            frequency_file = open(pp_pickled, 'rb')
            self.frequency_dict = pickle.load(frequency_file)
            frequency_file.close()
        else:
            pp = get_media_path('wordlists/en_us_wordlist.xml')
            frequencies = ET.parse(pp)
            root = frequencies.getroot()
            for child in root:
                self.frequency_dict[child.text] = int(child.attrib['f'])
            frequency_file = open('pickled_dict', 'wb+')
            pickle.dump(self.frequency_dict, frequency_file)
            frequency_file.close()

    def accept_suggestion(self, append=""):
        print("called")
        curr_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        start_iter = curr_iter.copy()
        start_iter.backward_visible_word_start()
        self.buffer.delete(start_iter, curr_iter)
        self.buffer.insert_at_cursor(self.suggestion + append)
        self.destroy_bubble()

    def key_pressed(self, _widget, event):
        if not self.bubble:
            return False
        if event.keyval in [Gdk.KEY_Escape, Gdk.KEY_BackSpace]:
            self.destroy_bubble()
        return False

    def text_insert(self, buffer, location,
                    text, _length, _data=None):
        # check if at end of a word
        # if yes, check if suggestion available
        # then display suggetion
        if self.suggestion and text in [' ', '\t', '\n', '.', '?', '!',
                                        ',', ';', '\'', '"', ')', ':']:
            self.accept_suggestion(append=text)
            location.assign(self.buffer.get_iter_at_mark(self.buffer.get_insert()))
        elif location.ends_word():
            iter_start = location.copy()
            iter_start.backward_visible_word_starts(3)
            text = buffer.get_text(iter_start, location, False)
            words = text.split()
            self.suggest(words[-1], words[0:-1])

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def set_language(self, language):
        print("Language changed to: %s" % language)

        # handle 2 char cases e.g. "en"
        if len(language) == 2:
            if "en":
                language = "en_US"

        if self.language == language:
            return

        self.language = language
        print("Language changing")
        config_file = get_media_path("pressagio_config.ini")
        pres_config = configparser.ConfigParser()
        pres_config.read(config_file)
        pres_config.set("Database", "database",
                        get_media_path("corpora/" + self.language + ".sqlite"))
        self.context_tracker = pressagio.context_tracker.ContextTracker(
            pres_config, self.predictor_registry, self.callback)
        self.prsgio = self.predictor_registry[0]

        self.enchant_dict = enchant.Dict(self.language)

    def __init__(self, textview, textbuffer):
        self.text_view = textview
        self.buffer = textbuffer
        self.suggestion = ""
        self.bubble = self.bubble_label = None
        self.buffer.connect_after('insert-text', self.text_insert)
        self.text_view.connect('key-press-event', self.key_pressed)

        self.language = "en_US"
        self.frequency_dict = {}
        self.get_frequency_dict(self.language)
        self.enchant_dict = enchant.Dict(self.language)

        self.use_pressagio = False
        config_file = get_media_path("pressagio_config.ini")
        pres_config = configparser.ConfigParser()
        pres_config.read(config_file)
        pres_config.set("Database", "database",
                        get_media_path("corpora/" + self.language + ".sqlite"))
        self.callback = PressagioCallback("")

        self.predictor_registry = pressagio.predictor.PredictorRegistry(pres_config)
        self.context_tracker = pressagio.context_tracker.ContextTracker(
            pres_config, self.predictor_registry, self.callback)
        self.prsgio = self.predictor_registry[0]
