# Copyright (C) 2022, Manuel Genovés <manuel.genoves@gmail.com>
#               2019, Wolf Vollprecht <w.vollprecht@gmail.com>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
# END LICENSE

import os
import re
import telnetlib
from gettext import gettext as _
from urllib.parse import unquote

import gi

gi.require_version("Gtk", "4.0")
# gi.require_version("WebKit2", "4.0")
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk

# from gi.repository import WebKit2
from apostrophe import latex_to_PNG, markup_regex
from apostrophe.settings import Settings


class DictAccessor:
    reEndResponse = re.compile(br"^[2-5][0-58][0-9] .*\r\n$", re.DOTALL +
                               re.MULTILINE)
    reDefinition = re.compile(br"^151(.*?)^\.", re.DOTALL + re.MULTILINE)

    def __init__(self, host="dict.dict.org", port=2628, timeout=60):
        self.telnet = telnetlib.Telnet(host, port)
        self.timeout = timeout
        self.login_response = self.telnet.expect([self.reEndResponse],
                                                 self.timeout)[2]

    def run_command(self, cmd):
        self.telnet.write(cmd.encode("utf-8") + b"\r\n")
        return self.telnet.expect([self.reEndResponse], self.timeout)[2]

    def get_matches(self, database, strategy, word):
        if database in ["", "all"]:
            d = "*"
        else:
            d = database
        if strategy in ["", "default"]:
            s = "."
        else:
            s = strategy
        w = word.replace("\"", r"\\\"")
        tsplit = self.run_command(
            "MATCH {} {} \"{}\"".format(
                d, s, w)).splitlines()
        mlist = list()
        if tsplit[-1].startswith(b"250 ok") and tsplit[0].startswith(b"1"):
            mlines = tsplit[1:-2]
            for line in mlines:
                lsplit = line.strip().split()
                db = lsplit[0]
                word = unquote(" ".join(lsplit[1:]))
                mlist.append((db, word))
        return mlist

    def get_definition(self, database, word):
        if database in ["", "all"]:
            d = "*"
        else:
            d = database
        w = word.replace("\"", r"\\\"")
        dsplit = self.run_command(
            "DEFINE {} \"{}\"".format(
                d, w)).splitlines(True)

        dlist = list()
        if dsplit[-1].startswith(b"250 ok") and dsplit[0].startswith(b"1"):
            dlines = dsplit[1:-1]
            dtext = b"".join(dlines)
            dlist = [dtext]
        return dlist

    def close(self):
        t = self.run_command("QUIT")
        self.telnet.close()
        return t

    def parse_wordnet(self, response):
        # consisting of group (n,v,adj,adv)
        # number, description, examples, synonyms, antonyms

        lines = response.splitlines()
        lines = lines[2:]
        lines = " ".join(lines)
        lines = re.sub(r"\s+", " ", lines).strip()
        lines = re.split(r"( adv | adj | n | v |^adv |^adj |^n |^v )", lines)
        res = []
        act_res = {"defs": [], "class": "none", "num": "None"}
        for l in lines:
            l = l.strip()
            if not l:
                continue
            if l in ["adv", "adj", "n", "v"]:
                if act_res:
                    res.append(act_res.copy())
                act_res = {"defs": [], "class": l}
            else:
                ll = re.split(r"(?: |^)(\d): ", l)
                act_def = {}
                for lll in ll:
                    if lll.strip().isdigit() or not lll.strip():
                        if "description" in act_def and act_def["description"]:
                            act_res["defs"].append(act_def.copy())
                        act_def = {"num": lll}
                        continue
                    a = re.findall(r"(\[(syn|ant): (.+?)\] ??)+", lll)
                    for n in a:
                        if n[1] == "syn":
                            act_def["syn"] = re.findall(r"{(.*?)}.*?", n[2])
                        else:
                            act_def["ant"] = re.findall(r"{(.*?)}.*?", n[2])
                    tbr = re.search(r"\[.+\]", lll)
                    if tbr:
                        lll = lll[:tbr.start()]
                    lll = lll.split(";")
                    act_def["examples"] = []
                    act_def["description"] = []
                    for llll in lll:
                        llll = llll.strip()
                        if llll.strip().startswith("\""):
                            act_def["examples"].append(llll)
                        else:
                            act_def["description"].append(llll)
                if act_def and "description" in act_def:
                    act_res["defs"].append(act_def.copy())

        res.append(act_res.copy())
        return res


def get_dictionary(term):
    da = DictAccessor()
    output = da.get_definition("wn", term)
    if output:
        output = output[0]
    else:
        return None
    return da.parse_wordnet(output.decode(encoding="UTF-8"))


