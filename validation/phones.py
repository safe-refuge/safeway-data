from phonenumbers.phonenumberutil import NumberParseException

import phonenumbers


def sanitise_phone(phone: str) -> str:
    try:
        _phone = phonenumbers.parse(phone, None)
        if phonenumbers.is_possible_number(_phone) and phonenumbers.is_possible_number(_phone):
            return phonenumbers.format_number(_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except NumberParseException:
        pass
    return f'Error: {phone}'  # TODO: return ''

