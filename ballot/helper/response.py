import json


def create_ballot_success_response(ballot_id):
    location = f"/ballot/{ballot_id}"
    response = {
        "statusCode": 201,
        "headers": {
            "Location": location
        },
        "body": json.dumps({
            "location": location
        })
    }
    return response
