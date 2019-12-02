from datetime import datetime
from init import app, db, login_manager

class User(db.Model):
    """
    This class corresponds to the database model for a User object.
    A high level interface that allows more efficient interactions with the relational database.
    """
    __tablename__ = 'Users'
    __searchable__ = ['username', 'first_name', 'last_name', 'email', 'school', 'state']

    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), index=True, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    school = db.Column(db.String(128))
    grade = db.Column(db.String(64))
    state = db.Column(db.String(64))
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    forum_questions = db.relationship("ForumQuestion", backref='author', lazy='dynamic')
    forum_posts = db.relationship("ForumPost", backref='author', lazy='dynamic')
    user_posts = db.relationship("UserPost", backref='author', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def test_password(self, password):
        if password == self.password:
            return True
        return False


class ForumQuestion(db.Model):
    """
    This class corresponds to the database model for a ForumQuestion object.
    A high level interface that allows more efficient interactions with the relational database.
    """
    __tablename__ = 'ForumQuestions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    forum_posts = db.relationship("ForumPost", backref='question', lazy='dynamic')

    def __repr__(self):
        return '<ForumQuestion {}>'.format(self.id)


class ForumPost(db.Model):
    """
    This class corresponds to the database model for a ForumPost object.
    A high level interface that allows more efficient interactions with the relational database.
    """
    __tablename__ = 'ForumPosts'
    id = db.Column(db.Integer, primary_key=True)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    forum_question_id = db.Column(db.Integer, db.ForeignKey('ForumQuestions.id'))
    content = db.Column(db.Text())
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<ForumPost {}>'.format(self.id)


class Message(db.Model):
    """
    This class corresponds to the database model for a Message object.
    A high level interface that allows more efficient interactions with the relational database.
    Due to time constraints, we were not able to implement messaging.
    """
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sender_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    receiver_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Message ID {} ({} -> {})>'.format(self.id, self.sender_username, self.receiver_username)


class UserPost(db.Model):
    """
    This class corresponds to the database model for a UserPost object.
    A high level interface that allows more efficient interactions with the relational database.
    """
    __tablename__ = 'UserPosts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<UserPost {} by {}>'.format(self.id, self.author_username)


class Follow(db.Model):
    """
    This class corresponds to the database model for a Follow object.
    A high level interface that allows more efficient interactions with the relational database.
    """
    __tablename__ = 'Follows'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    follower_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    following_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Follow ID {} ({} -> {})>'.format(self.id, self.follower_username, self.following_username)

@login_manager.user_loader
def load_user(user_id):
    """
    This function is invoked by Flask as part of its built-in user management features. This essentially loads a current
    user into the session.
    :param user_id: The username of the desired user to load into the session
    :return: User object or None
    """
    if user_id is not None:
        return User.query.get(user_id)
    return None

def create_db_models():
    """
    This function translates the defined database schemas into SQL commands.
    Creates the database tables.
    :return: void
    """
    db.create_all()
    db.engine.execute("DROP TABLE IF EXISTS usersfts")
    db.engine.execute("CREATE VIRTUAL TABLE usersfts USING FTS5(username, first_name, last_name, email, school, state)")
    db.session.commit()

create_db_models()