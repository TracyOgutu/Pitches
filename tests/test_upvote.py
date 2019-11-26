import unittest

from app.model import Upvote

class UpvoteModelTest(unittest.TestCase):

    def setUp(self):
        self.new_upvote=Upvote(upvote=1)

    def test_save_upvotes(self):
        self.new_upvote.save_upvotes()
        self.assertTrue(len(Upvote.query.all())>0)
