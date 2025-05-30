Feature: API to manage users
    As a user, I want register myself.

    Scenario Outline: Create user
        Given a request url http://localhost:8000/api/v1/u/auth-register/
            And a request json payload
                """
                {
                    "first_name": "alpha",
                    "last_name": "omega",
                    "username": "<username>",
                    "email": "<email>",
                    "password": "qwertyuiop1234567890-",
                    "re_password": "qwertyuiop1234567890-"
                }
                """
        When the request sends POST
        Then response is OK
        Then the response status is CREATED
            And the response json matches
                """
                {
                    "username": "<username>",
                    "email": "<email>"
                }
                """
            And the response json at username is equal to <username>
        Examples: users
            |username|email|
            |test_user1|test_user1@te.st|
            |test_user2|test_user2@te.st|
            |test_user3|test_user3@te.st|
