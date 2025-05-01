import re
from type import LineType, InlineTextType

LINE_REGEX_PATTERNS = {
    LineType.HEADING: re.compile(r"^(#{1,6})\s+(.+)$"),
    LineType.QUOTE: re.compile(r"^>\s*(.*)$"),
    LineType.CODE_START: re.compile(r"^```(\w*)$"),
    LineType.CODE_END: re.compile(r"^```$"),
    LineType.UNORDERED_LIST_ITEM: re.compile(r"^(\s*)[-*+]\s+(.+)$"),
    LineType.ORDERED_LIST_ITEM: re.compile(r"^(\s*)\d+\.\s+(.+)$"),
    LineType.HORIZONTAL_RULE: re.compile(r"^([\*\-_])\1{2,}$"),
}
INLINE_REGEX_PATTERNS = {
    InlineTextType.LINK: re.compile(r"\[([^\]]+)\]\(([^)]+)\)"),
    InlineTextType.IMAGE: re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"),
    InlineTextType.BOLD: re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__"),
    InlineTextType.ITALIC: re.compile(r"\*([^*]+)\*|_([^_]+)_"),
    InlineTextType.INLINE_CODE: re.compile(r"`([^`]+)`"),
}
