from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from flask_wtf.file import FileAllowed, FileField
from .models import User
from flask_login import current_user

class FormCreateAccount(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirm your Password", validators=[DataRequired(), EqualTo("senha")])
    botao_submit_criar_conta = SubmitField("Create Account")
    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("This e-mail is already registered!")
        
class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    lembrar = BooleanField("Rembemer Me")
    botao_submit_login = SubmitField("Login")

class FormEditProfile(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    profile_picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    botao_submit_editar_perfil = SubmitField("Confirm Edit")
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = User.query.filter_by(email=email.data).first()
            raise ValidationError("There is already a user with this e-mail!")
        
class FormLog(FlaskForm):
    status = RadioField('Status', choices=["Played", "Playing", "Want to Play"], validators=[DataRequired()])
    score = IntegerField('Your Rating', validators=[Optional(), NumberRange(min=0, max=100)])
    review_title = StringField('Review Title', validators=[Optional(), Length(max=200)])
    review_text = TextAreaField('Review')
    submit = SubmitField('Save Log')