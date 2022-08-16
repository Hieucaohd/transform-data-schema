************************************************************
transform-data-schema: simple transform and validate schema
***********************************************************

**transform-data-schema** is a library for converting complex datatypes, such as objects, to and from native Python datatypes.

    from transform_data_schema import (
        BaseSchemaTransform, 
        EXCLUDE, 
        fields, 
        transform_fields, 
        ValidationError
    )


    class EventJBTransformSchema(BaseSchemaTransform):
        class Meta:
            unknown = EXCLUDE

        ID = fields.Str()
        PROFILE_ID = transform_fields.NestedValueField(
            nested_key='data_event.profile_id',
            type_class=fields.Str,
            required=True
        )
        JOURNEY_ID = transform_fields.NestedValueField(
            nested_key='data_event.journey_id',
            type_class=fields.Str,
            required=True
        )
        MC_ID = transform_fields.NestedValueField(
            nested_key='data_event.master_campaign_id',
            type_class=fields.Str,
            required=True
        )
        MERCHANT_ID = transform_fields.NestedValueField(
            nested_key='data_event.merchant_id',
            type_class=fields.Str,
            required=True
        )
        DATA_TYPE = fields.Str(data_key='event_type')
        ACTION_TIME = transform_fields.NestedValueField(
            nested_key='data_event.action_time',
            type_class=transform_fields.DatetimeFromTimeStamp,
            required=True
        )
        NODE_CODE = transform_fields.NestedValueField(
            nested_key='data_event.node_code',
            type_class=fields.Str,
        )
        NODE_ID = transform_fields.NestedValueField(
            nested_key='data_event.node_id',
            type_class=fields.Str
        )
    
    if __name__ == '__main__':
        raw_data = {
            "message_id": "19db4e86-0cef-11ed-9d73-aea73dddcfef",
            "data_event": {
                "action_time": 1658845656.471722,
                "journey_id": "1a596c15-3ccb-4d51-8d75-03223c5bce8e",
                "merchant_id": "1b99bdcf-d582-4f49-9715-1b61dfff3924",
                "node_id": "64690a9e-e807-4b2a-8da2-f2d28d085fd2",
                "node_code": "WEB_PUSH",
                "event_type": "IN_NODE",
                "profile_id": "ff5d808c-5a28-415f-b60d-9070519e7f1a",
                "master_campaign_id": "a065a9fd-2341-468b-8580-dba1cc4b3459",
                "event_id": "061dbe38-b5db-4470-a1e5-8e2ce2e14851"
            },
            "event_type": "profile_in_node"
        }
        result = EventJBTransformSchema.transform(raw_data)
        pprint(result, indent=2)
        
        """
        { 
            'ACTION_TIME': datetime.datetime(2022, 7, 26, 14, 27, 36, 471722, tzinfo=datetime.timezone.utc),
            'DATA_TYPE': 'profile_in_node',
            'JOURNEY_ID': '1a596c15-3ccb-4d51-8d75-03223c5bce8e',
            'MC_ID': 'a065a9fd-2341-468b-8580-dba1cc4b3459',
            'MERCHANT_ID': '1b99bdcf-d582-4f49-9715-1b61dfff3924',
            'NODE_CODE': 'WEB_PUSH',
            'NODE_ID': '64690a9e-e807-4b2a-8da2-f2d28d085fd2',
            'PROFILE_ID': 'ff5d808c-5a28-415f-b60d-9070519e7f1a'
        }
        """

In short, transform-data-schema can be used to:

- **Validate** input data.
- **Deserialize** input data to app-level objects.

Get It Now
==========

    $ pip install -U transform-data-schema


Requirements
============

- Python >= 3.7


