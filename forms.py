from wtforms import Form 
from wtforms import StringField, IntegerField, PasswordField, FloatField
from wtforms import EmailField
from wtforms import validators
from wtforms import RadioField

class UserForm2(Form): 
    id=IntegerField("Id",[
        validators.NumberRange(min=1, max=20, message="Valor no valido")
    ])
    nombre=StringField("Nombre",[
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4, max=20, message="Requiere min=4 max=20")
    ])
    apaterno=StringField("Apaterno",[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message="Ingrese un apellido valido")
    ])
    correo=EmailField("Correo", [
        validators.Email(message="Ingresa un correo valido")
    ])