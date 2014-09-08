from datetime import datetime
import itertools
from marshmallow import Serializer, fields, pprint

class Embedded(fields.Nested):
    pass

class Linked(fields.Nested):
    pass

class BaseSerializer(Serializer):
    pass

@BaseSerializer.data_handler
def jsonapify(serializer, data, obj):
    def get_data(schema, data):
        k = schema.Meta.primary_key
        n = schema.Meta.name
        return {n: {data[k]: data}}

    def update_map(a, b):
        for k, v in b.items():
            if k in a:
                a[k].update(v)
            else:
                a[k] = v
        return a.copy()

    def depth_first(schema, data):
        linked = dict()
        for field in schema.declared_fields.values():
            name = field.name
            if isinstance(field, fields.Nested):
                if isinstance(field, Embedded):
                    if field.many:
                        for e in data[name]:
                            for f in field.schema.fields.values():
                                if isinstance(f, Linked):
                                    if f.many:
                                        links = {f.schema.Meta.name: [o[f.schema.Meta.primary_key] for o in e[f.schema.Meta.name]]}
                                    else:
                                        links = {f.schema.Meta.name: e[f.schema.Meta.single_name][f.schema.Meta.primary_key]}
                                    if 'links' in e:
                                        e['links'].update(links)
                                    else:
                                        e['links'] = links

                if field.many:
                    for e in data[name]:
                        p = depth_first(field.schema, e)
                        linked = update_map(linked, p)
                else:
                    p = depth_first(field.schema, data[name])
                    linked = update_map(linked, p)
                if isinstance(field, Linked):
                    del data[name]

        return update_map(linked, get_data(schema, data))


    linked = depth_first(serializer, data)

    for key, val in linked.items():
        linked[key] = val.values()

    del linked[serializer.ROOT]

    return {
        serializer.ROOT: data,
        "linked": linked
    }


class EventTypeSerializer(Serializer):
    class Meta():
        primary_key = 'event_type_id'
        name = 'event_types'
        additional = ('event_type_id', 'organization_id')


class EventSerializer(Serializer):
    class Meta():
        primary_key = 'event_id'
        name = 'events'
        single_name = 'event'
        additional = ('event_id',)

    event_type = Linked(EventTypeSerializer)


class TicketTypeSerializer(Serializer):
    class Meta():
        primary_key = 'ticket_type_id'
        name = 'ticket_types'
        single_name = 'ticket_type'
        additional = ("vat_factor", "name", "price", "ticket_type_id", "event_type_id", "identifier", "data")


class TicketReservationSerializer(Serializer):
    class Meta:
        primary_key = 'uuid'
        name = 'tickets'
        additional = ('price', 'fee', 'vat', 'fee_vat', 'uuid', 'data')

    events = Linked(EventSerializer, many=True)
    ticket_type = Linked(TicketTypeSerializer)


class ReservationSerializer(BaseSerializer):
    class Meta:
        primary_key = 'reservation_id'
        name = 'reservations'
        additional = ('data', 'reservation_id')

    ROOT = 'reservations'
    last_touched = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    created = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    ticket_reservations = Embedded(TicketReservationSerializer, attribute='tickets', many=True)



reservation = {
    "tickets": [
        {
            "uuid": "389aa88d-728b-43d4-a647-6e60c026853b",
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
                "identifier": "tt-student",
                "data": {},
            },
            "fee_vat": 0,
            "purchase_ref": "",
            "data": {},
            "events": [
                {
                    "event_id": 1615163368,
                    "event_type": {
                        "event_type_id": 1,
                        "organization_id": "krogstad"
                    }
                },
                {
                    'event_id': 783921,
                    "event_type": {
                        "event_type_id": 2,
                        "organization_id": "hansen"
                    }
                }
            ],
            "vat": 0
        },
        {
            "uuid": "389aa88d-728b-43d4-a647-6e60c026853b",
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
                "event_type_id": 1044709619,
                "identifier": "tt-voksen",
                "data": {},
            },
            "fee_vat": 0,
            "purchase_ref": "",
            "data": {},
            "events": [
                {
                    "event_id": 1615163368,
                    "event_type": {
                        "event_type_id": 1,
                        "organization_id": "krogstad"
                    }
                },
                {
                    'event_id': 783921,
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
