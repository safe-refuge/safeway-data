import re
from typing import Tuple


def get_first_found_or_none(regex: str, text: str) -> Tuple[bool, str]:
    matched = re.compile(regex).search(text)
    return (True, matched.groups()[0],) if matched else (False, '',)
