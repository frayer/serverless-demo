import json
import os
import uuid

import boto3

kinesis = boto3.client('kinesis')


def record_vote_event(ballot_id, measure_id):
    kinesis.put_record(
        StreamName=os.environ['KINESIS_STREAM'],
        Data=json.dumps({
            "specversion": "1.0",
            "type": "org.frayer.demo.ballot.vote.cast",
            "subject": f"{ballot_id}#{measure_id}",
            "id": str(uuid.uuid4()),
            "datacontenttype": "application/json",
            "data": "{}"
        }),
        PartitionKey=f"{ballot_id}#{measure_id}"
    )
