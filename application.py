
#Flask
from flask import Flask, url_for, redirect, render_template, request, session, send_file, flash
#MYSQL
import mysql.connector
#Config
from config import DevConfig
#Security libraries
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
#System
import pathlib
from datetime import datetime
#Import del formulario
import userform

application = app = Flask(__name__)

app.config.from_object(DevConfig)

#Conexion SQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)

#Variables globales
global user_datos
user_datos=[]
global vector
vector = []
global vector2
vector2 = []
global band
band = 0


@app.before_request
def before_request():
  #Si quieren ingresar al login sin cerrar sesion, para evitar bugs
  if 'username' in session and request.endpoint in ['auth.login', 'auth.registro', 'auth.recuperar']:
    datos = session['username']
    if datos[7] == 1:  # alumnos
      return redirect(url_for('alumnos.vermaterias'))
    if datos[6] == 2:  # profesores
      return redirect(url_for('profesores.miscursos'))
    if datos[6] == 3:  # Admin
      return redirect(url_for('directores.listadocursos'))
  if 'username' in session:
    datos = session['username']

#Vistas
from views.auth.auth_routes import auth_bp
from views.alumnos.alumnos_routes import alumnos_views
from views.profesores.profesores_routes import profesores_views
from views.directores.directores_routes import directores_views
# Variables globalers global en la aplicación
app.config['band'] = 0
app.config['alumnos'] = []
app.config['userdatos'] = []
app.config['vector'] = []
app.config['vector2'] = []
app.config['bcurso'] = 0
app.config['balumno'] = 0
app.config['tipoins'] = 0
app.config['cursos'] = []
app.config['idcurso'] = 0
app.config['idmaterias'] = 0
#rutas
app.register_blueprint(auth_bp, url_prefix='/', template_folder='views/auth/templates') #auth
app.register_blueprint(alumnos_views, url_prefix='/', template_folder='views/alumnos/templates') #alumnos
app.register_blueprint(profesores_views, url_prefix='/', template_folder='views/profesores/templates') #profesores
app.register_blueprint(directores_views, url_prefix='/', template_folder='views/directores/templates') #directores

##########################################################
#Vista genericas - Comparten todos los usuarios o algunos
##########################################################
#Ver Horarios
@app.route('/verhorario/<int:id>') 
def verhorarioadmin(id):
  datos = session['username']
  if datos[7] == 1:
    id = datos[4]
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  mycursor = mydb.cursor()
  global band
  for x in range(1, 7):
    sql = "SELECT id_horario, id_dia, hora_i, hora_f, des_m FROM horarios, materias WHERE id_curso = %s and id_dia = %s and horarios.id_materia = materias.id_materia ORDER BY horarios.hora_f ASC"
    val = [id, x]
    mycursor.execute(sql, val)
    if x == 1: #Lunes
      h_lu = mycursor.fetchall()
      print(h_lu)
    if x == 2: #Martes
      h_ma = mycursor.fetchall()
      print(h_ma)
    if x == 3:  # Miercoles
      h_mi = mycursor.fetchall()
      print(h_mi)
    if x == 4:  # Jueves
      h_ju = mycursor.fetchall()
      print(h_ju)
    if x == 5:  # Viernes
      h_vi = mycursor.fetchall()
      print(h_vi)
    if x == 6:  # Sabado
      h_sa = mycursor.fetchall()
      print(h_sa)
  if datos[7] == 1:  # alumnos
    return render_template('verhorariosal.html', cursos=cursos[0], datos=datos, h_lu=h_lu, h_ma=h_ma, h_mi=h_mi,
                           h_ju=h_ju, h_vi=h_vi, h_sa=h_sa)
  if datos[6] == 3:  # Admin
    if h_lu and h_ma and h_mi and h_ju and h_vi and h_sa:
      return render_template('verhorariosad.html', cursos = cursos[0], datos = datos, h_lu = h_lu, h_ma = h_ma, h_mi = h_mi, h_ju = h_ju, h_vi = h_vi, h_sa= h_sa)
    else: #Si no existe un horario totalmente cargado
      app.config['band'] = 4
      return redirect(url_for('directores.crearsemana'))
  
#Nav Bar, Boton "Mis Datos"
@app.route('/misdatos')
def misdatos():
  datos = session['username']
  print(datos)
  if datos[7] == 1: #alumnos
    return render_template('verdatos.html', datos = datos)
  if datos[6] == 2: #profesores
    return render_template('verdatosprof.html', datos=datos)
  if datos[6] ==3: #Admin
    return render_template('verdatosad.html', datos=datos)
  
