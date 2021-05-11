import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def create_ballot(ballot):
    ballot_id = ballot['name'].lower().replace(' ', '-')

    table.put_item(Item={
        'pk': 'BALLOTS',
        'sk': f"META#{ballot_id}",
        'name': ballot['name'],
        'open': False
    })

    for measure in ballot['measures']:
        measure_slug = measure.lower().replace(' ', '-')
        table.put_item(Item={
            'pk': f"BALLOT#{ballot_id}",
            'sk': f"MEASURE#{measure_slug}",
            'name': measure,
            'votes': 0
        })

    return ballot_id


def get_ballots():
    def to_ballot(item):
        return {
            'id': item['sk'].split('META#')[1],
            'name': item['name'],
            'open': item['open']
        }

    # TODO: This doesn't page over all possible results yet
    ballots = table.query(
        KeyConditionExpression=Key('pk').eq(
            f"BALLOTS") & Key('sk').begins_with('META#')
    )

    return [to_ballot(item) for item in ballots['Items']]


def get_ballot(ballot_id):
    def to_measure(measure):
        return {
            'id': measure['sk'].split('MEASURE#')[1],
            'name': measure['name'],
            'votes': measure['votes']
        }

    ballot = table.get_item(
        Key={
            'pk': 'BALLOTS',
            'sk': f"META#{ballot_id}"
        }
    )

    # TODO: This doesn't page over all possible results yet
    measures = table.query(
        KeyConditionExpression=Key('pk').eq(
            f"BALLOT#{ballot_id}") & Key('sk').begins_with('MEASURE#')
    )


    ballot_item = ballot['Item']
    return {
        'id': ballot_item['sk'].split('META#')[1],
        'name': ballot_item['name'],
        'open': ballot_item['open'],
        'measures': [to_measure(measure) for measure in measures['Items']]
    }


def delete_ballot(ballot_id):
    table.delete_item(
        Key={
            'pk': 'BALLOTS',
            'sk': f"META#{ballot_id}"
        }
    )

    measures = table.query(
        KeyConditionExpression=Key('pk').eq(
            f"BALLOT#{ballot_id}") & Key('sk').begins_with('MEASURE#')
    )
    with table.batch_writer() as batch:
        for measure in measures['Items']:
            batch.delete_item(
                Key={
                    'pk': measure['pk'],
                    'sk': measure['sk']
                }
            )

    return ballot_id


def increment_vote_count(ballot_id, measure_id, amount):
    table.update_item(
        Key={
            'pk': f"BALLOT#{ballot_id}",
            'sk': f"MEASURE#{measure_id}"
        },
        UpdateExpression='SET votes = votes + :incr',
        ExpressionAttributeValues={
            ':incr': amount
        }
    )
