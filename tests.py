import os

from config import basedir
from init import app, db
from db_models import User, UserPost, ForumQuestion, ForumPost, Follow
from funcs import *

OUT_FILE_PATH = 'tests_output.txt'
f = open(OUT_FILE_PATH, "a+")

class Test:
    """
    An encapsulation of a test function and its description
    """
    def __init__(self, description, proc):
        self.description = description
        self.run = proc

def write_output(msg):
    """
    Writes test output lines to the defined file
    :param msg: the string to write
    :return: void
    """
    f.write(msg + '\n')

def tester(test_obj):
    """
    Takes a test object, displays its description, and runs the test
    :param test_obj: a Test object
    :return: void
    """
    write_output("TEST DESCRIPTION: " + test_obj.description)
    passed, msgs = test_obj.run() # each test run method returns a boolean
    for msg in msgs:
        write_output(msg)
    if passed:
        write_output("----------\nResult: PASSED\n")
    else:
        write_output("----------\nResult: FAILED\n")

def test_add_user():
    """
    Tests the instantiation of a User object to the database
    :return: tuple (boolean, message list)
    """
    messages = []
    u1 = User(first_name='u1', last_name='u1', username='userexample', email='user623@example.com', password='password', school='KU', grade='col_jun', state='KS')
    try:
        messages.append("Adding a valid arbitrary user to empty database")
        db.session.add(u1)
        db.session.commit()
    except:
        messages.append("User could not be added to the database")
        db.session.rollback()
        return (False, messages)
    
    try:
        messages.append("Testing whether user query list is length 1")
        assert len(list(User.query.all())) == 1
    except:
        messages.append("Query list is not length 1")
        return (False, messages)

    [x] = list(User.query.all())
    try:
        messages.append("Testing whether added user is equivalent to created user")
        assert x == u1
    except:
        messages.append("Users are not equivalent")
        return (False, messages)
    return (True, messages)

def test_unique_username():
    """
    Tests whether only unique usernames are allowed
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Attempting to add two users to empty database with same username")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    u2 = User(first_name='u2', last_name='u2', username='user', email='user2@example.com', password='password', school='KU', grade='col_jun', state='KS')
    try:
        db.session.add(u2)
        db.session.commit()
    except:
        db.session.rollback()
    try:
        messages.append("Testing whether there is only one user in the database")
        assert len(list(User.query.all())) == 1
    except:
        messages.append("Not one user in database")
        return (False, messages)
    return (True, messages)

def test_unique_email():
    """
    Tests whether only unique email addresses are allowed
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Attempting to add 2 users with same email address to the empty database")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    u2 = User(first_name='u2', last_name='u2', username='user2', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
    try:
        db.session.add(u2)
        db.session.commit()
    except:
        db.session.rollback()
    try:
        messages.append("Testing whether the number of database users is 1")
        assert len(list(User.query.all())) == 1
    except:
        messages.append("Not one user in database")
        return (False, messages)
    return (True, messages)

def test_password_verification():
    """
    Tests the password verification method
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Adding a user with known password to the empty database")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    try:
        messages.append("Verfiying the known password")
        assert u1.test_password('password') == True
    except:
        messages.append("Verification failed")
        return (False, messages)
    try:
        messages.append("Testing verification of incorrect passwords")
        assert u1.test_password('diffpassword') == False
    except:
        messages.append("Verification failed")
        return (False, messages)
    return (True, messages)

def test_forum_questions():
    """
    Tests whether forum questions are properly added and referenced
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Adding user to empty database")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    messages.append("Adding 2 forum questions under the created user's username")
    forumq1 = ForumQuestion(author_username='user', content='This is a test post')
    forumq2 = ForumQuestion(author_username='user', content='This is another test post')
    db.session.add(forumq1)
    db.session.add(forumq2)
    db.session.commit()
    try:
        messages.append("Testing whether there are 2 forum questions referenced by user")
        assert len(list(u1.forum_questions)) == 2
    except:
        messages.append("There are not two referenced forum questions")
        return (False, messages)
    try:
        messages.append("Testing whether the referenced forum questions are equivalent")
        assert list(u1.forum_questions) == [forumq1, forumq2]
    except:
        messages.append("Different content")
        return (False, messages)
    return (True, messages)

def test_forum_posts():
    """
    Tests whether forum posts are properly added and referenced
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Adding user to empty database")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='Blue Valley West', grade='hs_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    messages.append("Adding a user-referenced forum question to database")
    forumq1 = ForumQuestion(author_username='user', content='This is a test post')
    db.session.add(forumq1)
    db.session.commit()
    messages.append("Adding 2 forum posts to database, referenced by both username and forum question id")
    forumpost1 = ForumPost(author_username='user', forum_question_id=forumq1.id, content='Test forum reply')
    forumpost2 = ForumPost(author_username='user', forum_question_id=forumq1.id, content='Test forum reply 2')
    db.session.add(forumpost1)
    db.session.add(forumpost2)
    db.session.commit()
    try:
        messages.append("Testing whether there are 2 forum posts referenced by username")
        assert len(list(u1.forum_posts)) == 2
    except:
        messages.append("There are not 2 referenced forum posts by username")
        return (False, messages)
    try:
        messages.append("Testing whether there are 2 forum posts referenced by forum question id")
        assert len(list(forumq1.forum_posts)) == 2
    except:
        messages.append("There are not 2 referenced forum posts by forum question id")
        return (False, messages)
    return (True, messages)


def test_user_posts():
    """
    Tests whether user post objects are properly added and referenced
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Adding user to empty database")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='Blue Valley West', grade='hs_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    messages.append("Adding 2 user posts under the created user's username")
    p1 = UserPost(author_username='user', content='Test post')
    p2 = UserPost(author_username='user', content='Test post 2')
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    try:
        messages.append("Testing whether there are 2 user posts referenced by user")
        assert len(list(u1.user_posts)) == 2
    except:
        messages.append("There are not 2 referenced user posts by username")
        return (False, messages)
    return (True, messages)

