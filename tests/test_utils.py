import pytest

from utils.phone_numbers import PolandPhoneNumberExtractorService, get_phone_numbers, PhoneNumberExtractorService


class TestPhoneNumberExtractorService:

    @pytest.mark.parametrize('origin, expected', [
        ('24 356 22 02  024 356 29 09', ['+48 243562202', '+48 243562909']),
        ('468302636\n468302648\n46 830', ['+48 468302636', '+48 468302648']),
        ('29 752-25-14   118', ['+48 297522514']),
        ('14 6761067       146761140', ['+48 146761067', '+48 146761140']),
        ('17 7445715 7445717 7445756', ['+48 177445715', '+48 744571774']),
        ('(15) 8643058, (15) 8665099', ['+48 158643058', '+48 158665099']),
        ('25 781 60 74, 25 787 73 50', ['+48 257816074', '+48 257877350']),
        ('22 510 98 03-19 foo', ['+48 225109803']),
        ('22 510 98 03-19 bar', ['+48 225109803']),
        ('542851327', ['+48 542851327']),
        ('(+48)792 568 561, (+48)22 621 51 65', ['+48 792568561', '+48 226215165']),
        ('224813418', ['+48 224813418']),
        ('735174517, 735755200, 731512726', ['+48 735174517', '+48 735755200', '+48 731512726'])
    ])
    def test_get_phone_numbers_in_e164_with_fixed_internal_number_length(self, origin, expected):
        service = PolandPhoneNumberExtractorService(origin)
        assert service.get_phone_numbers_in_e164() == expected

    @pytest.mark.parametrize('origin, expected', [
        ('24 356 22 02  024 356 29 09', '2435622020243562909'),
        ('468302636\n468302648\n46 830', '46830263646830264846830')
    ])
    def test_get_digits(self, origin, expected):
        service = PolandPhoneNumberExtractorService(origin)
        assert service._get_digits(origin) == expected

    @pytest.mark.parametrize('origin, expected', [
        ('243562202', ['243562202']),
        ('243562202243562909', ['243562202', '243562909']),
        ('46830263646830264846830', ['468302636', '468302648']),
        ('0243562202', ['243562202']),
        ('2435622020243562909', ['243562202', '243562909']),
        ('17744571574457177445756', ['177445715', '744571774'])
    ])
    def test_extract_phone_numbers(self, origin, expected):
        assert get_phone_numbers(origin, 9) == expected

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
