from typing import List, Callable

from requests import Session, Response
from scrapy.http import HtmlResponse

from models.point_of_interest import PointOfInterest


def parse_betamax_response(session: Session, parse_function: Callable, url: str) -> List[PointOfInterest]:
    """
    Loads response for a given URL through Betamax
    and parses it with a given parse function
    """
    scrapy_response = get_betamax_response(session, url)
    results = [
        PointOfInterest(**result) for result in parse_function(scrapy_response)
    ]

    return results


def get_betamax_response(session: Session, url: str) -> HtmlResponse:
    response: Response = session.get(url)
    return HtmlResponse(body=response.content, url=url)


class PhoneNumberExtractorService:
    INTERNAL_NUMBER_LENGTH: int = None
    COUNTRY_CODE: str = None

    def __init__(self, raw_phone: str):
        self.raw_phone = raw_phone

    def _get_digits(self, origin):
        digits = [digit for digit in list(origin) if digit in '0123456789']
        return ''.join(list(digits))

    def _get_phone_numbers(self, origin) -> List[str]:
        return [phone for phone in
                get_phone_numbers(list(origin), self.INTERNAL_NUMBER_LENGTH)
                if phone]

    def get_phone_number_in_e164(self):
        digits = self._get_digits(self.raw_phone)
        phones = self._get_phone_numbers(digits)
        return list(map(lambda phone: f'{self.COUNTRY_CODE} {phone}', phones))


class PolandPhoneNumberExtractorService(PhoneNumberExtractorService):
    INTERNAL_NUMBER_LENGTH = 9
    COUNTRY_CODE = '+48'


def get_phone_numbers(origin: List[str], internal_number_length) -> List[str]:
    _origin = list(origin)
    if len(_origin) < internal_number_length:
        return ['']

    if len(_origin) == internal_number_length:
        return [''.join(origin)]

    if _origin[0] == '0':
        left = _origin[1:1 + internal_number_length]
        right = _origin[1 + internal_number_length:]
    else:
        left = _origin[:internal_number_length]
        right = _origin[internal_number_length:]
    return get_phone_numbers(''.join(left), internal_number_length) + get_phone_numbers(''.join(right),
                                                                                        internal_number_length)
