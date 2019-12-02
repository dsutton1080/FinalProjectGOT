from datetime import datetime
from constants import GRADE_LEVELS, STATE_ABBREVS, STATE_NAMES
from init import app, db
from db_models import User, UserPost, ForumQuestion, ForumPost, Message, Follow
from db_setup import conn

MENTOR_GRADES = ['col_fresh', 'col_soph', 'col_jun', 'col_sen']

def add_user(u):
    """
    Add a user and its search index equivalent to the database.
    :param u: User object
    :return: void
    """
    db.session.add(u)
    db.session.commit()
    db.engine.execute("INSERT INTO usersfts(username, first_name, last_name, email, school, state) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(u.username, u.first_name, u.last_name, str(u.email), u.school, u.state))

def delete_user(u):
    """
    Deletes a user and its search index equivalent from the database.
    :param u: User object
    :return: void
    """
    db.engine.execute("DELETE FROM usersfts WHERE username='{}'".format(u.username))
    db.session.delete(u)
    db.session.commit()

def grade_level_string(grLvlCode):
    """
    Converts grade level encoding into a string.
    :param grLvlCode: Code for the grade level.
    :return: the converted string
    """
    for lvl in GRADE_LEVELS:
        code, string = lvl
        if grLvlCode == code:
            return string
    return None

def state_abbrev_to_name(abbrev):
    """
    Converts a state abbreviation string into the state name
    :param abbrev: state abbreviation
    :return: state name
    """
    return STATE_NAMES[STATE_ABBREVS.index(abbrev)]

def fst(pair):
    """
    Returns the first element of a 2-tuple
    :param pair: a 2-tuple object
    :return: first element of the tuple
    """
    x, y = pair
    return x

def clear_all_tables():
    """
    Deletes all rows from all current database tables
    :return: void
    """
    Follow.query.delete()
    UserPost.query.delete()
    ForumPost.query.delete()
    ForumQuestion.query.delete()
    Message.query.delete()
    User.query.delete()
    db.session.commit()

def is_mentor(u):
    """
    Determines whether a User object is a mentor (based on grade)
    :param u: User object
    :return: boolean
    """
    return u.grade in MENTOR_GRADES

def is_mentee(u):
    """
    Determines whether a User object is a mentee (based on grade)
    :param u: User object
    :return: boolean
    """
    return u.grade not in MENTOR_GRADES

def get_mentors():
    """
    Gets all the users that are mentors (in college)
    :return: list of User objects
    """
    return list(filter(lambda u: is_mentor(u), list(User.query.all())))

def get_mentees():
    """
    Gets all the users that are mentees (in high school)
    :return: list of User objects
    """
    return list(filter(lambda u: not is_mentor(u), list(User.query.all())))

def sorted_reverse_id_order(l):
    """
    Sorts a list of objects with 'id' attributes in reverse order
    :param l: list of identified objects
    :return: sorted list
    """
    return sorted(l, key=lambda p: p.id, reverse=True)

def get_following(user):
    """
    Get all users who are a particular user is following
    :param user: a User object
    :return: a list of User objects
    """
    follows = list(Follow.query.filter_by(follower_username = user.username))
    following_usernames = list(map(lambda f: f.following_username, follows))
    following_users = map(lambda u: User.query.get(u), following_usernames)
    return list(following_users)

def get_general_feed(user):
    """
    Gets the feed of the posts of all users whom the particular user is following in reverse chronological order
    :param user: a User object
    :return: a list of UserPost objects
    """
    following_unames = list(map(lambda u: u.username, get_following(user)))
    return sorted_reverse_id_order(list(filter(lambda post: (post.author_username in following_unames) or (post.author_username == user.username), list(UserPost.query.all()))))

def get_user_feed(user):
    """
    Gets all posts by a particular user
    :param user: a User object
    :return: a list of UserPost objects
    """
    return list(user.user_posts.all())

def get_forum_questions():
    """
    Gets all forum questions posted on the website by all users
    :return: A list of ForumQuestion objects
    """
    return sorted_reverse_id_order(list(ForumQuestion.query.all()))

def get_forum_question_posts(forum_q):
    """
    Gets all thread responses to a forum question
    :param forum_q: A ForumQuestion object
    :return: A list of ForumPost objects
    """
    return sorted_reverse_id_order(list(forum_q.forum_posts))

def get_forum_question_ids():
    """
    Gets the ids of all ForumQuestion objects
    :return: list of integers (ids)
    """
    return list(map(lambda q: q.id, get_forum_questions()))

def get_user_by_username(uname):
    """
    Gets a User object from its username
    :param uname: username (string)
    :return: a User object
    """
    return User.query.get(uname)

def date_to_string(dt_obj):
    """
    Gets a displayable string from a DateTime object
    :param dt_obj: a DateTime object
    :return: a string that represents that date/time
    """
    return dt_obj.strftime("%d-%b-%Y %I:%M %p")

def get_all_users():
    """
    Gets all users in the database
    :return: a list of User objects
    """
    return list(User.query.all())

def get_all_usernames():
    """
    Gets all usernames from users in the database
    :return: a list of strings (usernames)
    """
    return list(map(lambda u: u.username, get_all_users()))

def valid_post_params(uname, content):
    """
    Verifies author_username and content data
    :param uname: username (string)
    :param content: text
    :return: boolean
    """
    return (uname in get_all_usernames()) and (content is not None) and (content != "")

def add_forum_question(uname, content):
    """
    Adds a ForumQuesion object to the database after verification
    :param uname: username
    :param content: content
    :return: a ForumQuestion object (success) or None (failure)
    """
    if valid_post_params(uname, content):
        fq = ForumQuestion(author_username=uname, content=content)
        db.session.add(fq)
        db.session.commit()
        return fq
    return None

def add_forum_post(question_id, uname, content):
    """
    Adds a ForumPost object to the database after verification
    :param question_id: the id of the referenced ForumQuestion object
    :param uname: the username of the author
    :param content: the content of the post
    :return: a ForumPost object or None
    """
    if valid_post_params(uname, content) and (question_id in get_forum_question_ids()):
        fp = ForumPost(forum_question_id=question_id, author_username=uname, content=content)
        db.session.add(fp)
        db.session.commit()
        return fp
    return None

def add_user_post(uname, content):
    """
    Adds a UserPost object to the database after verification
    :param uname: the username of the author
    :param content: the content of the post
    :return: a UserPost object or None
    """
    if valid_post_params(uname, content):
        p = UserPost(author_username=uname, content=content)
        db.session.add(p)
        db.session.commit()
        return p
    return None

def id_to_forum_question(question_id):
    """
    Given the id of the parent forum question, returns a ForumQuestion object
    :param question_id: The id of the forum question (int)
    :return: a ForumQuestion object
    """
    return ForumQuestion.query.get(question_id)

def get_search_results(filt, text):
    """
    Given a filter parameter and search text, returns a list of possible matches for the user search
    :param filt: either 'all', 'mentee', or 'mentor'
    :param text: the search text
    :return: a list of User objects matching (close to) the search
    """
    cursor = []
    try:
        cursor = db.engine.execute("SELECT * FROM usersfts WHERE usersfts MATCH '{}*' ORDER BY rank".format(text))
    except:
        return []
    usernames = list(map(lambda obj: obj[0], list(cursor)))
    users = list(map(get_user_by_username, usernames))

    if filt == 'mentor':
        return list(filter(is_mentor, users))
    elif filt == 'mentee':
        return list(filter(is_mentee, users))
    else:
        return users
    

def is_following(follower, following):
    """
    Given 2 users, determines if the first is following the second
    :param follower: a User object
    :param following: a User object
    :return: a boolean
    """
    return len(list(Follow.query.filter_by(follower_username = follower.username).filter_by(following_username = following.username))) == 1

def is_valid_user(u):
    """
    Given a user object, determines whether it is in the database
    :param u: a User object
    :return: a boolean
    """
    return False if (User.query.get(u.username) is None) else True