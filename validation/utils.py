import re
from typing import Tuple


def get_first_match_or_empty(regex: str, text: str) -> str:
    matched = re.compile(regex).search(text)
    return matched.groups()[0] if matched else ''
