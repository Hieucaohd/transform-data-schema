import typing
from marshmallow import ValidationError


def super_call(supers):
    if len(supers) >= 1:
        return supers[0]
    else:
        return object


def add_hook_into_init(cls, supers):
    original_init = cls.__init__

    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.value_when_validate_error_hook = {
            'set': False
        }
        if 'value_when_validate_error' in kwargs:
            self.value_when_validate_error_hook = {
                'set': True,
                'value': kwargs.get('value_when_validate_error')
            }
    cls.__init__ = __init__


def add_hook_into_deserialize(cls, supers):
    def deserialize(
        self,
        value: typing.Any,
        attr: str or None = None,
        data: typing.Mapping[str, typing.Any] or None = None,
        **kwargs,
    ):
        try:
            deserialized_value = super_call(supers).deserialize(self, value, attr, data, **kwargs)
            return deserialized_value
        except ValidationError as e:
            if self.value_when_validate_error_hook['set']:
                return self.value_when_validate_error_hook['value']
            else:
                raise e
    cls.deserialize = deserialize


class AutoReplaceErrorField(type):
    def __init__(cls, class_name, supers, classdict):
        add_hook_into_init(cls, supers)
        add_hook_into_deserialize(cls, supers)
