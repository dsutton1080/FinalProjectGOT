from init import app, db
from db_models import *

MENTOR_GRADES = ['col_fresh', 'col_soph', 'col_jun', 'col_sen']

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

def get_mentors():
    return list(filter(lambda u: is_mentor(u), list(User.query.all())))

def get_mentees():
    return list(filter(lambda u: not is_mentor(u), list(User.query.all())))

def sorted_reverse_id_order(l):
    return sorted(l, key=lambda p: p.id, reverse=True)

def get_following(user):
    follows = list(Follow.query.get(follower_username = user.username))
    following_usernames = list(map(lambda f: f.following_username, follows))
    following_users = map(lambda u: User.query.get(u).first(), following_usernames)
    return list(following_users)

def get_general_feed(user):
    following_unames = map(lambda u: u.username, get_following(user))
    return sorted_reverse_id_order(list(filter(lambda post: post.author_username in following_unames, list(UserPost.query.all()))))

def get_user_feed(user):
    return list(user.user_posts.all())

def get_forum_questions():
    return sorted_reverse_id_order(list(ForumQuestion.query.all()))

def get_forum_question_posts(forum_q):
    return sorted_reverse_id_order(list(ForumPost.query.get(forum_question_id=forum_q.id)))

