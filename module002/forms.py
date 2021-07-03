from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length



class CommentForm(FlaskForm): # class RegisterForm extends FlaskForm
    comment = TextAreaField('Write your comment', validators=[Length(max=50), InputRequired()])
    submit_button = SubmitField('POSTEAR')

