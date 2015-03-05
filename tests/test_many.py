import unittest

from serializer.schema import Linked, Schema


class UserManySchema(Schema):
    class Meta():
        primary_key = 'user_id'
        type = "users"

        additional = ()


class OrganizationManySchema(Schema):
    class Meta():
        primary_key = 'organization_id'
        type = "organizations"

        additional = ()

    owners = Linked(UserManySchema, many=True, attribute="users")

class EventSchema(Schema):
    class Meta():
        primary_key = 'event_id'
        type = 'events'

        additional = ('name',)

    organization = Linked(OrganizationManySchema)


events = [{
    'event_id': 1,
    'name': 'Snoop Dogg',
    'organization': {
        'organization_id': 1,
        'users': []
    }
}, {
    'event_id': 2,
    'name': 'Justin Bieber',
    'organization': {
        'organization_id': 2,
        'users': [{
            'user_id': 1
        }, {
            'user_id': 2
        }]
    }
}]


class ManyTest(unittest.TestCase):
    def test_empty(self):
        serialized = EventSchema().serialize([], many=True)

        self.assertDictEqual(serialized, {
            "events": [],
            "links": {},
            "linked": {}
        })

    def test_many(self):
        serialized = EventSchema().serialize(events, many=True)

        self.assertDictEqual(serialized, {
            "events": [
                {
                    "id": 1,
                    "name": "Snoop Dogg",
                    "links": {
                        "organization": 1
                    }
                },
                {
                    "id": 2,
                    "name": "Justin Bieber",
                    "links": {
                        "organization": 2
                    }
                }
            ],
            "links": {
                "events.organization": {
                    "type": "organizations"
                },
                "organizations.owners": {
                    "type": "users"
                }
            },
            "linked": {
                "organizations": [
                    {
                        "id": 1,
                        "links": {
                            "owners": []
                        }
                    },
                    {
                        "id": 2,
                        "links": {
                            "owners": [
                                1,
                                2
                            ]
                        }
                    }
                ],
                "users": [{'id': user['user_id']} for user in events[1]['organization']['users']]
            }
        })


