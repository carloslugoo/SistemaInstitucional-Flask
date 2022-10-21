from wtforms import Form
from wtforms import StringField, EmailField, TextAreaField, PasswordField, IntegerField, DateField
from wtforms import validators
#Formulario de Usuarios
class User(Form):
 username = StringField('Usuario:',
                        [validators.length(min=4, max=12, message='Ingrese un usuario de 4 a 25 letras!..'),
                         validators.data_required(message='Ingrese un Usuario!')])

 email = EmailField('Email:',
                        [validators.length(min=4, max=25, message='Ingrese un usuario de 4 a 25 letras!..'),
                         validators.data_required(message='Ingrese un Usuario!')])


 password = PasswordField('Contraseña:',
                    [validators.data_required(message='Ingrese un Contraseña!'),
                     validators.length(min=4, max=25, message='Ingrese un contraseña de 4 a 25 letras!..')])

 confirmpassword = PasswordField('Confirmar Contrasena',
                          [validators.data_required(message='Ingrese un Contraseña!'),
                           validators.length(min=4, max=25, message='Ingrese un contraseña de 4 a 25 letras!..')])

 confirmpassword2 = PasswordField('Confirmar Contrasena',
                                 [validators.data_required(message='Ingrese un Contraseña!'),
                                  validators.length(min=4, max=25,
                                                    message='Ingrese un contraseña de 4 a 25 letras!..')])

 ci = StringField('Cedula de Identidad:',
                        [validators.length(min=7, max=7, message='Ingrese un numero de cedula valido!'),
                         validators.data_required(message='Ingrese su numero de CI!')])

class Task(Form):
    nombre = StringField('Trabajo:',
                           [validators.length(min=5, max=40, message='El trabajo debe tener 5 a 40 letras'),
                            validators.data_required(message='Ingrese el nombre del trabajo!')])

    puntaje = StringField('Trabajo:',
                         [validators.length(min=1, max=3, message='El puntaje maximo es 100..'),
                          validators.data_required(message='Ingrese un puntaje!')])

class Alumno(Form):
    nombre = StringField('Nombre Completo:',
                         [validators.length(min=4, max=50, message='El nombre debe tener 10 a 50 letras'),
                          validators.data_required(message='Ingrese el nombre del alumno!')])

    apellido = StringField('Apellido Completo:',
                         [validators.length(min=4, max=50, message='El apellido debe tener 10 a 50 letras'),
                          validators.data_required(message='Ingrese el apellido del trabajo!')])

    edad = StringField('Edad:',
                           [validators.length(min=1, max=2, message='Ingrese una edad valida'),
                            validators.data_required(message='Ingrese una edad!')])

    num_c = StringField('Numero de Cedula:',
                       [validators.length(min=7, max=8, message='Ingrese un numero de cedula valido'),
                        validators.data_required(message='Ingrese una numero de cedula!')])

    num_t = StringField('Numero de Telefono:',
                       [validators.length(min=10, max=10, message='Ingrese un numero de contacto valido'),
                        validators.data_required(message='Ingrese una numero de contacto!')])

    localidad = StringField('Localidad:',
                       [validators.length(min=5, max=40, message='Ingrese el lugar de residencia'),
                        validators.data_required(message='Ingrese su lugar de residencia!')])

    nmb_pa = StringField('Nombre y Apellido del Tutor:',
                       [validators.length(min=4, max=50, message='Ingrese el nombre completo del tutor'),
                        validators.data_required(message='Ingrese un nombre!')])

    num_pa = StringField('Numero del Tutor:',
                       [validators.length(min=5, max=40, message='Ingrese algun numero de contacto'),
                        validators.data_required(message='Ingrese un numero de contacto!')])

    email = EmailField('Email:',
                       [validators.length(min=4, max=25, message='Ingrese un usuario de 4 a 25 letras!..'),
                        validators.data_required(message='Ingrese un Usuario!')])

    barrio = StringField('Barrio:',
                       [validators.length(min=5, max=40, message='Ingrese el lugar de residencia'),
                        validators.data_required(message='Ingrese su lugar de residencia!')])


