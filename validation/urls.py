from validation.utils import get_first_found_or_none

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

    markdown_url, url_in_markdown = get_first_found_or_none(MARKDOWN_URL_REGEX, url)
    url = url_in_markdown if markdown_url else url

    valid_url, _url = get_first_found_or_none(URL_REGEX, url)
    if valid_url:
        if all([scheme not in _url for scheme in DEFAULT_URL_SCHEMES]):
            url = DEFAULT_URL_PROTOCOLS + _url

        not_start_with_http, url_in_text = get_first_found_or_none(HTTP_URL_REGEX, _url)
        url = url_in_text if not_start_with_http else url

    return url