class InlinePreview:
    WIDTH = 400
    HEIGHT = 300

    def __init__(self, text_view):
        self.settings = Settings.new()

        self.text_view = text_view
        self.text_view.gesture_controller.connect("pressed",
                                                   self.on_button_press_event)
        self.text_buffer = text_view.get_buffer()
        self.cursor_mark = self.text_buffer.create_mark(
            "click",
            self.text_buffer.get_iter_at_mark(self.text_buffer.get_insert()))

        self.latex_converter = latex_to_PNG.LatexToPNG()
        self.characters_per_line = self.settings.get_int("characters-per-line")

        self.popover = Gtk.Popover.new(self.text_view)
        self.popover.get_style_context().add_class("quick-preview-popup")
        self.popover.set_modal(True)

        self.preview_fns = {
            markup_regex.MATH: self.get_view_for_math,
            markup_regex.IMAGE: self.get_view_for_image,
            markup_regex.LINK: self.get_view_for_link,
            markup_regex.LINK_ALT: self.get_view_for_link,
            markup_regex.FOOTNOTE_ID: self.get_view_for_footnote,
            re.compile(r"(?P<text>\w+)"): self.get_view_for_lexikon
        }

    def on_button_press_event(self, _text_view, event):
        if event.button == 1 and event.state & Gdk.ModifierType.CONTROL_MASK:
            x, y = self.text_view.window_to_buffer_coords(2, int(event.x),
                                                          int(event.y))
            self.text_buffer.move_mark(
                self.cursor_mark,
                self.text_view.get_iter_at_location(x, y).iter)
            self.open_popover(self.text_view)

    def get_view_for_math(self, match):
        success, result = self.latex_converter.generatepng(match.group("text"))
        if success:
            return Gtk.Image.new_from_file(result)
        else:
            error = _("Formula looks incorrect:")
            error += "\n\n“{}”".format(result)
            return Gtk.Label(label=error)

    def get_view_for_image(self, match):
        path = match.group("url")

        if path.startswith(("https://", "http://", "www.")):
            return self.get_view_for_link(match)
        if path.startswith(("file://")):
            path = path[7:]
        if not path.startswith(("/", "file://")):
            path = os.path.join(
                self.settings.get_string("open-file-path"), path)
        path = unquote(path)

        return Gtk.Image.new_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_size(path, self.WIDTH,
                                                   self.HEIGHT))

    def get_view_for_link(self, match):
        return
        url = match.group("url")
        web_view = WebKit2.WebView(zoom_level=0.3125)  # ~1280x960
        web_view.set_size_request(self.WIDTH, self.HEIGHT)
        if GLib.uri_parse_scheme(url) is None:
            url = "http://{}".format(url)
        web_view.load_uri(url)
        return web_view

    def get_view_for_footnote(self, match):
        footnote_id = match.group("id")
        fn_matches = re.finditer(
            markup_regex.FOOTNOTE,
            self.text_buffer.props.text)
        for fn_match in fn_matches:
            if fn_match.group("id") == footnote_id:
                if fn_match:
                    footnote = re.sub("\n[\t ]+", "\n", fn_match.group("text"))
                else:
                    footnote = _("No matching footnote found")
                label = Gtk.Label(label=footnote)
                label.set_max_width_chars(self.characters_per_line)
                label.set_line_wrap(True)
                return label
        return None

    def get_view_for_lexikon(self, match):
        term = match.group("text")
        lexikon_dict = get_dictionary(term)
        if lexikon_dict:
            grid = Gtk.Grid.new()
            grid.get_style_context().add_class("lexikon")
            grid.set_row_spacing(2)
            grid.set_column_spacing(4)
            i = 0
            for entry in lexikon_dict:
                if not entry["defs"]:
                    continue
                elif entry["class"].startswith("n"):
                    word_type = _("noun")
                elif entry["class"].startswith("v"):
                    word_type = _("verb")
                elif entry["class"].startswith("adj"):
                    word_type = _("adjective")
                elif entry["class"].startswith("adv"):
                    word_type = _("adverb")
                else:
                    continue

                vocab_label = Gtk.Label.new(term + " ~ " + word_type)
                vocab_label.get_style_context().add_class("header")
                if i == 0:
                    vocab_label.get_style_context().add_class("first")
                vocab_label.set_halign(Gtk.Align.START)
                vocab_label.set_justify(Gtk.Justification.LEFT)
                grid.attach(vocab_label, 0, i, 3, 1)

                for definition in entry["defs"]:
                    i = i + 1
                    num_label = Gtk.Label.new(definition["num"] + ".")
                    num_label.get_style_context().add_class("number")
                    num_label.set_valign(Gtk.Align.START)
                    grid.attach(num_label, 0, i, 1, 1)

                    def_label = Gtk.Label(
                        label=" ".join(
                            definition["description"]))
                    def_label.get_style_context().add_class("description")
                    def_label.set_halign(Gtk.Align.START)
                    def_label.set_max_width_chars(self.characters_per_line)
                    def_label.set_line_wrap(True)
                    def_label.set_justify(Gtk.Justification.FILL)
                    grid.attach(def_label, 1, i, 1, 1)
                i = i + 1
            if i > 0:
                return grid
        return None

    def open_popover(self, _editor, _data=None):
        start_iter = self.text_buffer.get_iter_at_mark(self.cursor_mark)
        line_offset = start_iter.get_line_offset()
        end_iter = start_iter.copy()
        start_iter.set_line_offset(0)
        end_iter.forward_to_line_end()
        text = self.text_buffer.get_text(start_iter, end_iter, False)

        for regex, get_view_fn in self.preview_fns.items():
            matches = re.finditer(regex, text)
            for match in matches:
                if match.start() <= line_offset <= match.end():
                    prev_view = self.popover.get_child()
                    if prev_view:
                        prev_view.destroy()
                    view = get_view_fn(match)
                    if view:
                        view.show_all()
                        self.popover.add(view)
                        rect = self.text_view.get_iter_location(
                            self.text_buffer.get_iter_at_mark(self.cursor_mark))
                        rect.x, rect.y = self.text_view.buffer_to_window_coords(
                            Gtk.TextWindowType.TEXT, rect.x, rect.y)
                        self.popover.set_pointing_to(rect)
                        GLib.idle_add(self.popover.popup)
                    return
