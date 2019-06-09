import re
from multiprocessing import Process, Pipe

from gi.repository import GLib

from uberwriter.markup_regex import ITALIC, BOLD_ITALIC, BOLD, STRIKETHROUGH, IMAGE, LINK, \
    HORIZONTAL_RULE, LIST, MATH, TABLE, CODE_BLOCK, HEADER_UNDER, HEADER, BLOCK_QUOTE, ORDERED_LIST, \
    FOOTNOTE_ID, FOOTNOTE


class StatsCounter:
    """Counts characters, words, sentences and read time using a worker process."""

    # Regexp that matches any character, except for newlines and subsequent spaces.
    CHARACTERS = re.compile(r"[^\s]|(?:[^\S\n](?!\s))")

    # Regexp that matches Asian letters, general symbols and hieroglyphs,
    # as well as sequences of word characters optionally containing non-word characters in-between.
    WORDS = re.compile(r"[\u3040-\uffff]|(?:\w+\S?\w*)+", re.UNICODE)

    # Regexp that matches sentence-ending punctuation characters, ie. full stop, question mark,
    # exclamation mark, paragraph, and variants.
    SENTENCES = re.compile(r"[^\n][.。।෴۔።?՞;⸮؟？፧꘏⳺⳻⁇﹖⁈⁉‽!﹗！՜߹႟᥄\n]+")

    # Regexp that matches paragraphs, ie. anything separated by at least 2 newlines.
    PARAGRAPHS = re.compile(r"[^\n]+(\n{2,}|$)")

    # List of regexp whose matches should be replaced by their "text" group. Order is important.
    MARKUP_REGEXP_REPLACE = (
        BOLD_ITALIC, ITALIC, BOLD, STRIKETHROUGH, IMAGE, LINK, LIST, ORDERED_LIST, BLOCK_QUOTE,
        HEADER, HEADER_UNDER, CODE_BLOCK, TABLE, MATH, FOOTNOTE_ID, FOOTNOTE
    )

    # List of regexp whose matches should be removed. Order is important.
    MARKUP_REGEXP_REMOVE = (
        HORIZONTAL_RULE,
    )

    def __init__(self, callback):
        super().__init__()

        # Worker process to handle counting.
        self.counting = False
        self.count_pending_text = None
        self.parent_conn, child_conn = Pipe()
        Process(target=self.do_count, args=(child_conn,), daemon=True).start()
        GLib.io_add_watch(
            self.parent_conn.fileno(), GLib.PRIORITY_LOW, GLib.IO_IN, self.on_counted, callback)

    def count(self, text):
        """Count stats for text.

        In case counting is already running, it will re-count once it finishes. This ensure that
        the pipe doesn't fill (and block) if multiple requests are made in quick succession."""

        if not self.counting:
            self.counting = True
            self.count_pending_text = None
            self.parent_conn.send(text)
        else:
            self.count_pending_text = text

    def do_count(self, child_conn):
        """Counts stats in a worker process.
        
        The result is in the format: (characters, words, sentences, (hours, minutes, seconds))"""

        while True:
            while True:
                try:
                    text = child_conn.recv()
                    if not child_conn.poll():
                        break
                except EOFError:
                    child_conn.close()
                    return

            for regexp in self.MARKUP_REGEXP_REPLACE:
                text = re.sub(regexp, r"\g<text>", text)
            for regexp in self.MARKUP_REGEXP_REMOVE:
                text = re.sub(regexp, "", text)

            character_count = len(re.findall(self.CHARACTERS, text))

            word_count = len(re.findall(self.WORDS, text))

            sentence_count = len(re.findall(self.SENTENCES, text))

            paragraph_count = len(re.findall(self.PARAGRAPHS, text))

            read_m, read_s = divmod(word_count / 200 * 60, 60)
            read_h, read_m = divmod(read_m, 60)
            read_time = (int(read_h), int(read_m), int(read_s))

            child_conn.send(
                (character_count, word_count, sentence_count, paragraph_count, read_time))

    def on_counted(self, _source, _condition, callback):
        """Reads the counting result from the pipe and triggers any pending count."""

        self.counting = False
        if self.count_pending_text is not None:
            self.count(self.count_pending_text)  # self.count clears the pending text.

        try:
            if self.parent_conn.poll():
                callback(self.parent_conn.recv())
            return True
        except EOFError:
            return False

    def stop(self):
        """Stops the worker process. StatsCounter shouldn't be used after this."""

        self.parent_conn.close()
