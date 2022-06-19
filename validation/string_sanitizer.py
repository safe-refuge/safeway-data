import html


def sanitize_value(value: str) -> str:
    return html.unescape(value)
