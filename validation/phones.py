import re

import pycountry
from phonenumbers.phonenumberutil import country_code_for_region

from utils.phone_numbers import PolandPhoneNumberExtractorService, PhoneNumberExtractorService


def sanitise_phone(phone: str, country_name: str = None) -> str:
    if (not phone) and (not country_name):
        return ''

    country_code = get_country_code(phone)
    if country_code is None:
        country_code = get_country_code_by_name(country_name) if country_name is not None else None
    if country_code is None:
        return ''

    fixed_length_internal_phone_mapping = {'+48': PolandPhoneNumberExtractorService}
    class_ = fixed_length_internal_phone_mapping.get(
        country_code,
        get_phone_number_extractor_service_class_with_country_code(country_code))

    found = class_(phone).get_phone_numbers_in_e164()
    return found[0] if found else ''


def get_country_code_by_name(country_name: str) -> str:
    country = pycountry.countries.get(name=country_name)

    if country:
        country_code = f'+{country_code_for_region(country.alpha_2)}'
        return country_code
    else:
        missing_country_mapping = {'moldova': '+373', 'czech': '+430'}
        for k, v in missing_country_mapping.items():
            if k in country_name.lower():
                return v


def get_country_code(phone: str) -> str:
    result = re.findall(r'(\+[\d]+)', phone)
    return result[0].strip() if result else None


def get_phone_number_extractor_service_class_with_country_code(country_code: str) -> [PhoneNumberExtractorService]:
    class NormalPhoneNumberExtractorService(PhoneNumberExtractorService):
        COUNTRY_CODE = country_code

    return NormalPhoneNumberExtractorService
