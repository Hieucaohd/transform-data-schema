from src.transform_data_schema.base_schema import BaseSchemaTransform
from src.transform_data_schema.custom_fields import NestedValueField
from marshmallow import fields, EXCLUDE, ValidationError
import pytest


class DogSchema(BaseSchemaTransform):
    class Meta:
        unknown = EXCLUDE

    NAME = fields.Str(data_key='name')
    ACTION_RUN = NestedValueField(nested_key='action.run', type_class=fields.Str)
    ACTION_SOUND_WHEN_NORMAL = NestedValueField(nested_key='action.sound.normal', type_class=fields.Str)
    ACTION_SOUND_WHEN_HUNGRY = NestedValueField(nested_key='action.sound.hungry', type_class=fields.Str)


class DogSchemaRequire(BaseSchemaTransform):
    class Meta:
        unknown = EXCLUDE

    NAME = fields.Str(data_key='name', required=True)
    ACTION_RUN = NestedValueField(
        nested_key='action.run',
        type_class=fields.Str,
        required=True
    )
    ACTION_SOUND_WHEN_NORMAL = NestedValueField(
        nested_key='action.sound.normal',
        type_class=fields.Str,
        required=True
    )
    ACTION_SOUND_WHEN_HUNGRY = NestedValueField(
        nested_key='action.sound.hungry',
        type_class=fields.Str
    )


class TestBaseSchemaTransform:
    def test_result_of_load(self):
        dog_raw_data = {
            'name': 'Husky',
            'action': {
                'run': 'very fast',
                'sound': {
                    'normal': 'go go',
                    'hungry': 'ya ya'
                }
            }
        }
        result = DogSchema.transform(dog_raw_data)
        assert result == {
            'NAME': 'Husky',
            'ACTION_RUN': 'very fast',
            'ACTION_SOUND_WHEN_NORMAL': 'go go',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya'
        }

    def test_result_of_load_1(self):
        dog_raw_data = {
            'name': None,
            'action': {
                'run': 'very fast',
                'sound': None
            }
        }
        result = DogSchema.transform(dog_raw_data)
        assert result == {
            'ACTION_RUN': 'very fast',
        }

    def test_result_of_load_list(self):
        dog_raw_data_list = [
            {
                'name': None,
                'action': {
                    'run': 'very fast',
                    'sound': None
                }
            },
            {
                'name': 'Husky',
                'action': {
                    'run': 'very fast',
                    'sound': None
                }
            }
        ]
        result_list = DogSchema.transform(dog_raw_data_list, many=True)
        assert result_list == [
            {
                'ACTION_RUN': 'very fast',
            },
            {
                'NAME': 'Husky',
                'ACTION_RUN': 'very fast',
            }
        ]

    def test_require_field(self):
        dog_raw_data = {
            'name': 'Husky',
            'action': {
                'run': 'very fast',
                'sound': {
                    'hungry': 'ya ya'
                }
            }
        }
        with pytest.raises(ValidationError):
            DogSchemaRequire.transform(dog_raw_data)

    def test_require_list_field(self):
        dog_raw_data_list = [
            {
                'name': 'Husky',
                'action': {
                    'run': 'very fast',
                    'sound': {
                        'normal': 'go go',
                        'hungry': 'ya ya'
                    }
                }
            },
            {
                'name': 'Husky',
                'action': {
                    'sound': {
                        'normal': 'go go',
                        'hungry': 'ya ya'
                    }
                }
            },
        ]

        with pytest.raises(ValidationError):
            DogSchemaRequire.transform(dog_raw_data_list, many=True)


