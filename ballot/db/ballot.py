import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def create_ballot(ballot):
    ballot_id = ballot['name'].lower().replace(' ', '-')

    table.put_item(Item={
        "pk": "BALLOTS",
        "sk": f"META#{ballot_id}",
        "name": ballot['name'],
        "open": False
    })

    for measure in ballot['measures']:
        measure_slug = measure.lower().replace(' ', '-')
        table.put_item(Item={
            "pk": f"BALLOT#{ballot_id}",
            "sk": f"MEASURE#{measure_slug}",
            "name": measure,
            "votes": 0
        })

    return ballot_id


def delete_ballot(name):
    None
