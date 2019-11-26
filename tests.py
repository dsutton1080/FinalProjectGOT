
import os
import unittest

from config import basedir
from init import app, db
from db_models import User, ForumQuestion, ForumPost, Message, UserPost, Follow

class Tests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unique_username(self):
        pass

    def test_unique_email(self):
        pass

    def test_password_verification(self):
        pass

    def test_forum_questions(self):
        pass

    def test_forum_question_only_by_highschool_student(self):
        pass

    def test_forum_posts(self):
        pass

    def test_user_posts(self):
        pass

    def test_outbound_messages(self):
        pass

    def test_inbound_messages(self):
        pass

    def test_empty_posts_not_allowed(self):
        pass

    def test_non_completed_user_not_in_db(self):
        pass

