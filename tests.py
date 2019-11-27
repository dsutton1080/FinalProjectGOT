
import os
import unittest

from config import basedir
from init import app, db
from db_models import User, ForumQuestion, ForumPost, Message, UserPost, Follow
from stateful_functions import get_messages

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

    def test_add_user(self):
        User.query.delete()
        db.session.commit()
        u1 = User(first_name='u1', last_name='u1', username='userexample', email='user623@example.com', password='password', school='KU', grade='col_jun', state='KS')
        try:
            db.session.add(u1)
            db.session.commit()
        except:
            db.session.rollback()
        
        print("\nTesting whether a User can be added to the Database")
        self.assertEqual(len(list(User.query.all())), 1)
        [x] = list(User.query.all())
        self.assertEqual(x, u1)

    def test_unique_username(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u1)
        db.session.commit()
        u2 = User(first_name='u2', last_name='u2', username='user', email='user2@example.com', password='password', school='KU', grade='col_jun', state='KS')
        try:
            db.session.add(u2)
            db.session.commit()
        except:
            db.session.rollback()

        print("\nTesting whether the User Table requires unique usernames")
        self.assertEqual(len(list(User.query.all())), 1)

    def test_unique_email(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u1)
        db.session.commit()
        u2 = User(first_name='u2', last_name='u2', username='user2', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        try:
            db.session.add(u2)
            db.session.commit()
        except:
            db.session.rollback()

        print("\nTesting whether the User Table requires unique email addresses:")
        self.assertEqual(len(list(User.query.all())), 1)

    def test_password_verification(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u1)
        db.session.commit()

        print("\nTesting if passwords are verified correctly:")
        self.assertTrue(u1.test_password('password'))
        self.assertFalse(u1.test_password('diffpassword'))

    def test_forum_questions(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u1)
        db.session.commit()
        forumq1 = ForumQuestion(author_username='user', content='This is a test post')
        forumq2 = ForumQuestion(author_username='user', content='This is another test post')
        db.session.add(forumq1)
        db.session.add(forumq2)
        db.session.commit()

        print("\nTesting if User has reference to the forum questions under their username:")
        self.assertEqual(len(list(u1.forum_questions)), 2)

    def test_forum_posts(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='Blue Valley West', grade='hs_jun', state='KS')
        db.session.add(u1)
        db.session.commit()
        forumq1 = ForumQuestion(author_username='user', content='This is a test post')
        db.session.add(forumq1)
        db.session.commit()
        forumpost1 = ForumPost(author_username='user', forum_question_id=forumq1.id, content='Test forum reply')
        forumpost2 = ForumPost(author_username='user', forum_question_id=forumq1.id, content='Test forum reply 2')
        db.session.add(forumpost1)
        db.session.add(forumpost2)
        db.session.commit()

        print("\nTesting if User has reference to the forum posts under their username:")
        self.assertEqual(len(list(u1.forum_posts)), 2)
        self.assertEqual(len(list(forumq1.forum_posts)), 2)

    def test_user_posts(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='Blue Valley West', grade='hs_jun', state='KS')
        db.session.add(u1)
        db.session.commit()
        p1 = UserPost(author_username='user', content='Test post')
        p2 = UserPost(author_username='user', content='Test post 2')
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        print("\nTesting if the User has reference to the user posts under their username:")
        self.assertEqual(len(list(u1.user_posts)), 2)

    def test_get_messages(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u1)
        u2 = User(first_name='u2', last_name='u2', username='user2', email='user2@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u2)
        db.session.commit()
        m1 = Message(sender_username='user', receiver_username='user2', content="Message 1")
        m2 = Message(sender_username='user', receiver_username='user2', content="Message 2")
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()
        msgs = get_messages('user', 'user2')

        print("\nTesting messages query with specific sender and receiver (in ID order):")
        self.assertEqual(msgs, [m2, m1])

    def test_empty_post_not_allowed(self):
        u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
        db.session.add(u1)
        db.session.commit()
        p = UserPost(author_username='user', content=None)
        try:
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()

        print("\nTesting whether the a post with empty content is rejected by the database:")
        self.assertEqual(UserPost.query.all(), [])


    def test_non_completed_user_not_in_db(self):
        u1 = User(first_name='u1', last_name='u1', username='user', password='password')
        try:
            db.session.add(u1)
            db.session.commit()
        except:
            db.session.rollback()

        print("\nTesting whether a User without required parameters is rejected from the database:")
        self.assertEqual(User.query.all(), [])

unittest.main(verbosity=2)