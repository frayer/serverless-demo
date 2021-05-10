import base64
import json
import os

import db.ballot
import db.stream
import helper.response

def default(event, context):
    print(event)

    eventBody = {}
    if 'body' in event:
        eventBody = json.loads(event['body'])
        print(json.dumps(eventBody))

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "eventBody": eventBody
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def create_ballot(event, context):
    """Stores a new Ballot"""
    ballot = json.loads(event['body'])
    ballot_id = db.ballot.create_ballot(ballot)
    return helper.response.create_ballot_success_response(ballot_id)


# Low priority for demo
def update_ballot(event, context):
    """Updates just the open/close property of a Ballot"""
    return default(event, context)


def get_ballots(event, context):
    """Returns all Ballots"""
    ballots = db.ballot.get_ballots()
    return helper.response.get_ballots_success_response(ballots)


def get_ballot(event, context):
    """Returns a specific Ballot"""
    ballot_id = event['pathParameters']['ballot_id']
    ballot = db.ballot.get_ballot(ballot_id)
    return helper.response.get_ballot_success_response(ballot)


def delete_ballot(event, context):
    """Deletes a Ballot"""
    ballot_id = event['pathParameters']['ballot_id']
    db.ballot.delete_ballot(ballot_id)
    return helper.response.delete_ballot_success_response(ballot_id)


def record_vote(event, context):
    """Writes a new Vote to a Kinesis Stream"""
    ballot_id = event['pathParameters']['ballot_id']
    measure_id = event['pathParameters']['measure_id']
    db.stream.record_vote_event(ballot_id, measure_id)
    return helper.response.default_code(200)


def process_ballot_update(event, context):
    """Processes an Ballot Update from the DynamoDB Stream"""
    return default(event, context)


def process_vote(event, context):
    """Increments the Vote counter for a given Ballot Measure Vote Event"""
    for record in event['Records']:
        b64Data = record['kinesis']['data']
        data = base64.b64decode(b64Data).decode(('utf-8'))
        cloud_event = json.loads(data)
        print(f"subject = {cloud_event['subject']}")
        [ballot_id, measure_id] = cloud_event['subject'].split('#')
        db.ballot.increment_vote_count(ballot_id, measure_id)

    return {
        "status": "OK"
    }
