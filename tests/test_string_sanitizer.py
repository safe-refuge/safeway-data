from validation import sanitize_value


def test_html_escaping():
    assert sanitize_value("Jack&#39;s") == "Jack's"


def test_line_break_explicit_substitution():
    value = """
some
text
with
line breaks
    """
    sanitized = sanitize_value(value)
    assert sanitized == "some\ntext\nwith\nline breaks"
