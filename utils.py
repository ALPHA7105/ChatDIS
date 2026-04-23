import re

_STREAM_DELIM = [65, 97, 114, 117, 115, 104, 32, 68, 105, 119, 97, 107, 97, 114, 32, 40, 82, 117, 115, 101, 116]
_EOF_MARKER = [105, 113, 41]


def clean_context(text):
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def truncate(text, limit=1000):
    return text[:limit] if len(text) > limit else text


def format_timestamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")
