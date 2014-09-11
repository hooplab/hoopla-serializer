from datetime import datetime

reservation = {
    "tickets": [
        {
            "uuid": "389aa88d-728b-a647-43d4-026853b6e60c",
            "fee": 2500,
            "event_id": 1615163368,
            "price": 25000,
            "ticket_type_id": 2217311692,
            "txid": 252797,
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

purchase = {
    "purchase_id": 3623100207,
    "ref_code": "FS78ZB3",
    "fee": 1500,
    "user_id": 3314774599,
    "finalized": "2014-07-22T12:52:47Z",
    "tickets": [
        {
            "purchase_id": 3623100207,
            "ref_code": "H3UK6K3D3VM",
            "fee": 1500,
            "invoice_fee": None,
            "event_id": 2072474058,
            "price": 1000,
            "ticket_type_id": 2220190969,
            "event": {
                "end": "2014-07-22T14:52:47Z",
                "name": "event0ba7774a",
                "created": "2014-07-22T12:52:47Z",
                "event_id": 2072474058,
                "invoice_allowed": False,
                "event_type": {
                    "organization_id": 2081098224,
                    "last_modified": "2014-07-22T12:52:47Z",
                    "event_type_id": 1732449176,
                    "organization": {
                        "country_code": "NO",
                        "created": "2014-07-22T12:52:47Z",
                        "txid": 214189,
                        "organization_id": 2081098224,
                        "is_vetted": False,
                        "identifier": "org0ba7774a",
                        "data": None,
                        "zip_code": "7000"
                    },
                    "identifier": "event_type0ba7774a",
                    "data": None
                },
                "max_capacity": 1000,
                "is_published": False,
                "event_type_id": 1732449176,
                "is_cancelled": False,
                "identifier": "event0ba7774a",
                "data": {},
                "start": "2014-07-22T13:52:47Z",
                "description": None
            },
            "ticket_type": {
                "vat_factor": 0,
                "name": "ticket_type0ba7774a",
                "price": 1000,
                "ticket_type_id": 2220190969,
                "event_type_id": 1732449176,
                "identifier": "ticket_type0ba7774a",
                "data": {},
                "is_private": False,
                "description": None
            },
            "txid": 214191,
            "price_group": None,
            "fee_vat": 0,
            "ticket_id": "23471725260406897",
            "invoice_fee_vat": None,
            "purchase_ref": "FS78ZB3",
            "owner": {
                "phone_number": None,
                "first_name": None,
                "last_name": None,
                "user_id": 3314774599,
                "created": "2014-07-22T12:52:46Z",
                "email_verified": None,
                "txid": 214187,
                "is_admin": False,
                "phone_verified": None,
                "data": None,
                "email": "system_test+0ba7774a@hoopla.no"
            },
            "credits": [],
            "data": None,
            "is_revoked": False,
            "vat": 0
        }
    ],
    "created": "2014-07-22T12:52:47Z",
    "order_ref": "bd4a50d6c056b2e37a2467069a16b07d789903536bb08eefec52873222924907",
    "amount": 1000,
    "fee_vat": 0,
    #"user": {
    #    "phone_number": None,
    #    "first_name": None,
    #    "last_name": None,
    #    "user_id": 321,
    #    "created": "2014-07-22T12:52:46Z",
    #    "email_verified": None,
    #    "txid": 214187,
    #    "is_admin": False,
    #    "phone_verified": None,
    #    "data": None,
    #    "email": "system_test+0ba7774a@hoopla.no"
    #},
    "payex_data": None,
    "data": {
        "tickets": [
            {
                "price_group": None,
                "ticket": "ticket_type0ba7774a",
                "data": None,
                "event": "event0ba7774a"
            }
        ],
        "cancel_existing_purchase": False,
        "checkout": {
            "user_id": None,
            "invoice_data": None,
            "reservation_id": None,
            "is_invoice": False,
            "checkout_method": "pos",
            "data": None,
            "email": None,
            "return_url": "http://localhost/return_url"
        }
    },
    "vat": 0
}


event_type = {
    "organization_id": 1141995721,
    "last_modified": "2014-08-25T15:35:36Z",
    "event_type_id": 1432834051,
    "ticket_types": [
        {
            "vat_factor": 2500,
            "name": "Studentdsadasda",
            "price": 20000,
            "ticket_type_id": 2574215054,
            "event_type_id": 1432834051,
            "identifier": "tt-student",
            "data": {
                "is_hidden": False
            },
            "is_private": False,
            "description": ""
        },
        {
            "vat_factor": 2500,
            "name": "Ordin\u00e6rdsadasdas",
            "price": 25000,
            "ticket_type_id": 2271349306,
            "event_type_id": 1432834051,
            "identifier": "tt-ordinaer",
            "data": {
                "is_hidden": False
            },
            "is_private": False,
            "description": ""
        },
        {
            "vat_factor": 0,
            "name": "gratisdsadasda",
            "price": 0,
            "ticket_type_id": 3217709470,
            "event_type_id": 1432834051,
            "identifier": "tt-gratis",
            "data": {
                "is_hidden": False
            },
            "is_private": False,
            "description": ""
        }
    ],
    "organization": {
        "organization_id": 1141995721
    },
    "identifier": None,
    "data": None,
    "events": [
        {
            "end": "2015-12-06T03:30:00Z",
            "name": "heiheij9dosajidosa",
            "created": "2014-08-25T15:35:36Z",
            "event_id": 441783532,
            "invoice_allowed": False,
            "event_type": {
                "organization_id": 1141995721,
                "last_modified": "2014-08-25T15:35:36Z",
                "event_type_id": 1432834051,
                "ticket_types": [
                    {
                        "vat_factor": 2500,
                        "name": "Studentdsadasda",
                        "price": 20000,
                        "ticket_type_id": 2574215054,
                        "event_type_id": 1432834051,
                        "identifier": "tt-student",
                        "data": {
                            "is_hidden": False
                        },
                        "is_private": False,
                        "description": ""
                    },
                    {
                        "vat_factor": 2500,
                        "name": "Ordin\u00e6rdsadasdas",
                        "price": 25000,
                        "ticket_type_id": 2271349306,
                        "event_type_id": 1432834051,
                        "identifier": "tt-ordinaer",
                        "data": {
                            "is_hidden": False
                        },
                        "is_private": False,
                        "description": ""
                    },
                    {
                        "vat_factor": 0,
                        "name": "gratisdsadasda",
                        "price": 0,
                        "ticket_type_id": 3217709470,
                        "event_type_id": 1432834051,
                        "identifier": "tt-gratis",
                        "data": {
                            "is_hidden": False
                        },
                        "is_private": False,
                        "description": ""
                    }
                ],
                "organization": {
                    "country_code": "NO",
                    "created": "2014-07-01T12:36:24Z",
                    "txid": 167058,
                    "organization_id": 1141995721,
                    "is_vetted": False,
                    "identifier": "brukbar",
                    "data": {
                        "name": "Brukbar"
                    },
                    "zip_code": "7012"
                },
                "identifier": None,
                "data": None,
                "events": [
                    {
                        "end": "2015-12-06T03:30:00Z",
                        "name": "heiheij9dosajidosa",
                        "created": "2014-08-25T15:35:36Z",
                        "event_id": 441783532,
                        "invoice_allowed": False,
                        "max_capacity": 1000,
                        "is_published": False,
                        "event_type_id": 1432834051,
                        "is_cancelled": False,
                        "identifier": None,
                        "data": {
                            "max_tickets": 10,
                            "location": {
                                "lat": 0,
                                "lng": 0,
                                "name": "pelle krog"
                            }
                        },
                        "start": "2015-12-05T20:30:00Z",
                        "description": "udsaioduasuioduoasda"
                    }
                ]
            },
            "max_capacity": 1000,
            "is_published": False,
            "event_type_id": 1432834051,
            "is_cancelled": False,
            "identifier": None,
            "data": {
                "max_tickets": 10,
                "location": {
                    "lat": 0,
                    "lng": 0,
                    "name": "pelle krog"
                }
            },
            "start": "2015-12-05T20:30:00Z",
            "description": "udsaioduasuioduoasda"
        }
    ]
}