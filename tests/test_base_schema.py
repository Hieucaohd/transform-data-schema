from src.transform_data.base_schema import BaseSchemaTransform
from src.transform_data.custom_fields import NestedValueField
from marshmallow import fields, EXCLUDE


class DogSchema(BaseSchemaTransform):
    class Meta:
        unknown = EXCLUDE

    NAME = fields.Str(data_key='name')
    ACTION_RUN = NestedValueField(nested_key='action.run')
    ACTION_SOUND = NestedValueField(nested_key='action.sound.normal')
    ACTION_SOUND_WHEN_HUNGRY = NestedValueField(nested_key='action.sound.hungry')


class TestBaseSchemaTransform:
    def test_result_of_load(self):
        dog_schema = DogSchema()
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
        result = dog_schema.load(dog_raw_data)
        assert result == {
            'NAME': 'Husky',
            'ACTION_RUN': 'very fast',
            'ACTION_SOUND': 'go go',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya'
        }

    def test_result_of_load_1(self):
        dog_schema = DogSchema()
        dog_raw_data = {
            'name': None,
            'action': {
                'run': 'very fast',
                'sound': None
            }
        }
        result = dog_schema.load(dog_raw_data)
        assert result == {
            'ACTION_RUN': 'very fast',
        }

    def test_result_of_load_list(self):
        dog_schema = DogSchema()
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
        result_list = dog_schema.load(dog_raw_data_list, many=True)
        assert result_list == [
            {
                'ACTION_RUN': 'very fast',
            },
            {
                'NAME': 'Husky',
                'ACTION_RUN': 'very fast',
            }
        ]
