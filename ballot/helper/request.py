from dataclasses import dataclass

import base64
import json
import typing


@dataclass
class Measure:
    vote_total: int = 0


@dataclass
class Ballot:
    measures: typing.Dict[str, Measure]

    def increment_vote_total(self, measure: str, amount: int):
        if measure in self.measures:
            self.measures[measure].vote_total += amount
        else:
            m = Measure()
            m.vote_total += amount
            self.measures[measure] = m


@dataclass
class BallotCounts:
    ballots: typing.Dict[str, Ballot]

    def increment_vote_total(self, ballot: str, measure: str, amount: int):
        if ballot in self.ballots:
            self.ballots[ballot].increment_vote_total(measure, amount)
        else:
            b = Ballot(measures={})
            b.increment_vote_total(measure, amount)
            self.ballots[ballot] = b


def kinesis_cloud_events(lambda_event):
    records = []
    for record in lambda_event['Records']:
        b64Data = record['kinesis']['data']
        data = base64.b64decode(b64Data).decode(('utf-8'))
        cloud_event = json.loads(data)
        records.append(cloud_event)

    return records


def ballot_counts(cloud_events) -> BallotCounts:
    bc = BallotCounts(ballots={})

    for event in cloud_events:
        [ballot, measure] = event['subject'].split('#')
        bc.increment_vote_total(ballot, measure, 1)

    return bc
