from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length

db = SQLAlchemy()


class PostForm(FlaskForm):
    fileupload = FileField('Attach picture')

    thread = HiddenField('Thread', validators=[DataRequired()])

    author = StringField('Name', render_kw={'placeholder': 'Name'},
                         validators=[Length(max=80)])

    message = StringField('Message', validators=[DataRequired()],
                          render_kw={'placeholder': 'Message'},
                          widget=TextArea())


class ThreadForm(FlaskForm):
    fileupload = FileField('Attach picture')

    subject = StringField('Subject', render_kw={'placeholder': 'Subject'})

    author = StringField('Name', render_kw={'placeholder': 'Name'},
                         validators=[Length(max=80)])

    message = StringField('Message', validators=[DataRequired()],
                          render_kw={'placeholder': 'Message'},
                          widget=TextArea())


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80))

    def __init__(self, subject):
        self.subject = subject

    def op(self):
        return self.posts.first()

    def last(self, count):
        return self.posts.order_by(Post.id.desc()).limit(count)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    attachment = db.Column(db.String(80))
    message = db.Column(db.Text)
    time = db.Column(db.DateTime)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    thread = db.relationship('Thread',
            backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, thread, message, author=None, attachment=None, time=None):
        if not author:
            author = "Anonymous"

        if not time:
            time = datetime.utcnow()

        self.attachment = attachment
        self.message = message
        self.thread = thread
        self.author = author
        self.time = time

    def __repr__(self):
        return "<Post {}>".format(self.time)
