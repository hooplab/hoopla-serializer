import unittest

from serializer.schema import Linked, Schema


class UserBestFriendSchema(Schema):
    class Meta:
        primary_key = 'user_id'
        type = 'users'

        additional = ('user_id', 'name')

    best_friend = Linked("self")


class CyclicSchemaTest(unittest.TestCase):
    def test_cyclic_self_reference(self):
        forever_alone = {
            "user_id": 1,
            "name": "BibleThump",
        }
        forever_alone['best_friend'] = forever_alone

        """
            user <-> user
        """

        serialized_user = UserBestFriendSchema().dump(forever_alone).data

        self.assertDictEqual(serialized_user, {
            'users': {
                'links': {
                    'best_friend': forever_alone['user_id']
                },
                'user_id': forever_alone['user_id'],
                'name': forever_alone['name']
            },
            'links': {
                'users.best_friend': {
                    'type': 'users'
                }
            },
            'linked': {}
        })

    def test_cyclic_reference(self):
        user_1 = {
            "user_id": 1,
            "name": "Alice",
        }

        user_2 = {
            "user_id": 2,
            "name": "Bob",
        }

        user_3 = {
            "user_id": 3,
            "name": "Carol"
        }

        user_1['best_friend'] = user_2
        user_2['best_friend'] = user_3
        user_3['best_friend'] = user_1

        """
            user_1 -> user_2 -> user_3 -> user_1
        """

        serialized_user = UserBestFriendSchema().dump(user_1).data

        self.assertDictEqual(serialized_user, {
            'users': {
                'name': user_1['name'],
                'user_id': user_1['user_id'],
                'links': {
                    'best_friend': user_2['user_id']
                }
            },
            'linked': {
                'users': [
                    {
                        'name': user_3['name'],
                        'user_id': user_3['user_id'],
                        'links': {
                            'best_friend': user_1['user_id']
                        }
                    },
                    {
                        'name': user_2['name'],
                        'user_id': user_2['user_id'],
                        'links': {
                            'best_friend': user_3['user_id']
                        }
                    },

                ]
            },
            'links': {
                'users.best_friend': {
                    'type': 'users'
                }
            }
        })

    def test_deep_nested_cyclic_reference(self):
        class ParentSchema(Schema):
            class Meta:
                primary_key = 'parent_id'
                type = 'parents'

                additional = ('parent_id', 'name')

            children = Linked('ChildSchema', many=True)
            favorite_child = Linked('ChildSchema')

        class ChildSchema(Schema):
            class Meta:
                primary_key = 'child_id'
                type = 'children'

                additional = ('child_id', 'name')

            parent = Linked(ParentSchema)

        parent = {
            "parent_id": 1,
            "name": "Parent"
        }

        child_1 = {
            "child_id": 1,
            "name": "Kari",
            "parent": parent
        }

        child_2 = {
            "child_id": 2,
            "name": "Pelle",
            "parent": parent
        }

        parent['children'] = [child_1, child_2]
        parent['favorite_child'] = child_1

        serialized_parent = ParentSchema(parent).data

        self.assertDictEqual(serialized_parent, {
            'parents': {
                'parent_id': 1,
                'links': {
                    'favorite_child': 1,
                    'children': [1, 2]
                },
                'name': u'Parent'
            },
            'linked': {
                'children': [
                    {
                        'child_id': 1,
                        'links': {
                            'parent': 1
                        },
                        'name': u'Kari'
                    },
                    {
                        'child_id': 2,
                        'links': {
                            'parent': 1
                        },
                        'name': u'Pelle'
                    }
                ]
            },
            'links': {
                'parents.favorite_child': {
                    'type': 'children'
                },
                'children.parent': {
                    'type': 'parents'
                },
                'parents.children': {
                    'type': 'children'
                }
            }
        })
