from src.transform_data_schema import BaseSchemaTransform, transform_fields, fields, EXCLUDE, ValidationError
import pytest
import datetime


class DogSchema(BaseSchemaTransform):
    class Meta:
        unknown = EXCLUDE

    NAME = fields.Str(data_key='name')
    ACTION_RUN = transform_fields.NestedValueField(
        nested_key='action.run',
        type_class=fields.Str
    )
    ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
        nested_key='action.sound.normal',
        type_class=fields.Str
    )
    ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
        nested_key='action.sound.hungry',
        type_class=fields.Str
    )


class TimeTransform(BaseSchemaTransform):
    class Meta:
        unknown = EXCLUDE

    start_time = transform_fields.DatetimeFromTimeStamp()
    end_time = transform_fields.DatetimeFromTimeStamp()
    amount_of_time_start = transform_fields.NestedValueField(
        nested_key='amount_of_time.start',
        type_class=transform_fields.DatetimeFromTimeStamp
    )
    amount_of_time_end = transform_fields.NestedValueField(
        nested_key='amount_of_time.end',
        type_class=transform_fields.DatetimeFromTimeStamp
    )


class TestCustomFields:

    def test_get_value_of_nested_value_field(self):
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

    def test_validate_of_nested_value_field(self):
        dog_raw_data = {
            'name': 'Husky',
            'action': {
                'run': 1,
            }
        }

        with pytest.raises(ValidationError):
            DogSchema.transform(dog_raw_data)

    def test_datetime_from_timestamp_field(self):
        raw_data = {
            "start_time": 1640995200,
            "end_time": 1640995201
        }

        result = TimeTransform.transform(raw_data)
        assert result == {
            "start_time": datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            "end_time": datetime.datetime(2022, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
        }

    def test_datetime_from_timestamp_in_nested_value_field(self):
        raw_data = {
            "amount_of_time": {
                "start": 1640995200,
                "end": 1640995201
            }
        }
        result = TimeTransform.transform(raw_data)
        assert result == {
            "amount_of_time_start": datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            "amount_of_time_end": datetime.datetime(2022, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
        }

