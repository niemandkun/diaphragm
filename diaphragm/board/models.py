from datetime import datetime

from diaphragm.database import db


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80))
    bump = db.Column(db.DateTime)

    def __init__(self, subject):
        self.subject = subject.strip()
        self.bump = datetime.utcnow()

    def op(self):
        return self.posts.first()

    def last(self, count):
        return self.posts.order_by(Post.id.desc()).limit(count)


class Like(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    post = db.relationship('Post', backref=db.backref('likes', lazy='dynamic'))
    ip_address = db.Column(db.String(80), primary_key=True, nullable=False)

    def __init__(self, post_id, ip_address):
        self.post_id = post_id
        self.ip_address = ip_address


class Dislike(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    post = db.relationship('Post', backref=db.backref('dislikes', lazy='dynamic'))
    ip_address = db.Column(db.String(80), primary_key=True, nullable=False)

    def __init__(self, post_id, ip_address):
        self.post_id = post_id
        self.ip_address = ip_address


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    attachment = db.Column(db.String(80))
    message = db.Column(db.Text)
    time = db.Column(db.DateTime)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    thread = db.relationship('Thread', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, thread, message, author=None, attachment=None, time=None):
        if not author:
            author = "Anonymous"

        if not time:
            time = datetime.utcnow()

        self.attachment = attachment
        self.message = message.strip()
        self.author = author.strip()
        self.thread = thread
        self.time = time

    def __repr__(self):
        return "<Post {}>".format(self.time)
