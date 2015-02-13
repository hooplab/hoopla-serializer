import unittest

from serializer.schema import Embedded, Schema, Linked


ticket_type = {
    'ticket_type_id': 42,
    'fee': 1500,
    'name': 'Student',
    'price': 20000
}

reservation = {
    'last_touched': '2014-08-19T11:13:22Z',
    'reservation_id': 1337,
    'created': '2014-08-19T11:13:22Z',
    'ticket_reservations': [
        {
            'uuid': '8d696787-c301-4faf-9ab8-7960d20ce49a',
            'fee': 1500,
            'price': 20000,
            'ticket_type': ticket_type
        },
        {
            'uuid': '775cacc8-82bb-4208-bc3f-a9e25522f696',
            'fee': 1500,
            'price': 20000,
            'ticket_type': ticket_type
        }
    ]
}


class TicketTypeSchema(Schema):
    class Meta:
        primary_key = 'ticket_type_id'
        type = 'ticket_types'

        additional = ('ticket_type_id', 'fee', 'name', 'price')


class TicketReservationSchema(Schema):
    class Meta:
        primary_key = 'uuid'
        type = 'ticket_reservations'

        additional = ('uuid', 'fee', 'price')

    ticket_type = Linked(TicketTypeSchema)


class ReservationSchema(Schema):
    class Meta:
        primary_key = 'reservation_id'
        type = 'reservations'

        additional = ('reservation_id', 'last_touched', 'created')

    ticket_reservations = Embedded(TicketReservationSchema, many=True)


class EmbeddedSchemaTest(unittest.TestCase):
    def test_embedding(self):

        serialized_reservation = ReservationSchema().serialize(reservation)

        self.assertDictEqual(serialized_reservation, {
            'reservations': {
                'last_touched': reservation['last_touched'],
                'created': reservation['created'],
                'reservation_id': reservation['reservation_id'],
                'ticket_reservations': [
                    {
                        'price': ticket['price'],
                        'fee': ticket['fee'],
                        'uuid': ticket['uuid'],
                        'links': {
                            'ticket_type': ticket['ticket_type']['ticket_type_id']
                        }
                    } for ticket in reservation['ticket_reservations']
                ]
            },
            'linked': {
                'ticket_types': [ticket_type]
            },
            'links': {
                'reservations.ticket_reservations': {
                    'type': 'ticket_reservations'
                },
                'reservations.ticket_reservations.ticket_type': {
                    'type': 'ticket_types'
                }
            }
        })