def test_empty_post_not_allowed():
    """
    Tests whether empty posts are denied from being added to the database
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Adding user to empty database")
    u1 = User(first_name='u1', last_name='u1', username='user', email='user@example.com', password='password', school='KU', grade='col_jun', state='KS')
    db.session.add(u1)
    db.session.commit()
    messages.append("Creating a post with empty content")
    p = UserPost(author_username='user', content=None)
    try:
        messages.append("Attempting to add empty post to the database")
        db.session.add(p)
        db.session.commit()
    except:
        messages.append("Empty post not allowed; exception thrown")
        db.session.rollback()
    try:
        messages.append("Ensuring that query for user posts returns an empty list")
        assert UserPost.query.all() == []
    except:
        messages.append("User posts not empty")
        return (False, messages)
    return (True, messages)

def test_non_completed_user_not_in_db():
    """
    Tests whether a User object with incomplete parameters is denied from database
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Creating user with incomplete parameters")
    u1 = User(first_name='u1', last_name='u1', username='user', password='password')
    try:
        messages.append("Attempting to add incomplete user to database")
        db.session.add(u1)
        db.session.commit()
    except:
        messages.append("Incomplete user not added to database; exception thrown")
        db.session.rollback()
    try:
        messages.append("Testing whether a query list for users returns empty")
        assert User.query.all() == []
    except:
        messages.append("User query nonempty")
        return (False, messages)
    return (True, messages)

def test_search_query():
    """
    Tests the user search query method to determine whether the change of filter criteria works properly
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Creating indexed table structure with many users")
    try:
        messages.append("Ensuring that searching with character 'J' (all users) yields 5 hits")
        assert len(get_search_results('all', 'J')) == 5
    except:
        messages.append("Query failed")
        return (False, messages)
    try:
        messages.append("Ensuring that searching character 'J' (mentees) yields 1 hit")
        assert len(get_search_results('mentee', 'J')) == 1
    except:
        messages.append("Query failed")
        return (False, messages)
    try:
        messages.append("Ensuring that searching character 'J' (mentorss) yields 4 hits")
        assert len(get_search_results('mentor', 'J')) == 4
    except:
        messages.append("Query failed")
        return (False, messages)
    return (True, messages)

def test_search_query2():
    """
    Tests whether a user can be found by entering either first or last name
    :return: tuple (boolean, message list)
    """
    messages = []
    messages.append("Creating indexed table structure with many users")
    try:
        messages.append("Ensuring that searching a first name yields a search match")
        assert len(get_search_results('all', 'John')) == 1
        messages.append("Ensuring that searching a last name yields a search match")
        assert len(get_search_results('all', 'Thomsen')) == 1
    except:
        messages.append("Query failed")
        return (False, messages)
    return (True, messages)

db_tests = [
    Test(
        description = "Testing whether a User can be added to the Database in a predictable manner",
        proc = test_add_user
    ),
    Test(
        description = "Testing whether the User Table requires unique usernames",
        proc = test_unique_username
    ),
    Test(
        description = "Testing whether the User Table requires unique email addresses",
        proc = test_unique_email
    ),
    Test(
        description = "Testing if passwords are verified correctly",
        proc = test_password_verification
    ),
    Test(
        description = "Testing if User has reference to the forum questions under their username",
        proc = test_forum_questions
    ),
    Test(
        description = "Testing if User has reference to the forum posts under their username",
        proc = test_forum_posts
    ),
    Test(
        description = "Testing if the User has reference to the user posts under their username",
        proc = test_user_posts
    ),
    Test(
        description = "Testing whether the a post with empty content is rejected by the database",
        proc = test_empty_post_not_allowed
    ),
    Test(
        description = "Testing whether a User without required parameters is rejected from the database",
        proc = test_non_completed_user_not_in_db
    )
]

func_tests = [
    Test(
        description = "Testing whether filter parameter changes search query correctly",
        proc = test_search_query
    ),
    Test(
        description = "Testing whether a user can be searched by both first and last name",
        proc = test_search_query2
    )
]

if __name__ == "__main__":   
    def test_db():
        """
        The procedure to run the database testing functions and write to file
        :return: void
        """
        i = 1
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        test_app = app.test_client()
        db.create_all()
        db.session.commit()
        for test in db_tests:
            clear_all_tables()
            write_output("Database Schema Test " + str(i) + "\n----------")
            tester(test)
            i += 1
    
    def test_funcs():
        """
        The procedure to run the search query function tests and write to file
        :return: void
        """
        i = 1
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        test_app = app.test_client()
        db.create_all()
        db.engine.execute("DROP TABLE IF EXISTS usersfts")
        db.engine.execute("CREATE VIRTUAL TABLE usersfts USING FTS5(username, first_name, last_name, email, school, state)")
        db.session.commit()
        from create_test_users import run
        run()
        for test in func_tests:
            write_output("Search Query Test " + str(i) + "\n----------")
            tester(test)
            i += 1

    test_db()
    test_funcs()


