import pytest

from tests.utils import PolandPhoneNumberExtractorService, get_phone_numbers


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
        ('542851327', ['+48 542851327'])
    ])
    def test_get_phone_numbers_in_e164(self, origin, expected):
        service = PolandPhoneNumberExtractorService(origin)
        assert service.get_phone_number_in_e164() == expected

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
        ('46830263646830264846830', ['468302636', '468302648', '']),
        ('0243562202', ['243562202', '']),
        ('2435622020243562909', ['243562202', '243562909', '']),
        ('17744571574457177445756', ['177445715', '744571774', ''])
    ])
    def test_extract_phone_numbers(self, origin, expected):
        assert get_phone_numbers(origin, 9) == expected

# TODO: edge case
# ('17 7445715 7445717 7445756', '17 7445715 17 7445717 17 7445756'),
