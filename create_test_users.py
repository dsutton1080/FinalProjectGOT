from init import db
from db_models import *
from constants import GRADE_LEVELS, STATE_ABBREVS
from funcs import *

FIRSTS = ['Jim', 'Jack', 'Ashley', 'Tom', 'Greg', 'Jenna', 'Margaret', 'Courtney', 'Tim', 'Bill', 'Joe', 'Lexie']
LASTS = ['Thomsen', 'Black', 'Johnson', 'Davidson', 'Hernandez', 'Smith', 'Brown', 'Lee', 'Byrd', 'Danielson', 'Christopher', 'Lang']
USERNAMES = list(map(lambda i: FIRSTS[i] + LASTS[i], range(0,12)))

def even(n):
    return (n % 2) == 0

def spawn_mock_users():
    """
    Creates a set of 12 users for the purposes of testing the application.
    """
    for i in range(1, 13):
        u = User(first_name=FIRSTS[i-1], 
                    last_name=LASTS[i-1],
                    username=FIRSTS[i-1] + LASTS[i-1], 
                    email=FIRSTS[i-1] + LASTS[i-1] + '@example.com', 
                    password='password', 
                    school='School' + str(i), 
                    grade=fst(GRADE_LEVELS[7 - (i % 8)]), 
                    state=STATE_ABBREVS[i-1])
        add_user(u)

def spawn_mock_forum_questions():
    """
    Creates 3 forum question posts for each user for purposes of testing.
    """
    for i in range(0, 12):
        for j in range(1, 3):
            fq = ForumQuestion(author_username=USERNAMES[i],
                                content='How can I get into Harvard (User {}) (Question {})?'.format(i,j))
            db.session.add(fq)
    db.session.commit()

def spawn_mock_user_posts():
    """
    Creates 2 user posts per person for the purposes of testing.
    """
    for i in range(0, 12):
        for j in range(1,3):
            upost = UserPost(author_username=USERNAMES[i],
                             content = 'This is user post {} by user {}'.format(j,i))
            db.session.add(upost)
    db.session.commit()

def spawn_mock_forum_replies():
    """
    Creates a forum post reply for each forum question (each user)
    """
    for fq in get_forum_questions():
        for k in range(0, 12):
            fp = ForumPost(forum_question_id=fq.id,
                            author_username=USERNAMES[k],
                            content='Forum reply from user' + str(k))
            db.session.add(fp)
    db.session.commit()

def spawn_mock_follows():
    """
    Creates test relationships between users based on their stored index
    """
    for i in range(0, 12):
        for j in range(0, 12):
            if even(i) and even(j):
                pass
            else:
                follow = Follow(follower_username=USERNAMES[i],
                                following_username=USERNAMES[j])
                db.session.add(follow)
    db.session.commit()

def run():
    """
    Sets up the entire database test environment and fills with the test data
    """
    clear_all_tables()

    spawn_mock_users()
    spawn_mock_forum_questions()
    spawn_mock_forum_replies()
    spawn_mock_user_posts()
    spawn_mock_follows()


