from flask import Blueprint
from flask import url_for, redirect, render_template, request, session, flash
import time
from werkzeug.security import check_password_hash
import userform
import mysql.connector
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='templates')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)


@auth_bp.route('/', methods = ['GET', 'POST']) #Login
def login():
  user = userform.User(request.form)
  username = user.username.data
  password = user.password.data
  if request.method == 'POST':
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM user WHERE username = %(username)s', {'username': username})
    data = mycursor.fetchall()
    if data:
      userdata = data[0]
      if userdata:
        passcheck = userdata[3]
      if userdata and check_password_hash(passcheck, password):
        global tipo
        tipo = userdata[4]
        if userdata[4] == 1:
          sql = "SELECT * FROM alumnos WHERE id_user = %s"
          val = [userdata[0]]
          mycursor.execute(sql, val)
          data = mycursor.fetchall()
          datos = data[0]
          session['tipo_u'] = userdata[4]
          session['username'] = datos
          time.sleep(1)
          return redirect(url_for('alumnos.vermaterias'))
        if userdata[4] == 2:
          sql = "SELECT * FROM profesores WHERE id_user = %s"
          val = [userdata[0]]
          mycursor.execute(sql, val)
          data = mycursor.fetchall()
          datos = data[0]
          session['username'] = datos
          return redirect(url_for('profesores.miscursos'))
        if userdata[4] == 3:
          sql = "SELECT * FROM admin WHERE id_user = %s"
          val = [userdata[0]]
          mycursor.execute(sql, val)
          data = mycursor.fetchall()
          datos = data[0]
          session['username'] = datos
          return redirect(url_for('bienvenidoadmin'))
      else:
        flash("Contra", "error_p")
    else:
      flash("Not found", "error_n")

  return render_template('login.html', user = user)


@auth_bp.route('/registro', methods = ['GET', 'POST']) #Registro, falta ver username cambiar por cedula ❌
def registro():
  user = userform.User(request.form)
  global band
  #pasw = user.password.data
  if request.method == 'POST':
    password = createpassword(user.password.data)
    create = False
    ci = int(user.ci.data)
    print(ci)
    mycursor = mydb.cursor()
    sql = "SELECT * FROM alumnos WHERE ci_a = %s"
    val = [ci]
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    t_u = 0
    if data:
      t_u = 1 #Alumnos
      print("alumno encontrado")
      create = True
    else:
      sql = "SELECT * FROM profesores WHERE ci_p = %s"
      val = [ci]
      mycursor.execute(sql, val)
      data = mycursor.fetchall()
      if data:
        t_u = 2  #Profesores
        print("profesor encontrado")
        create = True
      else:
        sql = "SELECT * FROM admin WHERE ci_ad = %s"
        val = [ci]
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        if data:
          t_u = 3  # Admin
          print("admin encontrado")
          create = True
        else:
          flash("Ya tiene cuenta", "ci_e")
    if data:
      print("a")
      data = data[0]
      print(data)
      if data[7] == 1:
        print("asdff")
        if data[6]:
          create = False
          flash("Ya tiene cuenta", "existe_ci")
          print("test")
        else:
          print("crear si")
          create = True
      elif data[6] == 2:
        print("asd")
        if data[5]:
          create = False
          flash("Ya tiene cuenta", "existe_ci")
          print("test")
        else:
          print("crear si")
          create = True
    if t_u > 0:
      sql = "SELECT * FROM user WHERE username = %s"
      val = [user.username.data]
      mycursor.execute(sql, val)
      coc = mycursor.fetchall()
      if coc:
        flash("User existente", "existe_us")
        print("a")
        create = False
      else:
        sql = "SELECT * FROM user WHERE email = %s"
        val = [user.email.data]
        mycursor.execute(sql, val)
        coe = mycursor.fetchall()
        if coe:
          flash("Correo existente", "existe_co")
          create = False
    if create == True:
      if user.password.data == user.confirmpassword.data:
        mycursor.execute('INSERT INTO user (username, email, password, tipo_u) VALUES (%s, %s, %s, %s)', (user.username.data,
                                                                                         user.email.data, password, t_u))
        mydb.commit()
        sql = "SELECT * FROM user WHERE username = %s"
        val = [user.username.data]
        mycursor.execute(sql, val)
        aux = mycursor.fetchall()
        print(aux)
        aux = aux[0]
        if t_u == 1:
          id = aux[0]
          sql = "UPDATE alumnos SET id_user= %s WHERE ci_a = %s"
          val = (id,ci)
          mycursor.execute(sql, val)
          mydb.commit()
        if t_u == 2:
          id = aux[0]
          sql = "UPDATE profesores SET id_user= %s WHERE ci_p = %s"
          val = (id, ci)
          mycursor.execute(sql, val)
          mydb.commit()
        else:
          id = aux[0]
          sql = "UPDATE admin SET id_user= %s WHERE ci_ad = %s"
          val = (id, ci)
          mycursor.execute(sql, val)
          mydb.commit()
        band = 1
        #flash("Correcto", "success")
        return redirect(url_for('login'))
      else:
        print("e")
        flash("Error", "psw")
  return render_template('register.html', user = user)

def createpassword(password):
  return generate_password_hash(password)