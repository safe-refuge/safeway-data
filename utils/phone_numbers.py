import re

import phonenumbers
from phonenumbers import NumberParseException


class BasePhoneNumberExtractorService:
    INTERNAL_NUMBER_LENGTH: int = None
    COUNTRY_CODE: str = None

    def __init__(self, raw_phone: str):
        self.raw_phone = raw_phone

    def _get_phone_chars(self, origin):
        digits = [digit for digit in list(origin) if digit in '0123456789 -()\n']
        out = ''.join(list(digits))
        return out.replace('()', '')

    def get_phone_numbers_in_e164(self):
        _phone = self._remove_country_code()
        phone_chars = self._get_phone_chars(_phone)
        phones = get_human_phone_numbers('', phone_chars, self.INTERNAL_NUMBER_LENGTH)
        return list(map(lambda phone: f'{self.COUNTRY_CODE} {phone}', phones))

    def _remove_country_code(self):
        self.raw_phone = self.raw_phone.replace('+ ', '+')
        return self.raw_phone.replace(self.COUNTRY_CODE, '')


class PhoneNumberExtractorService(BasePhoneNumberExtractorService):
    INTERNAL_NUMBER_LENGTH = None

    def get_phone_numbers_in_e164(self):
        phone_numbers = self._split_phone_number()
        parsed_phones = [self._parse_phone(phone) for phone in phone_numbers]
        return [phone for phone in parsed_phones if phone]

    def _split_phone_number(self):
        result = re.findall(r'([+/0-9-– ()]+)', self.raw_phone)
        return [phone.strip() for phone in result if len(phone) >= 2]

    def _parse_phone(self, phone):
        if (not phone) and (not self.COUNTRY_CODE):
            return ''
        cleaned_phone = self._clean_phone(phone)
        country_code_phone = f'+{self.COUNTRY_CODE}{cleaned_phone}' \
            if not self._has_country_code(phone, self.COUNTRY_CODE) else \
            cleaned_phone if cleaned_phone.startswith('+') else f'+{cleaned_phone}'
        try:
            _phone = phonenumbers.parse(country_code_phone, None)
            if phonenumbers.is_possible_number(_phone) and phonenumbers.is_possible_number(_phone):
                return phonenumbers.format_number(_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except NumberParseException:
            pass

    def _clean_phone(self, phone):
        digits_plugs = [char for char in phone if char in '0123456789+-()/: ']
        return ''.join(digits_plugs)

    @classmethod
    def _has_country_code(cls, origin, code):
        started_with_code_number = code.lstrip('+')
        return any([origin.startswith(code), origin.startswith(started_with_code_number)])


class PolandPhoneNumberExtractorService(BasePhoneNumberExtractorService):
    INTERNAL_NUMBER_LENGTH = 9
    COUNTRY_CODE = '+48'


def get_human_phone_numbers(parsed: str, phone: str, internal_number_length: int) -> list[str]:
    _characters = list(phone)

    parsed = parsed.lstrip()

    if len([p for p in clean_leading_chars_phone(parsed) if is_digit(p)]) == internal_number_length:
        return [parsed] + get_human_phone_numbers('', phone, internal_number_length)

    if len(phone) == 0:
        return [parsed] if len(parsed) == internal_number_length else []

    first = _characters[0]
    rest = _characters[1:]

    return get_human_phone_numbers(parsed + first, ''.join(rest), internal_number_length)


def clean_leading_chars_phone(phone):
    phone = phone.lstrip('(')
    phone = phone.lstrip('0')
    return phone


def is_digit(alphabet: str) -> bool:
    return alphabet in '0123456789'
