from datetime import datetime
from constants import GRADE_LEVELS, STATE_ABBREVS, STATE_NAMES
from init import app, db
from db_models import User, UserPost, ForumQuestion, ForumPost, Message, Follow

MENTOR_GRADES = ['col_fresh', 'col_soph', 'col_jun', 'col_sen']

def grade_level_string(grLvlCode):
    for lvl in GRADE_LEVELS:
        code, string = lvl
        if grLvlCode == code:
            return string
    return None

def state_abbrev_to_name(abbrev):
    return STATE_NAMES[STATE_ABBREVS.index(abbrev)]

def fst(pair):
    x, y = pair
    return x

def clear_all_tables():
    Follow.query.delete()
    UserPost.query.delete()
    ForumPost.query.delete()
    ForumQuestion.query.delete()
    Message.query.delete()
    User.query.delete()
    db.session.commit()

def is_mentor(u):
    return u.grade in MENTOR_GRADES

def is_mentee(u):
    return u.grade not in MENTOR_GRADES

def get_mentors():
    return list(filter(lambda u: is_mentor(u), list(User.query.all())))

def get_mentees():
    return list(filter(lambda u: not is_mentor(u), list(User.query.all())))

def sorted_reverse_id_order(l):
    return sorted(l, key=lambda p: p.id, reverse=True)

def get_following(user):
    follows = list(Follow.query.filter_by(follower_username = user.username))
    following_usernames = list(map(lambda f: f.following_username, follows))
    following_users = map(lambda u: User.query.get(u), following_usernames)
    return list(following_users)

def get_general_feed(user):
    following_unames = list(map(lambda u: u.username, get_following(user)))
    return sorted_reverse_id_order(list(filter(lambda post: (post.author_username in following_unames) or (post.author_username == user.username), list(UserPost.query.all()))))

def get_user_feed(user):
    return list(user.user_posts.all())

def get_forum_questions():
    return sorted_reverse_id_order(list(ForumQuestion.query.all()))

def get_forum_question_posts(forum_q):
    return sorted_reverse_id_order(list(forum_q.forum_posts))

def get_forum_question_ids():
    return list(map(lambda q: q.id, get_forum_questions()))

def get_user_by_username(uname):
    return User.query.get(uname)

def date_to_string(dt_obj):
    return dt_obj.strftime("%d-%b-%Y %I:%M %p")

def get_all_users():
    return list(User.query.all())

def get_all_usernames():
    return list(map(lambda u: u.username, get_all_users()))

def valid_post_params(uname, content):
    return (uname in get_all_usernames()) and (content is not None) and (content != "")

def add_forum_question(uname, content):
    if valid_post_params(uname, content):
        fq = ForumQuestion(author_username=uname, content=content)
        db.session.add(fq)
        db.session.commit()
        return fq
    else:
        return None

def add_forum_post(question_id, uname, content):
    if valid_post_params(uname, content) and (question_id in get_forum_question_ids()):
        fp = ForumPost(forum_question_id=question_id, author_username=uname, content=content)
        db.session.add(fp)
        db.session.commit()
        return fp
    else:
        return None

def id_to_forum_question(question_id):
    return ForumQuestion.query.get(question_id)

