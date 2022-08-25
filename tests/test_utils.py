from src.transform_data_schema.utils import (
    get_value_from_field,
    remove_none_field,
    convert_timestamp_to_date_utc,
    merge_none_field_map_into_data_without_none_field,
    NotFoundValue,
)
import datetime
import pytest


class TestGetValueFromFieldFunc:
    def test_dict_value(self):
        assert get_value_from_field(
            {
                'a': {
                    'b': {
                        'c': 1
                    }
                }
            },
            'a.b'
        ) == {
            'c': 1
        }

    def test_int_value(self):
        assert get_value_from_field({'a': {'b': 1}}, 'a.b') == 1

    def test_list_value(self):
        assert get_value_from_field({'a': {'b': [1, 1, 1]}}, 'a.b') == [1, 1, 1]

    def test_empty_string_value(self):
        assert get_value_from_field({'a': {'b': ''}}, 'a.b') == ''

    def test_none_value(self):
        assert get_value_from_field({'a': {'b': None}}, 'a.b') is None

    def test_raise_exception_when_not_found_value(self):
        with pytest.raises(NotFoundValue):
            get_value_from_field(
                {
                    'a': {
                        'b': {
                            'c': None
                        }
                    }
                },
                'a.b.k'
            )

    def test_raise_exception_when_data_is_not_dict(self):
        with pytest.raises(NotFoundValue):
            get_value_from_field(
                {
                    'a': [1, 2, 3]
                },
                'a.c'
            )

    def test_default_value(self):
        assert get_value_from_field(
            {
                'a': {
                    'b': {}
                }
            },
            'a.b.c',
            None
        ) == None


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

        data_without_none_field_expect = {
            'a': {
                'b': 1
            },
            't': {}
        }

        none_field_map_expect = {
            'a': {
                'c': None
            },
            'k': None,
            't': {
                'e': None
            }
        }

        data_without_none_field, none_field_map = remove_none_field(data_input)
        assert data_without_none_field == data_without_none_field_expect
        assert none_field_map == none_field_map_expect

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

        data_without_none_field_expect = {
            'a': {
                'b': 1
            },
            't': {}
        }

        none_field_map_expect = {
            'e': None,
            'a': {
                'c': None
            },
            'k': None,
            't': {
                'e': None
            }
        }
        data_without_none_field, none_field_map = remove_none_field(data_input)
        assert data_without_none_field == data_without_none_field_expect
        assert none_field_map == none_field_map_expect

    def test_dict_3(self):
        data_input = {
            'a': {
                'b': 1,
                'c': None
            },
            't': {
                "e": 1,
                'f': 1,
                "h": {}
            }
        }

        data_without_none_field_expect = {
            'a': {
                'b': 1
            },
            't': {
                'e': 1,
                'f': 1,
                'h': {}
            }
        }

        none_field_map_expect = {
            'a': {
                'c': None
            }
        }
        data_without_none_field, none_field_map = remove_none_field(data_input)
        assert data_without_none_field == data_without_none_field_expect
        assert none_field_map == none_field_map_expect

    def test_dict_4(self):
        data_input = {
            'a': {
                'b': 1,
            },
            't': {
                "e": 1,
                'f': 1,
                "h": {}
            }
        }

        data_without_none_field_expect = {
            'a': {
                'b': 1
            },
            't': {
                'e': 1,
                'f': 1,
                'h': {}
            }
        }

        none_field_map_expect = {}
        data_without_none_field, none_field_map = remove_none_field(data_input)
        assert data_without_none_field == data_without_none_field_expect
        assert none_field_map == none_field_map_expect

    def test_dict_5(self):
        data_input = {
            'a': {
                'b': None,
            },
            't': {
                "e": None,
                'f': None,
                "h": None
            },
            'k': None
        }

        data_without_none_field_expect = {
            'a': {},
            't': {}
        }

        none_field_map_expect = {
            'a': {
                'b': None,
            },
            't': {
                "e": None,
                'f': None,
                "h": None
            },
            'k': None
        }
        data_without_none_field, none_field_map = remove_none_field(data_input)
        assert data_without_none_field == data_without_none_field_expect
        assert none_field_map == none_field_map_expect


class TestMergeDataWithoutNoneFieldAndNoneFieldMap:
    def test_merge_data_without_none_field_and_none_field_map(self):
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

        data_without_none_field_expect = {
            'a': {
                'b': 1
            },
            't': {}
        }

        none_field_map_expect = {
            'e': None,
            'a': {
                'c': None
            },
            'k': None,
            't': {
                'e': None
            }
        }
        data_without_none_field, none_field_map = remove_none_field(data_input)
        assert data_without_none_field == data_without_none_field_expect
        assert none_field_map == none_field_map_expect

        none_field_merge_into_data_without_none_field_expect = {
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

        merge_none_field_map_into_data_without_none_field(none_field_map, data_without_none_field)
        assert data_without_none_field == none_field_merge_into_data_without_none_field_expect


class TestConvertTimeStampToDateUtcFunc:
    def test_convert(self):
        assert convert_timestamp_to_date_utc(1660622040.0) \
               == datetime.datetime(2022, 8, 16, 3, 54, tzinfo=datetime.timezone.utc)
