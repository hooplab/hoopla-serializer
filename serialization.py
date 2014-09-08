from datetime import datetime
import itertools
from marshmallow import Serializer, fields, pprint


class BaseSerializer(Serializer):
    pass

@BaseSerializer.data_handler
def jsonapify(serializer, data, obj):
    def parse(obj, keys, serializer):
        key = keys[0]
        if isinstance(obj, list):
            lst = [parse(e, keys, serializer) for e in obj]
            if isinstance(lst[0], list):
                return list(itertools.chain.from_iterable(lst))
            else:
                return lst
        if len(keys) == 1:
            raw = obj[key]
            if isinstance(raw, list):
                return [serializer(e).data for e in raw]
            else:
                return serializer(raw).data
        else:
            return parse(obj[key], keys[1:], serializer)

    def get_linked(obj, linked):
        return {key: parse(obj, obje['key'].split("."), obje['serializer']) for key, obje in linked.items()}

    return {
        serializer.ROOT: data,
        "linked": get_linked(obj, serializer.LINKED)
    }


class EventTypeSerializer(Serializer):
    class Meta():
        additional = ('event_type_id', 'organization_id')


class EventSerializer(Serializer):
    class Meta():
        additional = ('event_id',)


class TicketTypeSerializer(Serializer):
    class Meta():
        additional = ("vat_factor", "name", "price", "ticket_type_id", "event_type_id", "identifier", "data")


class TicketReservationSerializer(Serializer):
    links = fields.Method('get_links')

    def get_links(self, obj):
        return {
            'ticket_type': obj['ticket_type']['ticket_type_id'],
            'event': obj['event_id']
        }

    class Meta:
        additional = ('price', 'fee', 'vat', 'fee_vat', 'uuid', 'data')


class ReservationSerializer(BaseSerializer):
    ROOT = 'reservations'
    LINKED = {
        'ticket_types': {
            'key': 'tickets.ticket_type',
            'serializer': TicketTypeSerializer
        },
        'event_types': {
            'key': 'tickets.events.event_type',
            'serializer': EventTypeSerializer
        },
        'events': {
            "key": 'tickets.events',
            "serializer": EventSerializer
        },
    }
    last_touched = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    created = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    ticket_reservations = fields.Nested(TicketReservationSerializer, attribute='tickets', many=True)

    class Meta:
        additional = ('data', 'reservation_id')


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
