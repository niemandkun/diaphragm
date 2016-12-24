from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FileField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    fileupload = FileField('Attach picture')

    thread = HiddenField('Thread', validators=[DataRequired()])

    author = StringField('Name', render_kw={'placeholder': 'Name'},
                         validators=[Length(max=80)])

    message = StringField('Message', validators=[DataRequired(), Length(max=5000)],
                          render_kw={'placeholder': 'Message'},
                          widget=TextArea())


class ThreadForm(FlaskForm):
    fileupload = FileField('Attach picture')

    subject = StringField('Subject', render_kw={'placeholder': 'Subject'},
                          validators=[Length(max=80)])

    author = StringField('Name', render_kw={'placeholder': 'Name'},
                         validators=[Length(max=80)])

    message = StringField('Message', validators=[DataRequired(), Length(max=5000)],
                          render_kw={'placeholder': 'Message'},
                          widget=TextArea())
