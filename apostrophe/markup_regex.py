import re

ITALIC_ASTERISK = re.compile(
    r"(?<!\\)\*[^\s\*](?P<text>.*?\S?.*?)(?<!\\)\*")
ITALIC_UNDERSCORE = re.compile(
    r"(?<!(\\|\S))_[^\s_](?P<text>.*?\S?.*?)(?<!\\)_")
BOLD = re.compile(
    r"(\*\*|__)[^\s*](?P<text>.*?\S.*?)\1")
BOLD_ITALIC = re.compile(
    r"((\*\*|__)([*_])|([*_])(\*\*|__))[^\s*](?P<text>.*?\S.*?)(?:\5\4|\3\2)")
STRIKETHROUGH = re.compile(
    r"~~(?P<text>.*?\S.*?)~~")
CODE = re.compile(
    r"(?<!`)(?P<ticks>`+)(?!`)(?P<content>.+?)(?<!`)(?P=ticks)(?!`)")
LINK = re.compile(
    r"\[(?P<text>.*?)\]\((?P<url>.+?)(?: \"(?P<title>.+)\")?\)")
LINK_ALT = re.compile(
    r"<(?P<text>(?P<url>[A-Za-z][A-Za-z0-9.+-]{1,31}:[^<>\x00-\x20]*|(?:[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)))>")
IMAGE = re.compile(
    r"!\[(?P<text>.*)\]\((?P<url>.+?)(?: \"(?P<title>.+)\")?\)")
HORIZONTAL_RULE = re.compile(
    r"(?:^|\n{2,})(?P<symbols> {0,3}[*\-_]{3,} *)(?:\n{2,}|$)")
LIST = re.compile(
    r"(?:^|\n)(?P<content>(?P<indent>(?:\t| {4})*)(?P<symbol>(?:[\-*+])) (?:\t| {4})*(?P<text>.+(?:\n+ \2.+)*)?)")
ORDERED_LIST = re.compile(
    r"(?:^|\n)(?P<content>(?P<indent>(?:\t| {4})*)(?P<prefix>(?:(?P<number>\d)|(?:[a-z]))+(?P<delimiter>[.)]))(?:\t| {4}| )(?P<text>.+(?:\n+ {2}\2.+)*)?)")
BLOCK_QUOTE = re.compile(
    r"^ {0,3}(?:> ?)+(?P<text>.+)", re.M)
HEADER = re.compile(
    r"^ {0,3}(?P<level>#{1,6}) (?P<text>[^\n]+)", re.M)
HEADER_UNDER = re.compile(
    r"(?:^\n*|\n\n)(?P<text>[^\s].+)\n {0,3}[=\-]+(?: +?\n|$)")
CODE_BLOCK = re.compile(
    r"^ {0,3}(?P<block>([`~]{3})(?P<text>.+?)(?<! ) {0,3}\2)(?:\s+?$|$)", re.S|re.M)
TABLE = re.compile(
    r"^[\-+]{5,}\n(?P<text>.+?)\n[\-+]{5,}\n", re.S)
MATH = re.compile(
    r"([$]{1,2})(?P<text>[^`\\ ]{1,2}|[^` ].+?[^`\\ ])\1", re.S|re.M)
FOOTNOTE_ID = re.compile(
    r"[^\s]+\[\^(?P<id>(?P<text>[^\s]+))\]")
FOOTNOTE = re.compile(
    r"(?:^\n*|\n\n)\[\^(?P<id>[^\s]+)\]: (?P<text>(?:[^\n]+|\n+(?=(?:\t| {4})))+)(?:\n+|$)", re.M)