#Ver documentos alumnos, admin o profesores
@app.route('/verdocumento/<int:id>', methods=['GET', 'POST'])
def verdocumento(id):
  datos = session['username']
  ruta = pathlib.Path('./static/./static/resources/documentos/')
  if request.method == "POST":
    filtro = int(request.form.get(('idfiltro')))
    if filtro <= 4:
      mycursor = mydb.cursor()
      sql = "SELECT id_alumno, ci_a FROM alumnos WHERE id_alumno = %s"
      val = [id]
      mycursor.execute(sql, val)
      data = mycursor.fetchall()
      print(data)
      if data:
        data = data[0]
        data = str(data[1])
        if filtro == 1:
          filename = "cedula_" + data + ".pdf"
        if filtro == 2:
          filename = "antecedente_" + data + ".pdf"
        if filtro == 3:
          filename = "autorizacion_" + data + ".pdf"
        if filtro == 4:
          filename = "ficha_" + data + ".pdf"
        archivo = ruta / filename
        print(archivo)
        if archivo.exists():
          print("El arhivo existe")
          return send_file(archivo, as_attachment=True)
        else:
          app.config['band'] = 8
        if datos[7] == 1:  # alumnos
          return redirect(url_for('misdatos'))
        if datos[6] == 3:  # Admin
          return redirect(url_for('directores.moddatos', id=id))

      if datos[7] == 1:  # alumnos
        redirect(url_for('misdatos'))
      if datos[6] == 3:  # Admin
        return redirect(url_for('directores.moddatos', id=id))
    else:
      mycursor = mydb.cursor()
      sql = "SELECT id_profesor, ci_p FROM profesores WHERE id_profesor = %s"
      val = [id]
      mycursor.execute(sql, val)
      data = mycursor.fetchall()
      print(data)
      print("profe")
      if data:
        data = data[0]
        data = str(data[1])
        if filtro == 5:
          filename = "cedulaprof_" + data + ".pdf"
        if filtro == 6:
          filename = "constancia_ingresos_" + data + ".pdf"
        if filtro == 7:
          filename = "constancia_cargos_" + data + ".pdf"
        archivo = ruta / filename
        print(archivo)
        if archivo.exists():
          print("El arhivo existe")
          return send_file(archivo, as_attachment=True)
        else:
          app.config['band'] = 8
        if datos[6] == 2:  # profesores
          return redirect(url_for('misdatos'))
        if datos[6] == 3:  # Admin
          return redirect(url_for('directores.moddatos', id=id))
      if datos[6] == 2:  # profesores
        redirect(url_for('misdatos'))
      if datos[6] == 3:  # Admin
        return redirect(url_for('directores.moddatos', id=id)) 
       
#Nav Bar, Boton "Configuracion de Cuenta"
@app.route('/miconfig', methods = ['GET', 'POST'])
def misconfig():
  global band
  datos = session['username']
  user = userform.User(request.form)
  if band == 1:
    band = 0
    flash("","c_u")
  if band == 2:
    band = 0
    flash("","co_u")
  if band == 3:
    band = 0
    flash("", "p_u")
  mycursor = mydb.cursor()
  if datos[7] == 1:  # alumnos
    sql = "SELECT * FROM user WHERE id_user = %s"
    val = [datos[6]]
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    print(data[0])
  else:
    sql = "SELECT * FROM user WHERE id_user = %s"
    val = [datos[5]]
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    print(data[0])
  if request.method == 'POST':
    us = user.username.data
    pasw = user.password.data
    em = user.email.data
    cpasw = user.confirmpassword.data
    cpasw2 = user.confirmpassword2.data
    if us and pasw:
      sql = "SELECT id_user FROM user WHERE username = %s"
      val = [us]
      mycursor.execute(sql, val)
      comp_u = mycursor.fetchall()
      if comp_u:
        flash("", "us_e")
      else:
        if data:
          userdata = data[0]
          # print(userdata)
          if userdata:
            passcheck = userdata[3]
            # print(passcheck)
            print(us)
          if userdata and check_password_hash(passcheck, pasw):
            sql = "UPDATE user SET username =  %s WHERE id_user = %s"
            val = (us, datos[6])
            mycursor.execute(sql, val)
            mydb.commit()
            band = 1
            return redirect(url_for('misconfig'))
          else:
            flash("", "psw")
    if em and pasw:
      if data:
        userdata = data[0]
        # print(userdata)
        if userdata:
          passcheck = userdata[3]
        if userdata and check_password_hash(passcheck, pasw):
          sql = "UPDATE user SET email = %s WHERE id_user = %s"
          val = (em, datos[6])
          mycursor.execute(sql, val)
          mydb.commit()
          band = 2
          return redirect(url_for('misconfig'))
        else:
          flash("", "psw")
    if pasw and cpasw and cpasw2:
      if data:
        userdata = data[0]
        if userdata:
          passcheck = userdata[3]
        if userdata and check_password_hash(passcheck, pasw):
          if cpasw == cpasw2:
            password = createpassword(cpasw)
            sql = "UPDATE user SET password = %s WHERE id_user = %s"
            val = (password, datos[6])
            mycursor.execute(sql, val)
            mydb.commit()
            band = 3
            return redirect(url_for('misconfig'))
          else:
            flash("", "psw2")
        else:
          flash("", "psw")
  if datos[7] == 1:  # alumnos
    return render_template('miconfig.html', datos=datos, data=data[0], user=user)
  if datos[6] == 2:  # profesores
    return render_template('miconfigpro.html', datos=datos, data=data[0], user=user)
  if datos[6] == 3:  # Admin
    return render_template('miconfigad.html', datos=datos, data=data[0], user=user)

