import unittest

from app.model import Downvote

class DownvoteModelTest(unittest.TestCase):

    def setUp(self):
        self.new_downvote=Downvote(downvote=1)

    def test_save_downvotes(self):
        self.new_downvote.save_downvotes()
        self.assertTrue(len(Downvote.query.all())>0)
