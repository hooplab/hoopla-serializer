from datetime import datetime
from marshmallow import Serializer, fields, pprint


class TicketReservationSerializer(Serializer):
    links = fields.Method('get_links')

    def get_links(self, obj):
        return {
            'ticket_type': obj['ticket_type']['ticket_type_id'],
            'event': obj['event_id']
        }

    class Meta:
        additional = ('price', 'fee', 'vat', 'fee_vat', 'uuid', 'data')


class ReservationSerializer(Serializer):
    ROOT = 'reservations'
    last_touched = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    created = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    ticket_reservations = fields.Nested(TicketReservationSerializer, attribute='tickets', many=True)

    class Meta:
        additional = ('data', 'reservation_id')


@ReservationSerializer.data_handler
def jsonapify(serializer, data, obj):
    return {
        serializer.ROOT: data,
        "linked": get_links(obj, {
            'ticket_types': 'tickets.ticket_type'
        })
    }


def get_links(obj, linked):
    return {key: parse(obj, keystr.split(".")) for key, keystr in linked.items()}


def parse(obj, keys):
    key = keys[0]
    if isinstance(obj, list):
        return [parse(e, keys) for e in obj]
    if len(keys) == 1:
        return obj[key]
    else:
        return parse(obj[key], keys[1:])


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
            "event": {
                "event_id": 1615163368
            },
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
            "event": {
                "event_id": 1615163368
            },
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
