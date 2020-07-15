Feature: Index

    Scenario: Show index
        When I send a GET request to "/main-api/phoopy"
        Then the response code should be 200
        And the response should contain json:
            """
            {
                "data": {
                    "message": "Hello phoopy"
                }
            }
            """