def createpassword(password):
  return generate_password_hash(password)

 #Nav Bar, Boton "Cerrar Sesion"
@app.route('/cerrarsesion')
def cerrarsesion():
  if 'username' in session:
    session.pop('username')
  return redirect(url_for('auth.login'))

#ABM Cargar Materias, desabilitado.
#@app.route('/cargar', methods = ['GET', 'POST']) 
def cargar():
  alumno = userform.Alumno(request.form)
  if request.method == 'POST':
    cur = request.form.getlist(('idalum'))
    enf = request.form.get(('enfasis'))
    sec = request.form.get(('seccion'))
    ch1 = request.form.get(('car_1'))
    ch2 = request.form.get(('car_2'))
    ch3 = request.form.get(('car_3'))
    #print(alumno.nombre.data)
    #print(cur)
    #print(ch1)
    nmb = (alumno.nombre.data ,)
    sql = "SELECT id_materia FROM materias WHERE des_m = %s"
    mycursor = mydb.cursor()
    val = [alumno.nombre.data]
    mycursor.execute(sql, val)
    id_m = mycursor.fetchall()
    #print(enf)
    #print(sec)
    mycursor = mydb.cursor()
    if enf == "Sociales": #Dependiendo del enfasis para no consultar la bd
      enf = 2
    else:
      enf = 1
    #print(enf)
    if id_m:
      pass
    else:
      mycursor.execute('INSERT INTO materias (des_m) VALUES (%s)', (nmb))
      mydb.commit()
    cursos = []
    for x in range(0, len(cur)): #Sacar los cursos seleccionados
      #print(x)
      aux = cur[x]
      mycursor = mydb.cursor()
      sql = "SELECT id_curso, id_enfasis FROM cursos WHERE des_c = %s and sec_c = %s and id_enfasis = %s"
      val = [aux, sec, enf]
      mycursor.execute(sql, val)
      aux = mycursor.fetchall()
      #print(aux)
      aux = aux[0]
      #print(aux)
      cursos.append(aux)
    print(cursos)
    sql = "SELECT id_materia FROM materias WHERE des_m = %s"
    val = [alumno.nombre.data]
    mycursor.execute(sql, val)
    id_m = mycursor.fetchall()
    id_m = id_m[0]
    print(id_m)
    for x in range(0, len(cursos)):  # Sacar los cursos seleccionados
      # print(x)
      aux = cursos[x]
      print(aux)
      print(cur[x])
      if cur[x] == "Primer Curso":
        ch = ch1
      if cur[x] == "Segundo Curso":
        ch = ch2
      if cur[x] == "Tercer Curso":
        ch = ch3
      mycursor = mydb.cursor()
      mycursor.execute(
        'INSERT INTO matxcur (id_curso, id_materia, id_enfasis, car_h) VALUES (%s, %s, %s ,%s)',
        (aux[0], id_m[0], aux[1], ch))
      mydb.commit()
  return render_template('cargarm.html', alumno = alumno)

