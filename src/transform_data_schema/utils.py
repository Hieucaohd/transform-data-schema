import copy
import datetime


def convert_timestamp_to_date_utc(timestamp):
    try:
        if timestamp is not None:
            return datetime.datetime.utcfromtimestamp(timestamp).replace(
                tzinfo=datetime.timezone.utc
            )
        else:
            return None
    except Exception as e:
        return None


class NoValue:
    pass


class NotFoundValue(Exception):
    pass


class DataIsNotDict(Exception):
    pass


def is_atom_value(value):
    return value is None or value == {} or not isinstance(value, dict)


def get_value_from_field(data: dict, from_field: str, default_value=NoValue()):
    data_copy = copy.deepcopy(data)
    field_road = from_field.split('.')

    value = NoValue()
    for field in field_road:
        try:
            value = data_copy[field]
        except Exception:
            if not isinstance(default_value, NoValue):
                value = default_value
                break
            raise NotFoundValue('Not found value')

        data_copy = value

    if isinstance(value, NoValue):
        raise NotFoundValue('Not found value')
    return value


def remove_none_field(data) -> (dict, dict):
    data_copy = copy.deepcopy(data)
    none_field_map = copy.deepcopy(data)

    def recurse_dict(data_in, data_copy_in, none_field_map_in, none_field_map_in_before=None, key_before=None):
        for key, value in data_in.items():
            if value is None:
                del data_copy_in[key]
            elif (value is not None and not isinstance(value, dict)) or value == {}:
                del none_field_map_in[key]
            elif isinstance(value, dict):
                recurse_dict(value, data_copy_in[key], none_field_map_in[key], none_field_map_in, key)

        if none_field_map_in == {} and none_field_map_in_before is not None:
            del none_field_map_in_before[key_before]

    recurse_dict(data, data_copy, none_field_map)
    return data_copy, none_field_map


def merge_none_field_map_into_data_without_none_field(none_field_map: dict, data_without_none_field: dict):
    for key, value in none_field_map.items():
        if not isinstance(value, dict) and value is None:
            data_without_none_field[key] = value
        elif isinstance(value, dict):
            merge_none_field_map_into_data_without_none_field(value, data_without_none_field[key])
