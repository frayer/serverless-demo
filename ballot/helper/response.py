import json


def default_code(http_status_code):
    return {
        "statusCode": http_status_code,
    }

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


def get_ballots_success_response(ballots):
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "ballots": ballots
        })
    }
    return response


def get_ballot_success_response(ballot):
    response = {
        "statusCode": 200,
        "body": json.dumps(ballot)
    }
    return response


def delete_ballot_success_response(ballot_id):
    location = f"/ballot/{ballot_id}"
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "deleted": location
        })
    }
    return response
