import os
import unittest

import db.ballot

class TestBallotIntegration(unittest.TestCase):
    def test_create_ballot(self):
        db.ballot.create_ballot({
            "name": "My Ballot 1",
            "measures": [
                "Measure A",
                "Measure B"
            ]
        })
        db.ballot.create_ballot({
            "name": "My Ballot 2",
            "measures": [
                "Measure C",
                "Measure D"
            ]
        })
        ballots = db.ballot.get_ballots()

        self.assertEqual(len(ballots), 2)

        self.assertEqual(ballots[0]["id"], "my-ballot-1")
        self.assertEqual(ballots[0]["name"], "My Ballot 1")
        self.assertEqual(ballots[0]["open"], False)

        self.assertEqual(ballots[1]["id"], "my-ballot-2")
        self.assertEqual(ballots[1]["name"], "My Ballot 2")
        self.assertEqual(ballots[1]["open"], False)

        db.ballot.delete_ballot('my-ballot-1')
        db.ballot.delete_ballot('my-ballot-2')


    def test_get_single_ballot(self):
        db.ballot.create_ballot({
            "name": "My Ballot 1",
            "measures": [
                "Measure A",
                "Measure B"
            ]
        })
        db.ballot.create_ballot({
            "name": "My Ballot 2",
            "measures": [
                "Measure C",
                "Measure D"
            ]
        })

        ballot = db.ballot.get_ballot("my-ballot-2")

        self.assertEqual(ballot["name"], "My Ballot 2")

        db.ballot.delete_ballot('my-ballot-1')
        db.ballot.delete_ballot('my-ballot-2')


    def test_get_single_ballot(self):
        db.ballot.create_ballot({
            "name": "My Ballot 1",
            "measures": [
                "Measure A",
                "Measure B"
            ]
        })
        db.ballot.create_ballot({
            "name": "My Ballot 2",
            "measures": [
                "Measure C",
                "Measure D"
            ]
        })

        ballot = db.ballot.get_ballot("my-ballot-2")

        self.assertEqual(ballot["name"], "My Ballot 2")

        db.ballot.delete_ballot('my-ballot-1')
        db.ballot.delete_ballot('my-ballot-2')


if __name__ == '__main__':
    unittest.main()
