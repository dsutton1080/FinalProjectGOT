from init import db

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    school = db.Column(db.String(128))
    school_grade = db.Column(db.String(64))
    state = db.Column(db.String(64))
    forum_questions = db.relationship("ForumQuestion")
    forum_posts = db.relationship("ForumPost")
    # messages = db.relationship("Message", foreign_keys=['sender_username', 'receiver_username'])
    user_posts = db.relationship("UserPost")
    # follows = db.relationship("Follow", foreign_keys=['follower_username', 'following_username'])

    def __repr__(self):
        return '<User {}>'.format(self.username)

class ForumQuestion(db.Model):
    __tablename__ = 'ForumQuestions'
    id = db.Column(db.Integer, primary_key=True)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    content = db.Column(db.Text())
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    forum_posts = db.relationship("ForumPost")

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
    id = db.Column(db.Integer, primary_key=True)
    sender_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    receiver_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    content = db.Column(db.Text())
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message ID {} ({} -> {})>'.format(self.id, self.sender_username, self.receiver_username)

class UserPost(db.Model):
    __tablename__ = 'UserPosts'
    id = db.Column(db.Integer, primary_key=True)
    author_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    content = db.Column(db.Text())
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<UserPost {} by {}>'.format(self.id, self.author_username)

class Follow(db.Model):
    __tablename__ = 'Follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    following_username = db.Column(db.String(64), db.ForeignKey('Users.username'))
    post_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Follow ID {} ({} -> {})>'.format(self.id, self.follower_username, self.following_username)