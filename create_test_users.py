from init import db
from db_models import *
from constants import GRADE_LEVELS, STATE_ABBREVS
from funcs import *

def spawn_mock_users():
    for i in range(1, 9):
        u = User(first_name='firstname' + str(i), 
                    last_name='lastname' + str(i),
                    username='user' + str(i), 
                    email='user' + str(i) + '@example.com', 
                    password='password', 
                    school='School' + str(i), 
                    grade=fst(GRADE_LEVELS[i-1]), 
                    state=STATE_ABBREVS[i-1])
        db.session.add(u)
    db.session.commit()

def spawn_mock_forum_questions():
    for i in range(1, 9):
        for j in range(1, 3):
            fq = ForumQuestion(author_username='user' + str(i),
                                content='How can I get into Harvard (User {}) (Question {})?'.format(i,j))
            db.session.add(fq)
    db.session.commit()

def spawn_mock_user_posts():
    for i in range(1, 9):
        for j in range(1,3):
            upost = UserPost(author_username='user' + str(i),
                             content = 'This is user post {} by user {}'.format(j,i))
            db.session.add(upost)
    db.session.commit()

def spawn_mock_forum_replies():
    for fq in get_forum_questions():
        for k in range(1, 9):
            fp = ForumPost(forum_question_id=fq.id,
                            author_username='user' + str(k),
                            content='Forum reply from user' + str(k))
            db.session.add(fp)
    db.session.commit()

def spawn_mock_follows():
    for i in range(1, 9):
        for j in range(1, 9):
            if i == j:
                pass
            else:
                follow = Follow(follower_username='user' + str(i),
                                following_username='user' + str(j))
                db.session.add(follow)
    db.session.commit()

def run():
    clear_all_tables()

    spawn_mock_users()
    spawn_mock_forum_questions()
    spawn_mock_forum_replies()
    spawn_mock_user_posts()
    spawn_mock_follows()


