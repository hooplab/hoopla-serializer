import unittest

from serializer.schema import Linked, Schema


class UserSchema(Schema):
    class Meta:
        primary_key = 'user_id'
        type = 'users'

        additional = ('user_id', 'name')


class OrganizationSchema(Schema):
    class Meta:
        primary_key = 'organization_id'
        type = 'organizations'

        additional = ('organization_id', 'name')
    owner = Linked("UserSchema")


class AdminSchema(Schema):
    class Meta:
        primary_key = 'admin_id'
        type = 'admins'

        additional = ('admin_id', 'name')

    orgs = Linked("OrganizationSchema", many=True)


user_E = {
    "user_id": 1,
    "name": "Pelle",
}

user_F = {
    "user_id": 2,
    "name": "Hans",
}

organization_B = {
    "organization_id": 1,
    "name": "Brukbar",
    "owner": user_E
}

organization_C = {
    "organization_id": 2,
    "name": "Naboen",
    "owner": user_E
}

organization_D = {
    "organization_id": 3,
    "name": "To rom",
    "owner": user_F
}

admin_A = {
    "admin_id": 1,
    "name": "Sjefen",
    "orgs": [organization_B, organization_C, organization_D],
}

"""
     A      A = admin_A
   / | \
  B  C  D   B = organization_B, C = organization_C, D = organization_D
   \ |  |
     E  F   E = user_E, F = user_F
"""


class NestedSchemaTest(unittest.TestCase):
    def test_simple_document(self):
        serialized_user = UserSchema().serialize(user_E)

        self.assertDictEqual(serialized_user, {
            'users': user_E,
            'linked': {},
            'links': {}
        })

    def test_nested_document(self):
        serialized_organization = OrganizationSchema().serialize(organization_B)

        self.assertDictEqual(serialized_organization, {
            'organizations': {
                'organization_id': organization_B['organization_id'],
                'name': organization_B['name'],
                'links': {
                    'owner': organization_B['owner']['user_id']
                }
            },
            'linked': {
                'users': [organization_B['owner']]
            },
            'links': {
                'organizations.owner': {
                    'type': 'users'
                }
            }
        })

    def test_deeply_nested_documents(self):
        serialized = AdminSchema(admin_A).data

        self.assertDictEqual(serialized, {
            'admins': {
                'name': admin_A['name'],
                'admin_id': admin_A['admin_id'],
                'links': {
                    'orgs': [org['organization_id'] for org in admin_A['orgs']]
                }
            },
            'linked': {
                'organizations': [
                    {
                        'organization_id': org['organization_id'],
                        'name': org['name'],
                        'links': {
                            'owner': org['owner']['user_id']
                        }
                    } for org in admin_A['orgs']
                ],
                'users': [user_E, user_F]
            },
            'links': {
                'admins.orgs': {
                    'type': 'organizations'
                },
                'organizations.owner': {
                    'type': 'users'
                }
            }
        })

