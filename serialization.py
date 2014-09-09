from datetime import datetime
from marshmallow import Serializer as MarshmallowSerializer, fields


class Embedded(fields.Nested):
    pass


class Linked(fields.Nested):
    pass


class Serializer(MarshmallowSerializer):
    @property
    def nested_fields(self):
        return [field for field in self.fields.values() if isinstance(field, fields.Nested)]

@Serializer.data_handler
def jsonapify(serializer, data, obj):
    def add_links_from_field(field, data):
        if not isinstance(field, Linked):
            return

        plural_name = field.schema.Meta.plural_name
        primary_key = field.schema.Meta.primary_key
        name = field.schema.Meta.name
        if field.many:
            links = {plural_name: [o[primary_key] for o in data[plural_name]]}
        else:
            links = {plural_name: data[name][primary_key]}
        if 'links' in data:
            data['links'].update(links)
        else:
            data['links'] = links

    def add_links_form_schema(schema, data):
        for field in schema.nested_fields:
            add_links_from_field(field, data)

            name = field.name
            if field.many:
                for e in data[name]:
                    add_links_form_schema(field.schema, e)
            else:
                add_links_form_schema(field.schema, data[name])

    def get_linked():
        def get_data(schema, data):
            k = schema.Meta.primary_key
            n = schema.Meta.plural_name
            return {n: {data[k]: data}}

        def update_map(a, b):
            for k, v in b.items():
                if k in a:
                    a[k].update(v)
                else:
                    a[k] = v

        def recur_schema(schema, data, linked):
            for field in schema.nested_fields:
                recur_field(field, data, linked)

        def recur_field(field, data, linked):
            name = field.name
            if field.many:
                for schema_data in data[name]:
                    recur_schema(field.schema, schema_data, linked)
                    if isinstance(field, Linked):
                        update_map(linked, get_data(field.schema, schema_data))
            else:
                recur_schema(field.schema, data[name], linked)
                if isinstance(field, Linked):
                    update_map(linked, get_data(field.schema, data[name]))

            if isinstance(field, Linked):
                del data[name]

        linked = dict()
        recur_schema(serializer, data, linked)
        for key, val in linked.items():
            linked[key] = val.values()
        return linked

    add_links_form_schema(serializer, data)
    return {
        serializer.ROOT: data,
        "linked": get_linked()
    }


class EventTypeSerializer(Serializer):
    class Meta():
        primary_key = 'event_type_id'
        plural_name = 'event_types'
        name = 'event_type'
        additional = ('event_type_id', 'organization_id')


class EventSerializer(Serializer):
    class Meta():
        primary_key = 'event_id'
        plural_name = 'events'
        name = 'event'
        additional = ('event_id', 'name')

    event_type = Linked(EventTypeSerializer)


class TicketTypeSerializer(Serializer):
    class Meta():
        primary_key = 'ticket_type_id'
        plural_name = 'ticket_types'
        name = 'ticket_type'
        additional = ("vat_factor", "name", "price", "ticket_type_id", "event_type_id", "identifier", "data")

    event_type = Linked(EventTypeSerializer)


class TicketReservationSerializer(Serializer):
    class Meta:
        primary_key = 'uuid'
        plural_name = 'ticket_reservations'
        name = 'ticket_reservation'
        additional = ('price', 'fee', 'vat', 'fee_vat', 'uuid', 'data')

    events = Linked(EventSerializer, many=True)
    ticket_type = Linked(TicketTypeSerializer)


class ReservationSerializer(Serializer):
    class Meta:
        primary_key = 'reservation_id'
        plural_name = 'reservations'
        additional = ('data', 'reservation_id')

    ROOT = 'reservations'
    last_touched = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    created = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    ticket_reservations = Embedded(TicketReservationSerializer, attribute='tickets', many=True)



reservation = {
    "tickets": [
        {
            "uuid": "389aa88d-728b-a647-43d4-026853b6e60c",
            "fee": 2500,
            "event_id": 1615163368,
            "price": 25000,
            "ticket_type_id": 2217311692,
            "txid": 252797,
            "ticket_type": {
                "vat_factor": 0,
                "name": "Student",
                "price": 25000,
                "ticket_type_id": 2217311692,
                "event_type_id": 1044709619,
                "event_type": {
                    "event_type_id": 1,
                    "organization_id": "krogstad"
                },
                "identifier": "tt-student",
                "data": {},
            },
            "fee_vat": 0,
            "purchase_ref": "",
            "data": {},
            "events": [
                {
                    "event_id": 1,
                    "name": "Gatebil",
                    "event_type": {
                        "event_type_id": 1,
                        "organization_id": "krogstad"
                    }
                },
                {
                    "event_id": 2,
                    "name": "Pultostfestival",
                    "event_type": {
                        "event_type_id": 2,
                        "organization_id": "hansen"
                    }
                }
            ],
            "vat": 0
        },
        {
            "uuid": "7a89c278-728b-43d4-a647-6e60c026853b",
            "fee": 2500,
            "event_id": 1615163368,
            "price": 25000,
            "ticket_type_id": 2217311692,
            "txid": 252797,
            "ticket_type": {
                "vat_factor": 0,
                "name": "Voksen",
                "price": 25000,
                "ticket_type_id": 78392173921,
                "event_type": {
                    "event_type_id": 1,
                    "organization_id": "krogstad"
                },
                "event_type_id": 1044709619,
                "identifier": "tt-voksen",
                "data": {},
            },
            "fee_vat": 0,
            "purchase_ref": "",
            "data": {},
            "events": [
                {
                    "event_id": 1,
                    "name": "Gatebil",
                    "event_type": {
                        "event_type_id": 1,
                        "organization_id": "krogstad"
                    }
                },
                {
                    "event_id": 3,
                    "name": "Vaernes airshow",
                    "event_type": {
                        "event_type_id": 2,
                        "organization_id": "hansen"
                    }
                }
            ],
            "vat": 0
        }
    ],
    "last_touched": datetime.now(),
    "reservation_id": "2321441891",
    "created": datetime.now(),
    "data": {}
}
serialized = ReservationSerializer(reservation)

import json
print json.dumps(serialized.data, indent=2, separators=(',', ': '))
