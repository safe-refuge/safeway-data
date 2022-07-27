import re

import pycountry
from phonenumbers.phonenumberutil import NumberParseException, country_code_for_region

import phonenumbers

from utils.phone_numbers import PolandPhoneNumberExtractorService


def sanitise_phone(phone: str, country_name: str = None) -> str:
    if not phone:
        return ''
    prefix = None
    if not has_prefix(phone):
        prefix = get_prefix_by_country_name(country_name) if not country_name is None else None
        phone = f'{prefix} {phone}' if (prefix and prefix not in phone) else phone

    if prefix == '+48' or '+48' in phone:
        found = PolandPhoneNumberExtractorService(phone).get_phone_number_in_e164()
        return found[0] if found else ''
    try:
        _phone = phonenumbers.parse(clean_phone(phone), None)
        if phonenumbers.is_possible_number(_phone) and phonenumbers.is_possible_number(_phone):
            return phonenumbers.format_number(_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except NumberParseException:
        pass
    return ''


def clean_phone(phone: str) -> str:
    first_phone = re.split(',|;', phone)[0]
    digits_plugs = [char for char in first_phone if char in '0123456789+-() ']
    return ''.join(digits_plugs).split('  ')[0]


def get_prefix_by_country_name(country_name: str) -> str:
    country = pycountry.countries.get(name=country_name)

    if country:
        country_code = f'+{country_code_for_region(country.alpha_2)}'
        return country_code
    else:
        missing_country_mapping = {'moldova': '+373', 'czech': '+430'}
        for k, v in missing_country_mapping.items():
            if k in country_name.lower():
                return v


def has_prefix(phone: str) -> bool:
    return '+' in phone
