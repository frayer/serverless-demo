import json
import os

import boto3
from boto3.dynamodb.conditions import Key

import db.ballot
import helper.response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


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


def update_ballot(event, context):
    """Updates just the open/close property of a Ballot"""
    return default(event, context)


def get_ballots(event, context):
    """Returns all Ballots"""
    return default(event, context)


def get_ballot(event, context):
    """Returns a specific Ballot"""
    return default(event, context)


def delete_ballot(event, context):
    """Deletes a Ballot"""
    ballot_id = event['pathParameters']['ballot_id']
    table.delete_item(
        Key={
            "pk": "BALLOTS",
            "sk": f"META#{ballot_id}"
        }
    )

    measures = table.query(
        KeyConditionExpression=Key('pk').eq(
            f"BALLOT#{ballot_id}") & Key('sk').begins_with(f"MEASURE#")
    )
    with table.batch_writer() as batch:
        print(f"Found {len(measures['Items'])} to delete")
        for measure in measures['Items']:
            print(f"Deleting {measure['pk']} : {measure['sk']}")
            batch.delete_item(
                Key={
                    "pk": measure['pk'],
                    "sk": measure['sk']
                }
            )

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "deleted": f"/ballot/{ballot_id}"
        })
    }

    return response


def record_vote(event, context):
    """Writes a new Vote to a Kinesis Stream"""
    return default(event, context)


def process_ballot_update(event, context):
    return default(event, context)


def process_vote(event, context):
    """Increments the Vote counter for a given Ballot Measure"""
    return default(event, context)