#Marcar Asistencia por Docente
@app.route('/asistencia',  methods = ['GET', 'POST']) 
def asistenciaprof():
  global user_datos #datos del profe para alerta
  global vector # hora de entrada
  global band
  global vector2 # hora de salida
  print(band)
  if band == 1:
    profesor = user_datos
    print(profesor)
    flash("", "entrada")
    band = 0
  if band == 2:
    profesor = user_datos
    print(profesor)
    print(vector)
    flash("", "salida")
    band = 0
  if band == 3: #ya marco
    profesor = user_datos
    print(profesor)
    print(vector2)
    print(vector)
    flash("", "no")
    band = 0
  if band == 4:
    profesor = user_datos
    print(profesor)
    flash("", "no_dia")
    band = 0
  if band == 5:
    band = 0
  user = userform.User(request.form)
  inf = datetime.now()
  #Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  #Extraemos la hora
  hora = datetime.strftime(inf, '%H:%M:%S')
  dia = datetime.today().weekday()
  print(fecha)
  print(hora)
  #Por que yo realize que Lunes = 1
  dia += 1
  print(dia)
  profesor = user_datos
  mycursor = mydb.cursor()
  #Crea un nuevo dia para asistencia de los profes
  sql = "SELECT id_asisprof, fec_a FROM asistenciaprof WHERE fec_a = %s"
  val = [fecha]
  mycursor.execute(sql, val)
  compf = mycursor.fetchall()
  print(compf)
  compc = []
  if not compf:
    #Saca los ids de los profes que deben marcar hoy
    sql = "SELECT id_horario, id_profesor FROM horarios WHERE id_dia =%s"
    val = [dia]
    mycursor.execute(sql, val)
    idsp = mycursor.fetchall()
    print(idsp)
    cont = 0
    for x in range(0, len(idsp)):
      aux = idsp[x]
      if aux[1] != 0:
        if cont == 0:
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO asistenciaprof (id_profesor, fec_a) VALUES (%s, %s)',
            (aux[1], fecha))
          mydb.commit()
          cont = 1
          compc.append(aux[1])
        if aux[1] not in compc:
          print(aux[1])
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO asistenciaprof (id_profesor, fec_a) VALUES (%s, %s)',
            (aux[1], fecha))
          mydb.commit()
          compc.append(aux[1])
          print(compc)
  if request.method == 'POST':
    #Codigo del input que sale del escaneo de la tarjeta
    codigo = user.username.data
    codigo = codigo.split('P')
    print(codigo)
    #Buscamos por cedula del proesor
    sql = "SELECT * FROM profesores WHERE ci_p = %s"
    val = [codigo[1]]
    mycursor.execute(sql, val)
    profesor = mycursor.fetchall()
    if profesor:
      profesor = profesor[0]
      user_datos = profesor #guardar para las alertas
      print(profesor)
      #Comprueba que el profesor tenga clases hoy
      sql = "SELECT id_horario, id_curso, id_materia, id_dia, hora_i, hora_f FROM horarios WHERE id_profesor = %s and id_dia =%s  ORDER BY horarios.hora_i ASC"
      val = [profesor[0], dia]
      mycursor.execute(sql, val)
      ent = mycursor.fetchall()
      if ent:
        ent = ent[0]
        ent = ent[4]
      print("Entrada:")
      print(ent)
      sql = "SELECT id_horario, id_curso, id_materia, id_dia, hora_i, hora_f FROM horarios WHERE id_profesor = %s and id_dia =%s  ORDER BY horarios.hora_f DESC"
      val = [profesor[0], dia]
      mycursor.execute(sql, val)
      sal = mycursor.fetchall()
      if sal:
        sal = sal[0]
        sal = sal[5]
      print("Salida:")
      print(sal)
      if ent and sal:
        sql = "SELECT hora_e, hora_s, fec_a FROM asistenciaprof WHERE id_profesor = %s and fec_a = %s"
        val = [profesor[0], fecha]
        mycursor.execute(sql, val)
        comp = mycursor.fetchall()
        print(comp)
        if comp:
          comp = comp[0]
          if comp[0] and not comp[1]:
            print("Ya Marco entrada, marca salida")
            vector = comp[0]  # entrada
            sql = "UPDATE asistenciaprof SET hora_s = %s WHERE id_profesor = %s and fec_a = %s"
            val = (hora, profesor[0], fecha)
            mycursor.execute(sql, val)
            mydb.commit()
            band = 2
            return redirect(url_for('asistenciaprof'))
          if comp[1]:
            vector = comp[0]
            vector2 = comp[1]  # salida
            print("Marco Salida, ya no puede marcar hoy")
            band = 3
            return redirect(url_for('asistenciaprof'))
          if not comp[0] and not comp[1]:
            print("No marco hoy, marca entrada")
            mycursor = mydb.cursor()
            sql = "UPDATE asistenciaprof SET hora_e = %s WHERE id_profesor = %s and fec_a = %s"
            val = (hora, profesor[0], fecha)
            mycursor.execute(sql, val)
            mydb.commit()
            band = 1
            return redirect(url_for('asistenciaprof'))
        else:
          print("No es su dia, no puede marcar")
          print(user_datos)
          band = 4
          return redirect(url_for('asistenciaprof'))
      else:
        band = 4
        return redirect(url_for('asistenciaprof'))
    else:
      print("Error no esta en el sistema")
      flash("","noesta")
  return render_template('asistenciaprof.html', user = user, profesor = profesor, vector= vector, vector2= vector2, hora = hora)
##########################################################
#Vistas Genericas - END
##########################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)