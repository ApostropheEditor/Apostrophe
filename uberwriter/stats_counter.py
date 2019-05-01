import math
import re
from queue import Queue
from threading import Thread

from gi.repository import GLib

from uberwriter import helpers


class StatsCounter:
    """Counts characters, words, sentences and read time using a background thread."""

    # Regexp that matches characters, with the following exceptions:
    # * Newlines
    # * Sequential spaces
    # * Sequential dashes
    CHARACTERS = re.compile(r"[^\s-]|(?:[^\S\n](?!\s)|-(?![-\n]))")

    # Regexp that matches Asian letters, general symbols and hieroglyphs,
    # as well as sequences of word characters optionally containing non-word characters in-between.
    WORDS = re.compile(r"[\u3040-\uffff]|(?:\w+\S?\w*)+", re.UNICODE)

    # Regexp that matches sentence-ending punctuation characters, ie. full stop, question mark,
    # exclamation mark, paragraph, and variants.
    SENTENCES = re.compile(r"[^\n][.。।෴۔።?՞;⸮؟？፧꘏⳺⳻⁇﹖⁈⁉‽!﹗！՜߹႟᥄\n]+")

    # Regexp that matches paragraphs, ie. anything separated by newlines.
    PARAGRAPHS = re.compile(r".+\n?")

    def __init__(self):
        super().__init__()

        self.queue = Queue()
        worker = Thread(target=self.__do_count, name="stats-counter")
        worker.daemon = True
        worker.start()

    def count(self, text, callback):
        """Count stats for text, calling callback with a result when done.

        The callback argument contains the result, in the form:

        (characters, words, sentences, (hours, minutes, seconds))"""

        self.queue.put((text, callback))

    def stop(self):
        """Stops the background worker. StatsCounter shouldn't be used after this."""

        self.queue.put((None, None))

    def __do_count(self):
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

            paragraph_count = len(re.findall(self.PARAGRAPHS, text))

            read_m, read_s = divmod(word_count / 200 * 60, 60)
            read_h, read_m = divmod(read_m, 60)
            read_time = (int(read_h), int(read_m), int(read_s))

            GLib.idle_add(
                callback,
                (character_count, word_count, sentence_count, paragraph_count, read_time))
