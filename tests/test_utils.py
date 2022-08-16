from src.transform_data.utils import get_value_from_field, remove_none_field, convert_timestamp_to_date_utc
import datetime


class TestGetValueFromFieldFunc:
    def test_dict(self):
        assert get_value_from_field({'a': {'b': 1}}, 'a.b') == 1

    def test_none(self):
        assert get_value_from_field({'a': {'b': 1}}, 'a.c') is None


class TestRemoveNoneFieldFunc:
    def test_dict_1(self):
        data_input = {
            'a': {
                'b': 1,
                'c': None
            },
            'k': None,
            't': {
                'e': None
            }
        }

        data_expect = {
            'a': {
                'b': 1
            },
            't': {}
        }
        assert remove_none_field(data_input) == data_expect

    def test_dict_2(self):
        data_input = {
            'e': None,
            'a': {
                'b': 1,
                'c': None
            },
            'k': None,
            't': {
                'e': None
            }
        }

        data_expect = {
            'a': {
                'b': 1
            },
            't': {}
        }
        assert remove_none_field(data_input) == data_expect


class TestConvertTimeStampToDateUtcFunc:
    def test_convert(self):
        assert convert_timestamp_to_date_utc(1660622040.0) \
               == datetime.datetime(2022, 8, 16, 3, 54, tzinfo=datetime.timezone.utc)
