#!/usr/bin/python3
#
# Generates color palettes based on the specified background/foreground colors.
#
# Usage: python color_palette_generator.py #fg_hex #bg_hex light|dark
#
# The light variant is based on GitHub's style, while the dark variant is based on pre-existing UberWriter styles.
#
# Accessibility is not accounted for, so make sure to verify contrast: https://webaim.org/resources/contrastchecker/

import operator
import os
import sys


def hex_to_tuple(h):
    return tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


def tuple_to_hex(t):
    (r, g, b) = t
    if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
        return '#%02x%02x%02x (clamped)' % tuple(map(lambda x: max(0, min(x, 255)), t))
    else:
        return '#%02x%02x%02x' % t


def sub_tuples(t1, t2):
    return tuple(map(operator.sub, t1, t2))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {} foreground_color background_color light|dark\n" +
              "Both colors must be in hexadecimal format, eg. #f6f5f4".format(os.path.basename(__file__)))
        exit()

    target_foreground_color = hex_to_tuple(sys.argv[1])
    target_background_color = hex_to_tuple(sys.argv[2])
    dark = sys.argv[3] == "dark"

    gh_text_color =               hex_to_tuple("#dbdbdb" if dark else "#24292e")
    gh_background_color =         hex_to_tuple("#353535" if dark else "#ffffff")
    gh_alt_background_color =     hex_to_tuple("#3a3a3a" if dark else "#f6f8fa")
    gh_link_color =               hex_to_tuple("#a2c7f8" if dark else "#0366d6")
    gh_blockquote_text_color =    hex_to_tuple("#959595" if dark else "#6a737d")
    gh_blockquote_border_color =  hex_to_tuple("#525252" if dark else "#dfe2e5")
    gh_header_border_color =      hex_to_tuple("#474747" if dark else "#eaecef")
    gh_hr_background_color =      hex_to_tuple("#505050" if dark else "#e1e4e8")
    gh_table_tr_border_color =    hex_to_tuple("#696969" if dark else "#c6cbd1")
    gh_table_td_border_color =    hex_to_tuple("#525252" if dark else "#dfe2e5")
    gh_kbd_text_color =           hex_to_tuple("#bbbbbb" if dark else "#444d56")
    gh_kbd_background_color =     hex_to_tuple("#3c3c3c" if dark else "#fafbfc")
    gh_kbd_border_color =         hex_to_tuple("#696969" if dark else "#c6cbd1")
    gh_kbd_shadow_color =         hex_to_tuple("#979797" if dark else "#959da5")

    text_color_diff = sub_tuples(gh_text_color, target_foreground_color)
    background_color_diff = sub_tuples(gh_background_color, target_background_color)

    text_color = tuple_to_hex(target_foreground_color)
    background_color = tuple_to_hex(target_background_color)
    alt_background_color = tuple_to_hex(sub_tuples(gh_alt_background_color, background_color_diff))
    link_color = tuple_to_hex(sub_tuples(gh_link_color, text_color_diff))
    blockquote_text_color = tuple_to_hex(sub_tuples(gh_blockquote_text_color, text_color_diff))
    blockquote_border_color = tuple_to_hex(sub_tuples(gh_blockquote_border_color, background_color_diff))
    header_border_color = tuple_to_hex(sub_tuples(gh_header_border_color, background_color_diff))
    hr_background_color = tuple_to_hex(sub_tuples(gh_hr_background_color, background_color_diff))
    table_tr_border_color = tuple_to_hex(sub_tuples(gh_table_tr_border_color, background_color_diff))
    table_td_border_color = tuple_to_hex(sub_tuples(gh_table_td_border_color, background_color_diff))
    kbd_text_color = tuple_to_hex(sub_tuples(gh_kbd_text_color, text_color_diff))
    kbd_background_color = tuple_to_hex(sub_tuples(gh_kbd_background_color, background_color_diff))
    kbd_border_color = tuple_to_hex(sub_tuples(gh_kbd_border_color, background_color_diff))
    kbd_shadow_color = tuple_to_hex(sub_tuples(gh_kbd_shadow_color, background_color_diff))

    print(("--text-color: {};\n" +
           "--background-color: {};\n" +
           "--alt-background-color: {};\n" +
           "--link-color: {};\n" +
           "--blockquote-text-color: {};\n" +
           "--blockquote-border-color: {};\n" +
           "--header-border-color: {};\n" +
           "--hr-background-color: {};\n" +
           "--table-tr-border-color: {};\n" +
           "--table-td-border-color: {};\n" +
           "--kbd-text-color: {};\n" +
           "--kbd-background-color: {};\n" +
           "--kbd-border-color: {};\n" +
           "--kbd-shadow-color: {};\n").format(
        text_color,
        background_color,
        alt_background_color,
        link_color,
        blockquote_text_color,
        blockquote_border_color,
        header_border_color,
        hr_background_color,
        table_tr_border_color,
        table_td_border_color,
        kbd_text_color,
        kbd_background_color,
        kbd_border_color,
        kbd_shadow_color))
