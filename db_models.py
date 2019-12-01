from datetime import datetime
from init import db, login_manager


class User(db.Model):
    __tablename__ = 'Users'
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
    __tablename__ = 'ForumQuestions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    forum_posts = db.relationship("ForumPost", backref='question', lazy='dynamic')

    def __repr__(self):
        return '<ForumQuestion {}>'.format(self.id)


class ForumPost(db.Model):
    __tablename__ = 'ForumPosts'
    id = db.Column(db.Integer, primary_key=True)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    forum_question_id = db.Column(db.Integer, db.ForeignKey('ForumQuestions.id'))
    content = db.Column(db.Text())
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<ForumPost {}>'.format(self.id)


class Message(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sender_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    receiver_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Message ID {} ({} -> {})>'.format(self.id, self.sender_username, self.receiver_username)


class UserPost(db.Model):
    __tablename__ = 'UserPosts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<UserPost {} by {}>'.format(self.id, self.author_username)


class Follow(db.Model):
    __tablename__ = 'Follows'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    follower_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    following_username = db.Column(db.String(64), db.ForeignKey('Users.username'), nullable=False)
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Follow ID {} ({} -> {})>'.format(self.id, self.follower_username, self.following_username)

class Searchable(db.Model):
    __tablename__ = 'Searchable'
    __searchable__ = ["user_first_name"]
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_first_name = db.Column(db.String(64), index=True, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

def create_db_models():
    db.create_all()
    db.session.commit()

create_db_models()