import pytest

from utils.phone_numbers import PolandPhoneNumberExtractorService, PhoneNumberExtractorService, \
    get_human_phone_numbers


class TestPhoneNumberExtractorService:

    @pytest.mark.parametrize('origin, expected', [
        ('24 356 22 02  024 356 29 09', ['+48 24 356 22 02', '+48 024 356 29 09']),
        ('468302636\n468302648\n46 830', ['+48 468302636', '+48 468302648']),
        ('29 752-25-14   118', ['+48 29 752-25-14']),
        ('14 6761067       146761140', ['+48 14 6761067', '+48 146761140']),
        ('17 7445715 7445717 7445756', ['+48 17 7445715', '+48 7445717 74']),
        ('(15) 8643058, (15) 8665099', ['+48 (15) 8643058', '+48 (15) 8665099']),
        ('25 781 60 74, 25 787 73 50', ['+48 25 781 60 74', '+48 25 787 73 50']),
        ('22 510 98 03-19 foo', ['+48 22 510 98 03']),
        ('22 510 98 03-19 bar', ['+48 22 510 98 03']),
        ('542851327', ['+48 542851327']),
        ('(+48)792 568 561, (+48)22 621 51 65', ['+48 792 568 561', '+48 22 621 51 65']),
        ('224813418', ['+48 224813418']),
        ('735174517, 735755200, 731512726', ['+48 735174517', '+48 735755200', '+48 731512726'])
    ])
    def test_get_phone_numbers_in_e164_with_fixed_internal_number_length(self, origin, expected):
        service = PolandPhoneNumberExtractorService(origin)
        assert service.get_phone_numbers_in_e164() == expected

    @pytest.mark.parametrize('origin, expected', [
        ('24 356 22 02  024 356 29 09', '24 356 22 02  024 356 29 09'),
        ('()792 568 561', '792 568 561'),
        ('468302636\n468302648\n46 830', '468302636\n468302648\n46 830')
    ])
    def test_get_phone_chars(self, origin, expected):
        service = PolandPhoneNumberExtractorService(origin)
        assert service._get_phone_chars(origin) == expected

    @pytest.mark.parametrize('origin, expected', [
        ('24 356 22 02', ['24 356 22 02']),
        ('24 356 22 02  24 356 29 09', ['24 356 22 02', '24 356 29 09']),
        ('468302636\n468302648\n46 830', ['468302636', '468302648']),
        ('0243562202', ['0243562202']),
        ('24 356 22 02 024 356 29 09', ['24 356 22 02', '024 356 29 09']),
        ('17 7445715 7445717 7445756', ['17 7445715', '7445717 74']),
        ('(0 44) 616 11 60', ['(0 44) 616 11 60'])
    ])
    def test_extract_human_phone_numbers(self, origin, expected):
        assert get_human_phone_numbers('', origin, 9) == expected

    @pytest.mark.parametrize('origin, country_code, expected', [
        ('0230 - 564462; 0230 – 564463; Fax: 0230 - 564464', '+40',
         ['+40 230 564 462', '+40 230 564 463', '+40 230 564 464']),
        ('Tel.: +40 261 80 77 57, +40 261 80 77 77 interior 20695, 20696, 20697 ', '+40',
         ['+40 261 807 757', '+40 261 807 777']),
        ('', '+48', []),
        ('224813418', '+43', ['+43 2248 13418']),
        ('+43 05/17 76 380 (the hotline is available Monday-Friday from 9:00-16:00 and is in German or English)',
         '+43',
         ['+43 517 76380', '+43 0016'])
    ])
    def test_get_phone_numbers_in_e164(self, origin, country_code, expected):
        class dynamicPhoneNumberExtractor(PhoneNumberExtractorService):
            COUNTRY_CODE = country_code

        service = dynamicPhoneNumberExtractor(origin)
        assert service.get_phone_numbers_in_e164() == expected

    @pytest.mark.parametrize('origin, code, expected', [
        ('+373 786 05 080', '+373', True),
        ('373 786 05 080', '+373', True)
    ])
    def test_has_country_code(self, origin, code, expected):
        real = PhoneNumberExtractorService._has_country_code(origin, code)
        assert real == expected
