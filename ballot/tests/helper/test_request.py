import unittest

import helper.request

class TestRequestHelper(unittest.TestCase):
    def test_kinesis_cloud_events(self):
        lambda_event = {
            'Records': [
                {
                    'kinesis': {
                        'data': 'eyJtZXNzYWdlIjogImhlbGxvIHdvcmxkIn0=' # { "message": "hello world" }
                    }
                },
                {
                    'kinesis': {
                        'data': 'eyJtZXNzYWdlIjogImdvb2RuaWdodCB3b3JsZCJ9' # { "message": "goodnight world" }
                    }
                }
            ]
        }

        cloud_events = helper.request.kinesis_cloud_events(lambda_event)

        self.assertEqual(len(cloud_events), 2)
        self.assertEqual(cloud_events[0]['message'], 'hello world')
        self.assertEqual(cloud_events[1]['message'], 'goodnight world')


    def test_ballot_counts(self):
        cloud_events = [
            { 'subject': 'ballot-1#measure-1' },
            { 'subject': 'ballot-2#measure-1' },
            { 'subject': 'ballot-1#measure-2' },
            { 'subject': 'ballot-1#measure-2' },
            { 'subject': 'ballot-2#measure-1' },
            { 'subject': 'ballot-2#measure-2' },
            { 'subject': 'ballot-2#measure-3' },
        ]

        ballot_counts = helper.request.ballot_counts(cloud_events)

        self.assertEqual(len(ballot_counts.ballots), 2)
        self.assertEqual(len(ballot_counts.ballots['ballot-1'].measures), 2)
        self.assertEqual(len(ballot_counts.ballots['ballot-2'].measures), 3)

        self.assertEqual(ballot_counts.ballots['ballot-1'].measures['measure-1'].vote_total, 1)
        self.assertEqual(ballot_counts.ballots['ballot-1'].measures['measure-2'].vote_total, 2)

        self.assertEqual(ballot_counts.ballots['ballot-2'].measures['measure-1'].vote_total, 2)
        self.assertEqual(ballot_counts.ballots['ballot-2'].measures['measure-2'].vote_total, 1)
        self.assertEqual(ballot_counts.ballots['ballot-2'].measures['measure-3'].vote_total, 1)
