import os
import unittest

import db.stream

class TestStreamIntegration(unittest.TestCase):
    def test_record_vote_event(self):
        db.stream.record_vote_event('ballot-1', 'starship-enterprise')


if __name__ == '__main__':
    unittest.main()
