from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired,Email,InputRequired,EqualTo, Length

class userSignUp(FlaskForm):

	name = StringField('Nome:', validators = [DataRequired(), Length(3, 20, 'O nome deve ter entre 3 e 20 caracteres.')])
	email = StringField('E-Mail:', validators = [DataRequired(), Email('Insira um endereço de E-mail valido.')])
	confirm_email = StringField('Confirme o E-mail:', validators = [DataRequired(), EqualTo('email', 'Ambos os campos devem ser iguais.')])
	pswd = PasswordField('Senha:', validators = [DataRequired(), Length(5, 15, 'A senha deve ter entre 5 e 15 caracteres.')])
	confirm_pswd  = PasswordField('Confirme a senha:', validators = [DataRequired(), EqualTo('pswd', 'Ambos os campos devem ser iguais.')])
	submit = SubmitField('Enviar')

class userLogin(FlaskForm):
	login_email = StringField("E-Mail",validators=[DataRequired(),Email()])
	login_pswd = PasswordField("Senha",validators=[DataRequired()])
	login_submit = SubmitField("Enviar")

class colaboratorSignUp(FlaskForm):

	name = StringField('Nome:', validators = [DataRequired(), Length(3, 20, 'O nome deve ter entre 3 e 20 caracteres.')])
	email = StringField('E-mail:', validators = [DataRequired(), Email('Insira um endereço de E-mail valido.')])
	confirm_email = StringField('Confirme o E-mail:', validators = [DataRequired(), EqualTo('email', 'Ambos os campos devem ser iguais.')])
	pswd = PasswordField('Senha:', validators = [DataRequired(), Length(5, 15, 'A senha deve ter entre 5 e 15 caracteres.')])
	confirm_pswd  = PasswordField('Confirme a senha:', validators = [DataRequired(), EqualTo('pswd', 'Ambos os campos devem ser iguais.')])
	submit = SubmitField('Enviar')

class applicationSignUp(FlaskForm):

	name = StringField("Nome",validators= [DataRequired(), Length(3, 20, 'O nome deve ter entre 3 e 20 caracteres.')])
	email = StringField('E-mail:', validators = [DataRequired(), Email('Insira um endereço de E-mail valido.')])
	confirm_email = StringField('Confirme o E-mail:', validators = [DataRequired(), EqualTo('email', 'Ambos os campos devem ser iguais.')])
	pswd = PasswordField('Senha:', validators = [DataRequired(), Length(5, 15, 'A senha deve ter entre 5 e 15 caracteres.')])
	confirm_pswd  = PasswordField('Confirme a senha:', validators = [DataRequired(), EqualTo('pswd', 'Ambos os campos devem ser iguais.')])
	questions = StringField("Rótulos Separados Por (,)",validators=[DataRequired()])
	submit = SubmitField("Enviar")

class findEmail(FlaskForm):
	email = StringField("Email:",validators=[Email()])

class payment(FlaskForm):
	#id = StringField("Application ID",validators=[DataRequired()])
	key_type = SelectField("Tipo de plano",choices=[(1,"10,000 requisitions"),(2,"100,000 requisitions"),(3,"1,000,000 requisitions")])
	submit = SubmitField("Enviar")

class searchColab(FlaskForm):
	cid = StringField(validators= [InputRequired()], render_kw={"placeholder":"ID do Colaborador"})
	submit = SubmitField("Enviar")

class manageColab(FlaskForm):
	cid = StringField(validators= [InputRequired()], render_kw={"placeholder":"ID do Colaborador"})
	status = StringField(validators= [InputRequired()], render_kw={"placeholder":"Status do Colaborador"})
	submit = SubmitField("Enviar")

class getScore(FlaskForm):
	submit = SubmitField("Procurar")