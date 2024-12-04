from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class CompleteRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Complete Registration')

class InviteUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Invite')

class CreateTeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    team_members = SelectMultipleField('Team Members', validators=[DataRequired()])
    submit = SubmitField('Create Team')

    def __init__(self, friends=None, *args, **kwargs):
        super(CreateTeamForm, self).__init__(*args, **kwargs)
        if friends:
            self.team_members.choices = [(str(friend.id), friend.username) for friend in friends]
        else:
            self.team_members.choices = []

class DeleteTeamForm(FlaskForm):
    team_id = HiddenField('team_id', validators=[DataRequired()])

class AddFriendForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add Friend')

class RemoveFriendForm(FlaskForm):
    friend_id = HiddenField('friend_id', validators=[DataRequired()])
    submit = SubmitField('Remove Friend')

class CreateGameForm(FlaskForm):
    list_id = SelectField('Jargon List', validators=[DataRequired()])
    team_id = SelectField('Team', validators=[DataRequired()])
    submit = SubmitField('Create Game')

    def __init__(self, jargon_lists=None, teams=None, *args, **kwargs):
        super(CreateGameForm, self).__init__(*args, **kwargs)
        if jargon_lists:
            self.list_id.choices = [(str(jargon_list.id), jargon_list.name) for jargon_list in jargon_lists]
        else:
            self.list_id.choices = []
        if teams:
            self.team_id.choices = [(str(team.id), team.name) for team in teams]
        else:
            self.team_id.choices = []