from marshmallow import Schema, pre_load
from .custom_fields import NestedValueField
from .utils import get_value_from_field, remove_none_field
import typing


class BaseSchemaTransform(Schema):
    def _get_value_for_nested_value_field(self, data):
        for attr_name, field_obj in self.load_fields.items():
            if isinstance(field_obj, NestedValueField):
                field_name = (
                    field_obj.nested_key if field_obj.nested_key is not None else attr_name
                )
                data[attr_name] = get_value_from_field(data, field_name, None)

    def pre_load_action(self, data, many, **kwargs):
        return data

    @pre_load(pass_many=True)
    def load_nested_field(self, data: dict, many, **kwargs):
        data = self.pre_load_action(data, many, **kwargs)
        data_list = data
        if not many:
            data_list = [data]

        data_list_copy = []
        for data_item in data_list:

            self._get_value_for_nested_value_field(data_item)
            data_item = remove_none_field(data_item)
            data_list_copy.append(data_item)

        if not many:
            return data_list_copy[0]
        return data_list_copy

    def dump(self, obj: typing.Any, *, many: bool | None = None):
        raise Exception('Method not use.')

    def dumps(self, obj: typing.Any, *args, many: bool | None = None, **kwargs):
        raise Exception('Method not use')