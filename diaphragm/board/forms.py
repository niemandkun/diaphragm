from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


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
