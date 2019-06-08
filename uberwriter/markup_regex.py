import re

ITALIC = re.compile(
    r"(\*|_)(?P<text>.+?)\1")
BOLD = re.compile(
    r"(\*\*|__)(?P<text>.+?)\1")
BOLD_ITALIC = re.compile(
    r"(\*\*\*|___)(?P<text>.+?)\1")
STRIKETHROUGH = re.compile(
    r"~~(?P<text>.+?)~~")
LINK = re.compile(
    r"\[(?P<text>.*)\]\((?P<url>.+?)(?: \"(?P<title>.+)\")?\)")
IMAGE = re.compile(
    r"!\[(?P<text>.*)\]\((?P<url>.+?)(?: \"(?P<title>.+)\")?\)")
HORIZONTAL_RULE = re.compile(
    r"(?:^\n*|\n\n)(?P<symbols> {0,3}[*\-_]{3,} *)(?:\n+|$)")
LIST = re.compile(
    r"(?:^\n*|\n\n)(?P<indent>(?:\t| {4})*)[\-*+]( +)(?P<text>.+(?:\n+ \2.+)*)")
ORDERED_LIST = re.compile(
    r"(?:^\n*|\n\n)(?P<indent>(?:\t| {4})*)(?P<prefix>(?:\d|[a-z])+[.)]) (?P<text>.+(?:\n+ {2}\2.+)*)")
BLOCK_QUOTE = re.compile(
    r"^ {0,3}(?:> ?)+(?P<text>.+)", re.M)
HEADER = re.compile(
    r"^ {0,3}(?P<level>#{1,6}) (?P<text>[^\n]+)", re.M)
HEADER_UNDER = re.compile(
    r"(?:^\n*|\n\n)(?P<text>[^\s].+)\n {0,3}[=\-]+(?:\s+?\n|$)")
CODE_BLOCK = re.compile(
    r"(?:^|\n) {0,3}(?P<block>([`~]{3})(?P<text>.+?) {0,3}\2)(?:\s+?\n|$)", re.S)
TABLE = re.compile(
    r"^[\-+]{5,}\n(?P<text>.+?)\n[\-+]{5,}\n", re.S)
MATH = re.compile(
    r"([$]{1,2})[^` ](?P<text>.+?)[^`\\ ]\1")
FOOTNOTE_ID = re.compile(
    r"[^\s]+\[\^(?P<id>(?P<text>[^\s]+))\]")
FOOTNOTE = re.compile(
    r"(?:^\n*|\n\n)\[\^(?P<id>[^\s]+)\]: (?P<text>(?:[^\n]+|\n+(?=(?:\t| {4})))+)(?:\n+|$)", re.M)
