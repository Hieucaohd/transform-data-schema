from marshmallow import fields, ValidationError, utils
import typing
from .utils import convert_timestamp_to_date_utc
from .auto_replace_validate_error_field import AutoReplaceErrorField
import datetime


__all__ = [
    "NestedValueField",
    "DatetimeFromTimeStamp"
]


class NestedValueField(fields.Field, metaclass=AutoReplaceErrorField):
    """Field that help to get value from nested field when deserializer
    :param nested_key: show where to get value in nested field"""

    def __init__(self, *args, **kwargs):
        if 'data_key' in kwargs and 'nested_key' in kwargs:
            raise Exception('You must define just one of data_key or nested_key.')
        super(NestedValueField, self).__init__(*args, **kwargs)
        self.type_class = kwargs.get('type_class', None)
        self.nested_key = kwargs.get('nested_key', None)


class Str(fields.Str, metaclass=AutoReplaceErrorField):
    pass


class Int(fields.Int, metaclass=AutoReplaceErrorField):
    pass


class Float(fields.Float, metaclass=AutoReplaceErrorField):
    pass


class Date(fields.Date, metaclass=AutoReplaceErrorField):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime.date):
            return value
        else:
            return super(Date, self)._deserialize(value, attr, data, **kwargs)


class DateTime(fields.DateTime, metaclass=AutoReplaceErrorField):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime.datetime):
            return value
        else:
            return super(DateTime, self)._deserialize(value, attr, data, **kwargs)


class Nested(fields.Nested, metaclass=AutoReplaceErrorField):
    pass


class DatetimeFromTimeStamp(fields.Field):
    """Field that deserializer from timestamp like: 1660622040.0 to datetime object"""

    def _deserialize(
            self,
            value: typing.Any,
            attr: str or None,
            data: typing.Mapping[str, typing.Any] or None,
            **kwargs,
    ):
        if value is None:
            return None
        return convert_timestamp_to_date_utc(value)
