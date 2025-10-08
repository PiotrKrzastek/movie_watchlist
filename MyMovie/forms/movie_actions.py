from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, URLField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo

class StringListField(TextAreaField):
    def _value(self):
        if self.data:
            return '\n'.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split('\n')]
        else:
            self.data = []

class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])

    year = IntegerField(
        "Year",
        validators=[
            InputRequired(),
            NumberRange(1800,message="Please enter a year in format: YYYY.")
        ]
    )

    submit = SubmitField("Add Movie")


class ExtendedMovieForm(MovieForm):
    description = TextAreaField("Description")
    tags = StringListField("Genres")
    cast = StringListField("Cast")
    series = StringListField("Series")
    video_link = URLField("Video Link")

    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[
                            InputRequired(),
                            Length(min=6, message="Password must be at least 6 characters long.")
                            ]
                           )
    confirm_password = PasswordField("Confirm Password", validators=[
                            InputRequired(),
                            EqualTo('password', message="Passwords must match.")
                            ]
                           )
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])

    submit = SubmitField("Login")
