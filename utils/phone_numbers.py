import re
from typing import List

import phonenumbers
from phonenumbers import NumberParseException


class BasePhoneNumberExtractorService:
    INTERNAL_NUMBER_LENGTH: int = None
    COUNTRY_CODE: str = None

    def __init__(self, raw_phone: str):
        self.raw_phone = raw_phone

    def _get_digits(self, origin):
        digits = [digit for digit in list(origin) if digit in '0123456789']
        return ''.join(list(digits))

    def get_phone_numbers_in_e164(self):
        _phone = self._remove_country_code()
        digits = self._get_digits(_phone)
        phones = get_phone_numbers(digits, self.INTERNAL_NUMBER_LENGTH)
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
            if self.COUNTRY_CODE not in cleaned_phone else cleaned_phone
        try:
            _phone = phonenumbers.parse(country_code_phone, None)
            if phonenumbers.is_possible_number(_phone) and phonenumbers.is_possible_number(_phone):
                return phonenumbers.format_number(_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except NumberParseException:
            pass

    def _clean_phone(self, phone):
        digits_plugs = [char for char in phone if char in '0123456789+-()/: ']
        return ''.join(digits_plugs)


class PolandPhoneNumberExtractorService(BasePhoneNumberExtractorService):
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
