import copy

from marshmallow import Schema, pre_load, ValidationError
from .transform_fields import NestedValueField
from .utils import get_value_from_field, NotFoundValue
import typing


class ActionWhenValidateErrorField:
    REMOVE_FIELD = 'REMOVE_FIELD'


class BaseSchemaTransform(Schema):
    def __init__(
            self,
            *args,
            action_when_validate_error: ActionWhenValidateErrorField or None = None,
            **kwargs
    ):
        super(BaseSchemaTransform, self).__init__(*args, **kwargs)
        self.action_when_validate_error_field = action_when_validate_error

    def _get_value_for_nested_value_field(self, data):
        for attr_name, field_obj in self.load_fields.items():
            if isinstance(field_obj, NestedValueField):
                field_name = (
                    field_obj.nested_key if field_obj.nested_key is not None else attr_name
                )
                try:
                    data[attr_name] = get_value_from_field(data, field_name)
                except NotFoundValue as e:
                    pass

    def _return_type_class_for_nested_value_field(self):
        load_fields_copy = copy.deepcopy(self.load_fields)
        for attr_name, field_obj in self.load_fields.items():
            if isinstance(field_obj, NestedValueField) and field_obj.type_class is not None:
                attrs_of_field_obj = copy.deepcopy(field_obj.__dict__)
                load_fields_copy[attr_name] = field_obj.type_class(**attrs_of_field_obj)
        self.load_fields = load_fields_copy

    def pre_load_action(self, data, many, **kwargs):
        return data

    @pre_load(pass_many=True)
    def _pre_load_action(self, data: dict, many, **kwargs):
        data = self.pre_load_action(data, many, **kwargs)
        data_list = data
        if not many:
            data_list = [data]

        data_list_copy = []
        for i in range(0, len(data_list)):
            data_item = data_list[i]
            self._get_value_for_nested_value_field(data_item)
            data_list_copy.append(data_item)
        self._return_type_class_for_nested_value_field()

        if not many:
            return data_list_copy[0]
        return data_list_copy

    def remove_fields_error(self, data, fields_error):
        for field in fields_error:
            del data[field]

    def load(
        self,
        data: (
            typing.Mapping[str, typing.Any]
            or typing.Iterable[typing.Mapping[str, typing.Any]]
        ),
        *,
        many: bool or None = None,
        partial: bool or None = None,
        unknown: str or None = None,
    ):
        try:
            return super().load(data, many=many, partial=partial, unknown=unknown)
        except ValidationError as e:
            error_messages: typing.Mapping[int, dict] | typing.Mapping[str, list] = e.messages
            data_list = data

            if not many:
                error_messages = {0: error_messages}
                data_list = [data]

            if self.action_when_validate_error_field is not None:
                if self.action_when_validate_error_field == ActionWhenValidateErrorField.REMOVE_FIELD:
                    for index, fields_error in error_messages.items():
                        self.remove_fields_error(data_list[index], list(fields_error.keys()))
                    return super().load(data, many=many, partial=partial, unknown=unknown)
            raise e

    @classmethod
    def transform(
        cls,
        data: (
            typing.Mapping[str, typing.Any]
            or typing.Iterable[typing.Mapping[str, typing.Any]]
        ),
        *,
        many: bool or None = False,
        partial: bool or None = False,
        unknown: str or None = None,
        action_when_validate_error: ActionWhenValidateErrorField or None = None
    ):
        data_copy = copy.deepcopy(data)
        instance = cls(many=many, partial=partial, unknown=unknown, action_when_validate_error=action_when_validate_error)
        return instance.load(data_copy, many=many, partial=partial, unknown=unknown)

    @classmethod
    def get_require_fields(cls):
        self = cls()
        require_fields = {}
        for attr_name, field_obj in self.load_fields.items():
            if field_obj.required:
                require_fields[attr_name] = field_obj
        return require_fields

    def dump(self, obj: typing.Any, *, many: bool or None = None):
        raise Exception('Method not use.')

    def dumps(self, obj: typing.Any, *args, many: bool or None = None, **kwargs):
        raise Exception('Method not use')
