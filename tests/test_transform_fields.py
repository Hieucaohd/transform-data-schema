from src.transform_data_schema import BaseSchemaTransform, transform_fields, EXCLUDE, ValidationError
from marshmallow import validate
import pytest
import datetime


class TestNestedValueField:

    def test_get_value_of_nested_value_field(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name')
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str
            )

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
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name')
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str
            )

        dog_raw_data = {
            'name': 'Husky',
            'action': {
                'run': 1,
            }
        }

        with pytest.raises(ValidationError):
            DogSchema.transform(dog_raw_data)


class TestDateTimeFromTimestampField:
    def test_datetime_from_timestamp_field(self):
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


class TestTransformFieldsStr:
    def test_str_transform_field_1(self):
        class CatSchema(BaseSchemaTransform):
            id = transform_fields.Str()
            name_vietnamese = transform_fields.Str(
                validate=validate.Length(max=2),
                value_when_validate_error='baobao',
                allow_none=True
            )

        cat_data = {
            'id': "1",
            'name_vietnamese': 'hieucao'
        }
        result = CatSchema.transform(cat_data)
        assert result == {
            'id': "1",
            'name_vietnamese': 'baobao'
        }

    def test_str_transform_field_2(self):
        class CatSchema(BaseSchemaTransform):
            id = transform_fields.Str()
            name_vietnamese = transform_fields.Str(
                validate=validate.Length(max=2),
                value_when_validate_error='baobao',
                allow_none=True
            )

        cat_data = {
            'id': "1",
            'name_vietnamese': 'hi'
        }
        result = CatSchema.transform(cat_data)
        assert result == {
            'id': "1",
            'name_vietnamese': 'hi'
        }

    def test_raise_validate_error_of_transform_field_str(self):
        class CatSchema(BaseSchemaTransform):
            id = transform_fields.Str()
            name_vietnamese = transform_fields.Str(
                validate=validate.Length(max=2),
            )

        cat_data = {
            'id': "1",
            'name_vietnamese': 'hieucao'
        }

        with pytest.raises(ValidationError):
            result = CatSchema.transform(cat_data)


class TestTransformFieldInt:
    def test_int_transform_field_1(self):
        class CatSchema(BaseSchemaTransform):
            age = transform_fields.Int(value_when_validate_error=None, strict=True)
            name = transform_fields.Str(
                value_when_validate_error=None,
                validate=validate.Length(max=2)
            )

        cat_data = {
            'age': '3',
            'name': '333'
        }
        result = CatSchema.transform(cat_data)
        assert result == {
            'age': None,
            'name': None
        }

    def test_int_transform_field_2(self):
        class CatSchema(BaseSchemaTransform):
            age = transform_fields.Int(value_when_validate_error=None, strict=True)
            name = transform_fields.Str(
                value_when_validate_error=None,
                validate=validate.Length(max=2)
            )

        cat_data = {
            'age': 1,
            'name': 'ba'
        }

        result = CatSchema.transform(cat_data)
        assert result == {
            'age': 1,
            'name': 'ba'
        }

    def test_raise_validate_error(self):
        class CatSchema(BaseSchemaTransform):
            age = transform_fields.Int(strict=True)

        cat_data = {
            'age': 'hehe',
        }

        with pytest.raises(ValidationError):
            result = CatSchema.transform(cat_data)


class TestTransformFieldFloat:
    def test_float_transform_field_1(self):
        class CatSchema(BaseSchemaTransform):
            age = transform_fields.Float(value_when_validate_error=None, strict=True)

        cat_data = {
            'age': 'ii',
        }
        result = CatSchema.transform(cat_data)
        assert result == {
            'age': None,
        }

    def test_float_transform_field_2(self):
        class CatSchema(BaseSchemaTransform):
            age = transform_fields.Float(value_when_validate_error=None, strict=True)

        cat_data = {
            'age': 1,
        }

        result = CatSchema.transform(cat_data)
        assert result == {
            'age': 1,
        }

    def test_raise_validate_error(self):
        class CatSchema(BaseSchemaTransform):
            age = transform_fields.Float(strict=True)

        cat_data = {
            'age': 'hehe',
        }

        with pytest.raises(ValidationError):
            result = CatSchema.transform(cat_data)


