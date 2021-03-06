import unittest

from serializer.schema import Linked, Schema


class AccessorTest(unittest.TestCase):
    def test_asd(self):
        class OrganizationMembershipSchema(Schema):
            class Meta:
                primary_key = 'organization_id'
                type = 'organizations'

                additional = ('name',)

        class UserOrganizationSchema(Schema):
            class Meta:
                primary_key = 'user_id'
                type = 'users'

                additional = ('name',)

            organizations = Linked(OrganizationMembershipSchema, many=True, attribute="memberships.organization")

        organizations = [
            {"organization_id": 2, "name": "Brukbar"},
            {"organization_id": 3, "name": "Samfundet"}
        ]

        user = {
            "user_id": 1,
            "name": "Bob",
            "memberships": [
                {"organization": organizations[0]},
                {"organization": organizations[1]}
            ]
        }

        serialized_user = UserOrganizationSchema().serialize(user)

        self.assertDictEqual(serialized_user, {
            "users": {
                "id": user['user_id'],
                "name": user['name'],
                "links": {
                    "organizations": [org['organization_id'] for org in organizations]
                }
            },
            "linked": {
                "organizations": [{
                    "id": org['organization_id'],
                    "name": org['name']
                } for org in organizations]
            },
            "links": {
                "users.organizations": {
                    "type": "organizations"
                }
            }
        })
