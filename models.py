from init import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    school = db.Column(db.String(64))
    grade = db.Column(db.String(64))
    state = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)
