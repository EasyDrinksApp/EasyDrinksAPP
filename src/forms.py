from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, TextAreaField, SelectField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import Required, NumberRange


class FormProducto(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[Required("Tienes que introducir el dato")]
                         )
    precio = DecimalField("Precio:", default=0,
                          validators=[Required("Tienes que introducir el dato")
                                      ])
    stock = IntegerField("Stock:", default=1,
                         validators=[Required("Tienes que introducir el dato")]
                         )
    CategoriaId = SelectField("Categoría:", coerce=int)
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    usuario = StringField('', validators=[Required()], render_kw={"placeholder": "Usuario"})
    password = PasswordField('', validators=[Required()], render_kw={"placeholder": "Contraseña"})
    submit = SubmitField('Entrar')

class FormCliente(FlaskForm):
    usuario = StringField('', validators=[Required()], render_kw={"placeholder": "Usuario"})
    password = PasswordField('', validators=[Required()], render_kw={"placeholder": "Contraseña"})
    nombre = StringField('', render_kw={"placeholder": "Nombre completo"})
    email = EmailField('', render_kw={"placeholder": "Email"})
    submit = SubmitField('Aceptar')


class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Aceptar')


class FormCarrito(FlaskForm):
    id = HiddenField()
    cantidad = IntegerField('Cantidad', default=1,
                            validators=[NumberRange(min=1,
                                                    message="Debe ser un númer"
                                                            "o positivo"),
                                        Required("Tienes que introducir el "
                                                 "dato")])
    submit = SubmitField('Aceptar')