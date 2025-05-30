Feature: API to manage advertisements
    As a user, I want register myself.


    Scenario: Create realestate types
        Given an authenticated session with email: test_user1@te.st and password: qwertyuiop1234567890-
        And a request url http://localhost:8000/api/v1/a/realestate/
        And a request json payload
            """
            {"type": "room"}
            """
        When the auth request sends POST
        Then response is OK
        Given a request json payload
            """
            {"type": "apartment"}
            """
        When the auth request sends POST
        Then response is OK
        Given a request json payload
            """
            {"type": "house"}
            """
        When the auth request sends POST
        Then response is OK
        Given a request json payload
            """
            {"type": "tent"}
            """
        When the auth request sends POST
        Then response is OK

    Scenario: Create advertisements for user
        Given an authenticated session with email: test_user1@te.st and password: qwertyuiop1234567890-
        And a request url http://localhost:8000/api/v1/a/ads/
        And a request json payload
            """
            {
                "real_estate_type": "room",
                "title": "title1",
                "description": "description1",
                "price": "100",
                "rooms_count": 1,
                "beds_count": 1,
                "location": {
                    "country": "Hungary",
                    "city": "Budapest",
                    "address": "Bartok Bela ut 31",
                    "index": "1111"
                },
                "is_active": true
            }
            """
        When the auth request sends POST
        Then response is OK
        Given a request json payload
            """
            {
                "real_estate_type": "apartment",
                "title": "title2",
                "description": "description2",
                "price": "200",
                "rooms_count": 2,
                "beds_count": 2,
                "location": {
                    "country": "Hungary",
                    "city": "Budapest",
                    "address": "Bartok Bela ut 32",
                    "index": "1112"
                },
                "is_active": true
            }
            """
        When the auth request sends POST
        Then response is OK
        Given a request json payload
            """
            {
                "real_estate_type": "house",
                "title": "title3",
                "description": "description3",
                "price": "300",
                "rooms_count": 3,
                "beds_count": 3,
                "location": {
                    "country": "Hungary",
                    "city": "Budapest",
                    "address": "Bartok Bela ut 33",
                    "index": "1113"
                },
                "is_active": true
            }
            """
        When the auth request sends POST
        Then response is OK
        Given a request json payload
            """
            {
                "real_estate_type": "tent",
                "title": "title4",
                "description": "description4",
                "price": "400",
                "rooms_count": 4,
                "beds_count": 4,
                "location": {
                    "country": "Hungary",
                    "city": "Budapest",
                    "address": "Bartok Bela ut 34",
                    "index": "1114"
                },
                "is_active": true
            }
            """
        When the auth request sends POST
        Then response is OK
