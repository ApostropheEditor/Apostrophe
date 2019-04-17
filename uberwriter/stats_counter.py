import math
import re
from queue import Queue
from threading import Thread

from gi.repository import GLib

from uberwriter import helpers


class StatsCounter:
    """Counts characters, words, sentences and reading time using a background thread."""

    # Regexp that matches any character, except for newlines and subsequent spaces.
    CHARACTERS = re.compile(r"[^\s]|(?:[^\S\n](?!\s))")

    # Regexp that matches Asian letters, general symbols and hieroglyphs,
    # as well as sequences of word characters optionally containing non-word characters in-between.
    WORDS = re.compile(r"[\u3040-\uffff]|(?:\w+\S?\w*)+", re.UNICODE)

    # Regexp that matches sentence-ending punctuation characters, ie. full stop, question mark,
    # exclamation mark, paragraph, and variants.
    SENTENCES = re.compile(r"[^\n][.。।෴۔።?՞;⸮؟？፧꘏⳺⳻⁇﹖⁈⁉‽!﹗！՜߹႟᥄\n]+")

    def __init__(self):
        super().__init__()

        self.queue = Queue()
        worker = Thread(target=self.__do_count_stats, name="stats-counter")
        worker.daemon = True
        worker.start()

    def count_stats(self, text, callback):
        """Count stats for text, calling callback with a result when done.

        The callback argument contains the result, in the form:

        (characters, words, sentences, (hours, minutes, seconds))"""

        self.queue.put((text, callback))

    def stop(self):
        """Stops the background worker. StatsCounter shouldn't be used after this."""

        self.queue.put((None, None))

    def __do_count_stats(self):
        while True:
            while True:
                (text, callback) = self.queue.get()
                if text is None and callback is None:
                    return
                if self.queue.empty():
                    break

            text = helpers.pandoc_convert(text, to="plain")

            character_count = len(re.findall(self.CHARACTERS, text))

            word_count = len(re.findall(self.WORDS, text))

            sentence_count = len(re.findall(self.SENTENCES, text))

            dec_, int_ = math.modf(word_count / 200)
            hours = int(int_ / 60)
            minutes = int(int_ % 60)
            seconds = round(dec_ * 0.6)
            reading_time = (hours, minutes, seconds)

            GLib.idle_add(callback, (character_count, word_count, sentence_count, reading_time))
