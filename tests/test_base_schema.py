from src.transform_data_schema import BaseSchemaTransform, transform_fields, EXCLUDE, ActionWhenValidateErrorField


class TestBaseSchemaTransform:
    def test_transform_1(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', required=True)
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                allow_none=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
                required=True
            )

        dog_raw_data = {
            'name': 'miu miu',
            'action': {
                'run': 'very fast',
                'sound': {
                    'normal': 'go go',
                    'hungry': 'ya ya'
                }
            }
        }

        result_expect = {
            'NAME': 'miu miu',
            'ACTION_RUN': 'very fast',
            'ACTION_SOUND_WHEN_NORMAL': 'go go',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya'
        }

        result = DogSchema.transform(dog_raw_data)
        assert result == result_expect

    def test_transform_2(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', required=True)
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                allow_none=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
                required=True
            )

        dog_raw_data = {
            'name': 'miu miu',
            'action': {
                'run': None,
                'sound': {
                    'normal': 'go go',
                    'hungry': 'ya ya'
                }
            }
        }

        result_expect = {
            'NAME': 'miu miu',
            'ACTION_RUN': None,
            'ACTION_SOUND_WHEN_NORMAL': 'go go',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya'
        }

        result = DogSchema.transform(dog_raw_data)
        assert result == result_expect

    def test_transform_3(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', required=True)
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                allow_none=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
                required=True
            )

        dog_raw_data = {
            'name': 'miu miu',
            'action': {
                'sound': {
                    'normal': 'go go',
                    'hungry': 'ya ya'
                }
            }
        }

        result_expect = {
            'NAME': 'miu miu',
            'ACTION_SOUND_WHEN_NORMAL': 'go go',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya'
        }

        result = DogSchema.transform(dog_raw_data)
        assert result == result_expect

    def test_transform_4(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', required=True)
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                allow_none=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
                required=True
            )

        dog_raw_data = {
            'name': 'miu miu',
            'action': {
                'sound': {
                    'hungry': 'ya ya'
                }
            }
        }

        result_expect = {
            'NAME': 'miu miu',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya'
        }

        assert DogSchema.transform(dog_raw_data) == result_expect

    def test_transform_5(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', required=True)
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
                required=True
            )

        dog_raw_data = {
            'name': 'miu miu',
            'action': {
                'run': 'very fast',
                'sound': {
                    'hungry': 'ya ya',
                    'normal': 'uo uo'
                }
            }
        }

        result_expect = {
            'NAME': 'miu miu',
            'ACTION_SOUND_WHEN_HUNGRY': 'ya ya',
            'ACTION_SOUND_WHEN_NORMAL': 'uo uo'
        }

        assert DogSchema.transform(dog_raw_data) == result_expect

    def test_action_remove_field_validate_error_1(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name')
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                allow_none=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
            )

        dog_raw_data = {
            'name': 1,
            'action': {
                'sound': {
                    'normal': 'meo meo',
                    'hungry': 1
                }
            }
        }

        result_expect = {
            'ACTION_SOUND_WHEN_NORMAL': 'meo meo'
        }

        assert DogSchema.transform(
            dog_raw_data,
            action_when_validate_error=ActionWhenValidateErrorField.REMOVE_FIELD
        ) == result_expect

    def test_action_remove_field_validate_error_2(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name')
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                allow_none=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
            )

        dog_raw_data = {
            'name': 1,
            'action': {
                'sound': {
                    'normal': 'meo meo',
                    'hungry': 1
                }
            }
        }

        result_expect = {
            'ACTION_SOUND_WHEN_NORMAL': 'meo meo'
        }

        assert DogSchema.transform(
            dog_raw_data,
            action_when_validate_error=ActionWhenValidateErrorField.REMOVE_FIELD
        ) == result_expect

    def test_action_remove_field_validate_error_3(self):
        class Action(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            RUN = transform_fields.Str(data_key='run')
            SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='sound.normal',
                type_class=transform_fields.Str
            )
            SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='sound.hungry',
                type_class=transform_fields.Str
            )

        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', allow_none=True)
            ACTION = transform_fields.Nested(
                lambda: Action(action_when_validate_error=ActionWhenValidateErrorField.REMOVE_FIELD),
                data_key='action'
            )

        dog_data_raw = {
            'name': 'meo meo',
            'action': {
                'run': 'very fast',
                'sound': {
                    'normal': 'miu miu',
                    'hungry': 1
                }
            }
        }

        data_expect = {
            'NAME': 'meo meo',
            'ACTION': {
                'RUN': 'very fast',
                'SOUND_WHEN_NORMAL': 'miu miu'
            }
        }

        result = DogSchema.transform(dog_data_raw, action_when_validate_error=ActionWhenValidateErrorField.REMOVE_FIELD)
        assert result == data_expect

    def test_get_require_fields(self):
        class DogSchema(BaseSchemaTransform):
            class Meta:
                unknown = EXCLUDE

            NAME = transform_fields.Str(data_key='name', required=True, allow_none=True)
            ACTION_RUN = transform_fields.NestedValueField(
                nested_key='action.run',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
                nested_key='action.sound.normal',
                type_class=transform_fields.Str,
                required=True
            )
            ACTION_SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
                nested_key='action.sound.hungry',
                type_class=transform_fields.Str,
                required=True
            )

        expect_require_fields = ['NAME', 'ACTION_RUN', 'ACTION_SOUND_WHEN_NORMAL', 'ACTION_SOUND_WHEN_HUNGRY']
        for require_field in list(DogSchema.get_require_fields().keys()):
            assert require_field in expect_require_fields


if __name__ == '__main__':
    from pprint import pprint

    class Action(BaseSchemaTransform):
        class Meta:
            unknown = EXCLUDE

        RUN = transform_fields.Str(data_key='run')
        SOUND_WHEN_NORMAL = transform_fields.NestedValueField(
            nested_key='sound.normal',
            type_class=transform_fields.Str
        )
        SOUND_WHEN_HUNGRY = transform_fields.NestedValueField(
            nested_key='sound.hungry',
            type_class=transform_fields.Str
        )


    class DogSchema(BaseSchemaTransform):
        class Meta:
            unknown = EXCLUDE

        NAME = transform_fields.Str(data_key='name', allow_none=True)
        ACTION = transform_fields.Nested(
            lambda: Action(action_when_validate_error=ActionWhenValidateErrorField.REMOVE_FIELD),
            data_key='action'
        )

    dog_data_raw = {
        'name': 'meo meo',
        'action': {
            'run': 'very fast',
            'sound': {
                'normal': 'miu miu',
                'hungry': 1
            }
        }
    }

    result = DogSchema.transform(dog_data_raw, action_when_validate_error=ActionWhenValidateErrorField.REMOVE_FIELD)
    pprint(result)

