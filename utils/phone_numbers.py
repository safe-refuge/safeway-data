from typing import List


class PhoneNumberExtractorService:
    INTERNAL_NUMBER_LENGTH: int = None
    COUNTRY_CODE: str = None

    def __init__(self, raw_phone: str):
        self.raw_phone = raw_phone

    def _get_digits(self, origin):
        digits = [digit for digit in list(origin) if digit in '0123456789']
        return ''.join(list(digits))

    def get_phone_number_in_e164(self):
        digits = self._get_digits(self.raw_phone)
        phones = get_phone_numbers(digits, self.INTERNAL_NUMBER_LENGTH)
        return list(map(lambda phone: f'{self.COUNTRY_CODE} {phone}', phones))


class PolandPhoneNumberExtractorService(PhoneNumberExtractorService):
    INTERNAL_NUMBER_LENGTH = 9
    COUNTRY_CODE = '+48'


def get_phone_numbers(origin: str, internal_number_length) -> List[str]:
    _origin = list(origin)
    if len(_origin) < internal_number_length:
        return []

    if len(_origin) == internal_number_length:
        return [''.join(origin)]

    if _origin[0] == '0':
        left = _origin[1:1 + internal_number_length]
        right = _origin[1 + internal_number_length:]
    else:
        left = _origin[:internal_number_length]
        right = _origin[internal_number_length:]
    return get_phone_numbers(''.join(left), internal_number_length) + \
           get_phone_numbers(''.join(right), internal_number_length)
