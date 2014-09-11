from schema import NameSpacedSchema, BaseSchema, fields, Linked


class EventTypeSerializer(NameSpacedSchema):
    class Meta():
        primary_key = 'event_type_id'
        plural_name = 'event_types'
        name = 'event_type'
        additional = ('event_type_id', 'organization_id')


class EventSerializer(NameSpacedSchema):
    class Meta():
        primary_key = 'event_id'
        plural_name = 'events'
        name = 'event'
        additional = ('event_id', 'name')

    event_type = Linked(EventTypeSerializer)


class TicketTypeSerializer(NameSpacedSchema):
    class Meta():
        primary_key = 'ticket_type_id'
        plural_name = 'ticket_types'
        name = 'ticket_type'
        additional = ("vat_factor", "name", "price", "ticket_type_id", "identifier", "data")

    event_type = Linked(EventTypeSerializer)


class TicketReservationSerializer(NameSpacedSchema):
    class Meta:
        primary_key = 'uuid'
        plural_name = 'tickets'
        name = 'ticket'
        additional = ('price', 'fee', 'vat', 'fee_vat', 'uuid', 'data',)

    events = Linked(EventSerializer, many=True)
    ticket_type = Linked(TicketTypeSerializer)


class ReservationSerializer(BaseSchema):
    class Meta:
        primary_key = 'reservation_id'
        plural_name = 'reservations'
        name = 'reservation'
        additional = ('data', 'reservation_id')

    last_touched = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    created = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    ticket_reservations = fields.Nested(TicketReservationSerializer, attribute='tickets', many=True)


class TicketSerializer(NameSpacedSchema):
    class Meta():
        primary_key = 'ticket_id'
        name = 'ticket'
        plural_name = 'tickets'

        additional = ('ticket_id', 'price', 'fee', 'fee_vat')

    user = Linked('UserSerializer', attribute="owner")


class UserSerializer(NameSpacedSchema):
    class Meta():
        primary_key = 'user_id'
        name = 'user'
        plural_name = 'users'

        additional = ('user_id', 'email', 'first_name', 'last_name')


class PurchaseSerializer(BaseSchema):
    ROOT = "purchases"

    class Meta():
        name = "purchase"
        primary_key = 'purchase_id'
        additional = ('purchase_id', 'fee', 'finalized', 'created', 'amount', 'fee_vat', 'vat')

    tickets = Linked(TicketSerializer, many=True)
    user = Linked(UserSerializer)


class EventTypeSerializer2(BaseSchema):
    class Meta():
        name = "event_type"
        primary_key = 'event_type_id'
        additional = ('event_type_id',)

    ticket_types = Linked(TicketTypeSerializer, many=True)
    events = Linked(EventSerializer, many=True)

from data import purchase, reservation, event_type
import json
serialized = PurchaseSerializer(purchase)
serialized = ReservationSerializer(reservation)
serialized = EventTypeSerializer2(event_type)
print json.dumps(serialized.data, indent=2, separators=(',', ': '))
