from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo, URL


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Please use at least 8 characters in your password")
        if password.data == "password":
            raise ValidationError(
                'Seriously? (¬_¬) use something other than "password"'
            )


class CreateFeedForm(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired()], render_kw={"placeholder": "Cool Site"}
    )
    link = StringField(
        "Feed Link",
        validators=[DataRequired(), URL()],
        render_kw={"placeholder": "http://example.com"},
    )
    desc = TextAreaField(
        "Description", render_kw={"placeholder": "an RSS feed from a very cool website"}
    )
    pattern = TextAreaField(
        "Item Search Pattern",
        validators=[DataRequired()],
        render_kw={"placeholder": '<div id="{*}" class="post">{%}</div>'},
    )
    address = StringField(
        "Address",
        validators=[DataRequired(), URL()],
        render_kw={"placeholder": "http://example.com/posts"},
    )
    item_title_template = StringField(
        "Item Title Template",
        validators=[DataRequired()],
        render_kw={"placeholder": "{%1}"},
    )
    item_link_template = StringField(
        "Item Link Template",
        validators=[DataRequired()],
        render_kw={"placeholder": "{%2}"},
    )
    item_content_template = StringField(
        "Item Content Template",
        validators=[DataRequired()],
        render_kw={"placeholder": "{%3}"},
    )
    submit = SubmitField("Add!!")
