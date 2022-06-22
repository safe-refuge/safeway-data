from validation.utils import get_first_match_or_empty

URL_REGEX = r'([(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))'
MARKDOWN_URL_REGEX = r'\[.*\]\((.*)\)'
HTTP_URL_REGEX = r'(http.*)$'

DEFAULT_URL_SCHEMES = ['https', 'http']
DEFAULT_URL_PROTOCOLS = 'https://'
ABNORMAL_HOST_PARTS_NUMBER = 2
HOST_SPLIT_DOT_CHAR = '.'
WWW_HOST_CHARS = 'www'
EMAIL_CHAR = '@'


def sanitise_url(url: str) -> str:
    if len(url.split(HOST_SPLIT_DOT_CHAR)) <= ABNORMAL_HOST_PARTS_NUMBER and url.startswith(WWW_HOST_CHARS) \
            or EMAIL_CHAR in url:
        return ''

    url_in_markdown = get_first_match_or_empty(MARKDOWN_URL_REGEX, url)
    url = url_in_markdown if url_in_markdown else url

    _url = get_first_match_or_empty(URL_REGEX, url)
    if _url:
        if all([scheme not in _url for scheme in DEFAULT_URL_SCHEMES]):
            url = DEFAULT_URL_PROTOCOLS + _url

        url_in_text = get_first_match_or_empty(HTTP_URL_REGEX, _url)
        url = url_in_text if url_in_text else url

    return url


