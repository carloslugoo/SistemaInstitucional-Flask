
#Flask
from flask import Flask, url_for, redirect, render_template, request, session, send_file, flash
#MYSQL
import mysql.connector
#Config
from config import DevConfig
#Security libraries
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
#System
import pathlib
from datetime import datetime
import os
#Import del formulario
import userform
#Reporte en pdf
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
#Reporte en excel
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Font


application = app = Flask(__name__)

app.config.from_object(DevConfig)


folder = os.path.abspath("./static/resources/documentos/")
ext_p = set(["pdf"])
ext_c = set(["xls", "xlsx", "xlsm", "xlsb", "xltx"])
app.config['folder'] = folder

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)
global bcurso
bcurso =0
global user_datos
user_datos=[]
global vector
vector = []
global vector2
vector2 = []
global cursos
cursos=[]
global idmaterias
idmaterias = 0
global alumnos
alumnos = []
global balumno
balumno = 0
global idcurso
idcurso = 0
global ci
ci = 0
global tel
tel = 0
global band
band = 0
global tipoins
tipoins = 0


@app.before_request
def before_request(): #antes de cargar la pag
  if 'username' in session and request.endpoint in ['login', 'registro', 'recuperar']:
    datos = session['username']
    if datos[7] == 1:  # alumnos
      return redirect(url_for('alumnos.vermaterias'))
    if datos[6] == 2:  # profesores
      return redirect(url_for('bienvenidoprofe'))
    if datos[6] == 3:  # Admin
      return redirect(url_for('bienvenidoadmin'))
  if 'username' in session:
    datos = session['username']
    if datos[7] == 1:
      if request.endpoint in ['bienvenidoadmin', 'inscribirdir','sacarmat', ' inscurmat', 'inscribirprof','proceso',
                              'procesoss', 'alumnosproceso', 'inscmatxprof', 'modproceso', 'modificarproceso2','miscursos',
                              'listadocursos', 'controldeplanilla', 'crearsemana', 'inscribirprof',
                              'inscribirdir', 'asignarpof', 'generarcuotas', 'verlog',
                              'miscursos','enviarplanilla', 'verasistenciaprofe', 'proceso']:
        return redirect(url_for('vermaterias'))
    if datos[6] == 2:
      if request.endpoint in ['verproceso','vermaterias ', 'bienvenidoadmin', 'inscribirdir', 'sacarmat',
                              'inscurmat', 'inscribirprof', 'inscmatxprof',
                              'listadocursos', 'controldeplanilla', 'crearsemana', 'inscribirprof',
                              'inscribirdir', 'asignarpof', 'generarcuotas', 'verlog', 'miscuotasal', 'vermaterias'
                              ]:
        return redirect(url_for('bienvenidoprofe'))
    if datos[6] == 3:
      if request.endpoint in ['verproceso', 'vermaterias', 'proceso', 'procesoss', 'alumnosproceso', 'modproceso',
                              'modificarproceso2','miscursos',
                              'miscursos','enviarplanilla', 'verasistenciaprofe', 'proceso', 'miscuotasal', 'vermaterias']:
        return redirect(url_for('bienvenidoadmin'))

#Vistas
from views.auth.auth_routes import auth_bp
from views.alumnos.alumnos_routes import alumnos_views
from views.profesores.profesores_routes import profesores_views
from views.directores.directores_routes import directores_views
# Configurar la variable global en la aplicación
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



@app.route('/inscribirprofe', methods = ['GET', 'POST']) #Inscripcion de Profesor, carga.
def inscribirprof():
  alumno = userform.Alumno(request.form) #Reutilizo el form
  datos = session['username']
  global band
  global idmaterias
  print(band)
  if band == 1:
    flash("", "si")
    band = 0
  if band == 3:
    band  = 0
    flash("", "no")
  if band == 4:
    band = 0
    flash("", "profe")
  global tipoins
  tipoins = 2
  if request.method == "POST":
    co_i = request.files["co_i"]
    cedu = request.files["cedu_p"]
    co_c = request.files["co_c"]
    fecha = (request.form['fec_n'])
    print(fecha)
    if fecha:
      # Parte Cedula...
      if "cedu_p" not in request.files:
        # print("No envio nada")
        pass
      elif cedu.filename == "":
        # print("No mando nada")
        pass
      elif cedu and archpermi(cedu.filename):
        filename = secure_filename(cedu.filename)
        extc = filename.split('.')
        print(extc)
        print(filename)
        print(alumno.num_c.data)
        filename = "cedulaprof_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        cedu.save(os.path.join(app.config["folder"], filename))
        flash("", "")  # Ya guarda el archivo
      else:
        print("archivo no permitido")
      # Parte Constancia de Ingresos
      if "co_i" not in request.files:
        #print("No envio nada")
        pass
      elif co_i.filename == "":
        #print("No mando nada")
        pass
      elif co_i and archpermi(co_i.filename):
        filename = secure_filename(co_i.filename)
        extc = filename.split('.')
        print(extc)
        print(filename)
        print(alumno.num_c.data)
        filename = "constancia_ingresos_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        co_i.save(os.path.join(app.config["folder"], filename))
        flash("", "")  # Ya guarda el archivo
      else:
        print("archivo no permitido")
      # Parte Autorizacion de Padres
      if "co_c" not in request.files:
        #print("No envio nada")
        pass
      elif co_c.filename == "":
        #print("No mando nada")
        pass
      elif co_c and archpermi(co_c.filename):
        filename = secure_filename(co_c.filename)
        extc = filename.split('.')
        print(extc)
        print(filename)
        print(alumno.num_c.data)
        filename = "constancia_cargos_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        co_c.save(os.path.join(app.config["folder"], filename))
        flash("", "")  # Ya guarda el archivo
      else:
        print("archivo no permitido")
      mycursor = mydb.cursor()
      print(cursos)
      global cur
      global enf
      global sec
      global ci
      global tel
      cur = request.form.get(('curso'))
      enf = request.form.get(('enfasis'))
      sec = request.form.get(('seccion'))
      ci = alumno.num_c.data
      tel = alumno.num_t.data
      # Validar si la cedula y el num de telefono no son repetidos..
      sql = "SELECT ci_p FROM profesores WHERE ci_p = %s"
      val = [ci]
      mycursor.execute(sql, val)
      comp_p = mycursor.fetchall()
      if comp_p:
        print(comp_p)
        flash("", "error")
      else:
        # Inserta en tabla profesores todos los datos
        mycursor.execute(
          'INSERT INTO profesores (nmb_p, ape_p, tel_p, ci_p, edad, email, loc_p, fec_p, bar_p) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
          (alumno.nombre.data, alumno.apellido.data, alumno.num_t.data, alumno.num_c.data, alumno.edad.data,
           alumno.email.data, alumno.localidad.data, fecha, alumno.barrio.data))
        mydb.commit()
        # Auditoria
        inf = datetime.now()
        # Extraemos la fecha
        fecha = datetime.strftime(inf, '%Y/%m/%d')
        mycursor = mydb.cursor()
        mycursor.execute(
          'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
          (datos[0], "Incorporó al docente {a}, {b} al sistema".format(a=alumno.nombre.data, b=alumno.apellido.data),
           fecha))
        mydb.commit()
        return redirect(url_for('inscmatxprof'))
    else:
      print("no fehca")
      flash("fecha", "fecha")
  return render_template('inscribirprof.html', datos=datos, alumno=alumno, profe = idmaterias)

@app.route('/inscribirprofee', methods = ['GET', 'POST']) #Parte de incorporacion, carga de materias por  profe
def inscmatxprof():
  bver = 0
  datos = session['username']
  global idmaterias #Contiene el nombre de las materias y sus id
  global ci
  global tel
  global tipoins
  global band
  tipoins = 2 #Profesores
  fecha = datetime.now()
  fecha = datetime.strftime(fecha, '%Y')
  print(fecha)
  mycursor = mydb.cursor(buffered=True)
  for x in range(1, 7):
    print(x)
    if x <= 3:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 1]
      mycursor.execute(sql, val)
      if x == 1:
        con_p = mycursor.fetchall()
        print(con_p)
      if x == 2:
        con_s = mycursor.fetchall()
        print(con_s)
    if x == 3:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 2]
      mycursor.execute(sql, val)
      soc_p = mycursor.fetchall()
      print(soc_p)
    if x == 4:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 1]
      mycursor.execute(sql, val)
      con_t = mycursor.fetchall()
      print(con_t)
    if x > 4:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 2]
      mycursor.execute(sql, val)
      if x == 5:
        soc_s = mycursor.fetchall()
        print(soc_s)
      if x == 6:
        soc_t = mycursor.fetchall()
        print(soc_t)
  if request.method == 'POST':
    if ci == 0 or tel == 0:
      band = 3
      return redirect(url_for('inscribirprof'))
    idmat = request.form.getlist(('idmat')) #Aca si tengo los id de las materias en q se insc
    idcur = request.form.getlist(('idcur'))
    print(idmat)
    print(idcur)
    mycursor = mydb.cursor()
    sql = "SELECT id_profesor, id_user FROM profesores WHERE ci_p = %s and tel_p = %s"
    val = [ci,tel]
    mycursor.execute(sql, val)
    id_p = mycursor.fetchall()
    #print(cur)
    if id_p:
      id_p = id_p[0]
      print(id_p[0])
      if idmat:
        print(idmat)
        for x in range(0, len(idmat)):
          aux = idmat[x]
          aux2 = aux.split(',')
          aux3 = int(aux2[0])
          aux2 = int(aux2[1])
          print((aux2))
          print((aux3))
          mycursor = mydb.cursor()
          sql = "SELECT * FROM matxpro WHERE id_materia = %s and id_curso = %s"
          val = [aux2, aux3]
          mycursor.execute(sql, val)
          comp_m = mycursor.fetchall()
          if comp_m:
            comp_m = comp_m[0]
            print(comp_m)
            if comp_m[2] != 0:
              band = 4
              print("ya tiene profesor")
            if comp_m[2] == 0:
              sql = "UPDATE matxpro SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
              val = (id_p[0], aux2, aux3)
              mycursor.execute(sql, val)
              mydb.commit()
              # Asigna el profesor a los alumnos
              sql = "UPDATE matxalum SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
              val = (id_p[0], aux2, aux3)
              mycursor.execute(sql, val)
              mydb.commit()
              # Asigna el profesor al horario
              sql = "UPDATE horarios SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
              val = (id_p[0], aux2, aux3)
              mycursor.execute(sql, val)
              mydb.commit()
              # Comprueba si cargo un trabajo
              sql = "SELECT id_trabajo, id_materia FROM trabajos WHERE id_profesor = %s and id_materia = %s and id_curso = %s"
              val = [0, aux2, aux3]
              mycursor.execute(sql, val)
              trabajos = mycursor.fetchall()
              if trabajos:
                for x in range(0, len(trabajos)):
                  aux = trabajos[x]
                  id_t = aux[0]
                  sql = "UPDATE trabajos SET id_profesor = %s WHERE id_trabajo = %s"
                  val = (id, id_t)
                  mycursor.execute(sql, val)
                  mydb.commit()
              print("el profesor fue dado de baja")
              band = 1
          else:
            print(aux2, id_p, aux3, fecha)
            mycursor.execute(
              'INSERT INTO matxpro (id_materia, id_profesor, id_curso, fecha) VALUES (%s, %s, %s, %s)',
              (aux2, id_p[0], aux3, fecha))
            mydb.commit()
            band = 1
            print(band)
            print("se le asigna")
            # Asigna el profesor a los alumnos
            sql = "UPDATE matxalum SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
            val = ( id_p[0], aux2, aux3)
            mycursor.execute(sql, val)
            mydb.commit()
            # Asigna el profesor al horario
            sql = "UPDATE horarios SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
            val = (id_p[0], aux2, aux3)
            mycursor.execute(sql, val)
            mydb.commit()
        return redirect(url_for('inscribirprof'))
      else:
        band = 3
        return redirect(url_for('inscribirprof'))
    else:
      band == 3
      return redirect(url_for('inscribirprof'))
  return render_template('inscribirprof2.html', datos = datos, cursos = cursos, materias=idmaterias, bver = bver,
                         soc_p = soc_p, soc_s = soc_s, soc_t = soc_t, con_p=con_p, con_s = con_s, con_t = con_t)


#@app.route('/cargar', methods = ['GET', 'POST']) #ABM Cargar Materias, desabilitado.
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

 #Nav Bar, Boton "Cerrar Sesion"
@app.route('/cerrarsesion')
def cerrarsesion():
  if 'username' in session:
    session.pop('username')
  return redirect(url_for('auth.login'))
##########################################################
#Vistas Genericas - END
##########################################################

@app.route('/asistencia',  methods = ['GET', 'POST']) #Marcar Asistencia por Docente
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

@app.route('/exportardocentesad/<int:id>', methods = ['GET', 'POST'])
def exportardocentesad(id):
  datos = session['username']
  #Datos del curso
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  cursos = cursos[0]
  print(cursos)
  # Saca los profesores
  sql = "SELECT DISTINCT matxpro.id_profesor, nmb_p, ape_p, des_m FROM matxpro, profesores, materias WHERE matxpro.id_curso = %s " \
        "and matxpro.id_profesor = profesores.id_profesor and matxpro.id_materia = materias.id_materia"
  val = [id]
  mycursor.execute(sql, val)
  profe_t = mycursor.fetchall()
  profe_t = sorted(profe_t, key=lambda profe_t: profe_t[2])
  print(profe_t)
  if request.method == 'POST':
    pdf = SimpleDocTemplate(
      "./static/resources/pdfs_creados/{a}{b}_docentes.pdf".format(a=cursos[1], b = cursos[3]),
      pagesize=A4,
      rightMargin=inch,
      leftMargin=inch,
      topMargin=inch,
      bottomMargin=inch / 2
    )
    Story = []
    # Estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    # Cabecera
    text = ''' <strong><font size=14>Docentes </font></strong>
       '''
    text2 = '''
           <strong><font size=10>Diretor/a: {a}, {b}</font></strong>
       '''.format(a=datos[1], b=datos[2])
    text3 = '''
           <strong><font size=10>Curso: {a}, {b}</font></strong>
       '''.format(a=cursos[1], b=cursos[3])
    # Adjuntamos los titulos declarados mas arriba, osea las cabeceras
    Story.append(Paragraph(text2))
    Story.append(Paragraph(text3))
    Story.append(Paragraph(text, styles['Center']))
    Story.append(Spacer(1, 20))
    data = [(
      Paragraph('<strong><font size=6>#</font></strong>', styles['Center']),
      Paragraph('<strong><font size=6>Nombre y Apellido</font></strong>', styles['Center']),
      Paragraph('<strong><font size=6>Disciplina a su cargo</font></strong>', styles['Center'])
    )]
    # Aqui acomplamos los registros o datos a nuestra tabla data, estos seran los datos mostrados de bajo de los headers
    for x in range(0, len(profe_t)):
      aux = profe_t[x]
      count = str(x + 1)
      docente = aux[1] + "," + aux[2]
      materia = aux[3]
      data.append((
        Paragraph('<font size=6>%s</font>' % count, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % docente, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % materia, styles['Normal'])
      ))
    # Declaramamos que la tabla recibira como dato los datos anteriores y le damos la dimensiones a cada uno de nuestros campos
    table = Table(
       data,
      colWidths=[20, 140, 140]
    )
    table.setStyle(
      TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
      ])
    )
    Story.append(table)
    pdf.build(Story)
    # Comprueba si existe el archivo y lo descarga para el usuario
    ruta = pathlib.Path('./static/resources/pdfs_creados')
    filename = "{a}{b}_docentes.pdf".format(a=cursos[1], b = cursos[3])
    archivo = ruta / filename  # Si existe un pdf con su nombre
    print(archivo)
    if archivo.exists():
      return send_file(archivo, as_attachment=True)
  return redirect(url_for('listadodocentes', id=id))
@app.route('/asignarprofe', methods = ['POST', 'GET']) #Listado de Alumnos admin  #falta swa
def asignarprofe():
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT id_profesor, nmb_p, ape_p, ci_p FROM profesores"
  val = []
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  data = sorted(data, key=lambda data: data[2])
  print(data)
  estado = 3
  if request.method == 'POST':
    estado = request.form.get("estado")
    estado = int(estado)
    print(estado)
    if estado == 1 or estado == 0:
      mycursor = mydb.cursor()
      sql = "SELECT id_profesor, nmb_p, ape_p, ci_p FROM profesores WHERE estado = %s"
      val = [estado]
      mycursor.execute(sql, val)
      data = mycursor.fetchall()
      data = sorted(data, key=lambda data: data[2])
      print(data)
      return render_template('asignarprofe.html', datos=datos, data=data, estado = estado)
    else:
      return redirect(url_for('asignarprofe'))

  return render_template('asignarprofe.html', datos=datos, data = data, estado = estado)

@app.route('/asignarmaterias/<int:id>', methods = ['POST', 'GET']) #falta swa
def asignarmaterias(id):
  global user_datos
  user_datos = id
  global band
  datos = session['username']
  if band == 1:
    flash("","bien")
    band = 0
  if band == 4:
    flash("","mal")
    band = 0
  mycursor = mydb.cursor()
  sql = "SELECT id_profesor, nmb_p, ape_p, ci_p FROM profesores WHERE id_profesor = %s"
  val = [id]
  mycursor.execute(sql, val)
  profesor = mycursor.fetchall()
  profesor = profesor[0]
  print(profesor)
  sql = "SELECT matxpro.id_materia, des_m, des_c, des_e, matxpro.id_curso FROM matxpro, materias, cursos, enfasis WHERE id_profesor = %s " \
        "and matxpro.id_materia = materias.id_materia and matxpro.id_curso = cursos.id_curso and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  print(materias)
  fecha = datetime.now()
  fecha = datetime.strftime(fecha, '%Y')
  print(fecha)
  mycursor = mydb.cursor(buffered=True)
  for x in range(1, 7):
    #print(x)
    if x <= 3:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 1]
      mycursor.execute(sql, val)
      if x == 1:
        con_p = mycursor.fetchall()
        #print(con_p)
      if x == 2:
        con_s = mycursor.fetchall()
        #print(con_s)
    if x == 3:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 2]
      mycursor.execute(sql, val)
      soc_p = mycursor.fetchall()
      #print(soc_p)
    if x == 4:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 1]
      mycursor.execute(sql, val)
      con_t = mycursor.fetchall()
      #print(con_t)
    if x > 4:
      sql = "SELECT matxcur.id_curso, materias.id_materia, des_m FROM matxcur, materias WHERE id_curso = %s and id_enfasis = %s and " \
            "materias.id_materia = matxcur.id_materia"
      val = [x, 2]
      mycursor.execute(sql, val)
      if x == 5:
        soc_s = mycursor.fetchall()
        #print(soc_s)
      if x == 6:
        soc_t = mycursor.fetchall()
        #print(soc_t)
  if request.method == "POST":
    idmat = request.form.getlist(('idmat')) #Aca si tengo los id de las materias en q se insc
    print(idmat)
    if idmat:
      for x in range(0, len(idmat)):
        aux = idmat[x]
        aux2 = aux.split(',')
        aux3 = int(aux2[0])
        aux2 = int(aux2[1])
        print((aux2))
        print((aux3))
        mycursor = mydb.cursor()
        sql = "SELECT * FROM matxpro WHERE id_materia = %s and id_curso = %s"
        val = [aux2, aux3]
        mycursor.execute(sql, val)
        comp_m = mycursor.fetchall()
        print(comp_m)
        if comp_m:
            comp_m = comp_m[0]
            print(comp_m)
            if comp_m[2] != 0:
              band = 4
              print("ya tiene profesor")
            if comp_m[2] == 0:
              sql = "UPDATE matxpro SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
              val = (id,aux2, aux3)
              mycursor.execute(sql, val)
              mydb.commit()
              # Asigna el profesor a los alumnos
              sql = "UPDATE matxalum SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
              val = (id, aux2, aux3)
              mycursor.execute(sql, val)
              mydb.commit()
              # Asigna el profesor al horario
              sql = "UPDATE horarios SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
              val = (id, aux2, aux3)
              mycursor.execute(sql, val)
              mydb.commit()
              #Comprueba si cargo un trabajo
              sql = "SELECT id_trabajo, id_materia FROM trabajos WHERE id_profesor = %s and id_materia = %s and id_curso = %s"
              val = [0, aux2,aux3]
              mycursor.execute(sql, val)
              trabajos = mycursor.fetchall()
              print(trabajos)
              if trabajos:
                for x in range(0, len(trabajos)):
                  aux = trabajos[x]
                  id_t = aux[0]
                  sql = "UPDATE trabajos SET id_profesor = %s WHERE id_trabajo = %s"
                  val = (id, id_t)
                  mycursor.execute(sql, val)
                  mydb.commit()
              print("se asigno, el profesor anterior fue dado de baja")
        else:
          mycursor.execute(
            'INSERT INTO matxpro (id_materia, id_profesor, id_curso, fecha) VALUES (%s, %s, %s, %s)',
            (aux2, id, aux3, fecha))
          mydb.commit()
          band = 1
          print(band)
          print("se le asigna")
          #Asigna el profesor a los alumnos
          sql = "UPDATE matxalum SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
          val = (id, aux2, aux3)
          mycursor.execute(sql, val)
          mydb.commit()
          # Asigna el profesor al horario
          sql = "UPDATE horarios SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
          val = (id, aux2, aux3)
          mycursor.execute(sql, val)
          mydb.commit()
    #En caso que el profe este de baja, lo pone activo
    sql = "UPDATE profesores SET estado = %s WHERE id_profesor = %s"
    val = (1, id)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('asignarmaterias', id=id))
  return render_template('asginarmaterias.html', datos=datos, profesor = profesor,
                         soc_p = soc_p, soc_s = soc_s, soc_t = soc_t, con_p=con_p, con_s = con_s, con_t = con_t, materias = materias)

@app.route('/dardebajaprofe/<int:id>', methods = ['POST', 'GET']) #Se debe guardar en el log,  #falta swa
def dardebajaprofe(id):
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT id_profesor, nmb_p, ape_p, ci_p FROM profesores WHERE id_profesor = %s"
  val = [id]
  mycursor.execute(sql, val)
  profesor = mycursor.fetchall()
  profesor = profesor[0]
  print(profesor)
  sql = "SELECT matxpro.id_materia, des_m, des_c, des_e, matxpro.id_curso FROM matxpro, materias, cursos, enfasis WHERE id_profesor = %s " \
        "and matxpro.id_materia = materias.id_materia and matxpro.id_curso = cursos.id_curso and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  print(materias)
  fecha = datetime.now()
  fecha = datetime.strftime(fecha, '%Y')
  print(fecha)
  if request.method == "POST":
    sql = "SELECT id_trabajo, id_materia FROM trabajos WHERE id_profesor = %s"
    val = [id]
    mycursor.execute(sql, val)
    trabajos = mycursor.fetchall()
    if materias:
      for x in range(0, len(materias)):
        aux = materias[x]
        id_m = aux[0]
        id_c = aux[4]
        #Da de baja en materia x profesor
        sql = "UPDATE matxpro SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
        val = (0, id_m, id_c)
        mycursor.execute(sql, val)
        mydb.commit()
        # Da de baja en profesor a los alumnos
        sql = "UPDATE matxalum SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
        val = (0, id_m, id_c)
        mycursor.execute(sql, val)
        mydb.commit()
        # Da de baja al profesor en horario
        sql = "UPDATE horarios SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
        val = (0, id_m, id_c)
        mycursor.execute(sql, val)
        mydb.commit()
    if trabajos:
      print(trabajos)
      for x in range(0, len(trabajos)):
        aux = trabajos[x]
        id_t = aux[0]
        sql = "UPDATE trabajos SET id_profesor = %s WHERE id_trabajo = %s"
        val = (0, id_t)
        mycursor.execute(sql, val)
        mydb.commit()
    sql = "UPDATE profesores SET estado = %s WHERE id_profesor = %s"
    val = (0, id)
    mycursor.execute(sql, val)
    mydb.commit()
    # Auditoria
    inf = datetime.now()
    # Extraemos la fecha
    fecha = datetime.strftime(inf, '%Y/%m/%d')
    mycursor = mydb.cursor()
    mycursor.execute(
      'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
      (datos[0], "Dió de baja al docente {a}, {b} del sistema".format(a=profesor[1], b=profesor[2]), fecha))
    mydb.commit()
    return redirect(url_for('asignarprofe'))
  return render_template('dardebajaprofe.html', datos=datos, profesor = profesor, materias = materias)

@app.route('/eliminarmatxpro/<string:id>') #falta swa
def eliminarmatxpro(id):
  print(id)
  global user_datos
  print(user_datos)
  aux = id.split('C')
  id_m = aux[0]
  id_c = aux[1]
  mycursor = mydb.cursor()
  # Da de baja en materia x profesor
  sql = "UPDATE matxpro SET id_profesor = %s WHERE id_materia = %s and id_curso = %s and id_profesor = %s"
  val = (0, id_m, id_c, user_datos)
  mycursor.execute(sql, val)
  mydb.commit()
  # Da de baja en profesor a los alumnos
  sql = "UPDATE matxalum SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
  val = (0, id_m, id_c)
  mycursor.execute(sql, val)
  mydb.commit()
  # Da de baja al profesor en horario
  sql = "UPDATE horarios SET id_profesor = %s WHERE id_materia = %s and id_curso = %s"
  val = (0, id_m, id_c)
  mycursor.execute(sql, val)
  mydb.commit()
  #Si tiene trabajos..
  sql = "SELECT id_trabajo, id_materia FROM trabajos WHERE id_materia = %s and id_curso = %s and id_profesor = %s"
  val = [id_m, id_c, user_datos]
  mycursor.execute(sql, val)
  trabajos = mycursor.fetchall()
  print(trabajos)
  if trabajos:
    for x in range(0, len(trabajos)):
      aux = trabajos[x]
      id_t = aux[0]
      sql = "UPDATE trabajos SET id_profesor = %s WHERE id_trabajo = %s"
      val = (0, id_t)
      mycursor.execute(sql, val)
      mydb.commit()
  return redirect(url_for('asignarmaterias', id = user_datos))


@app.route('/controlplanillas', methods = ['POST', 'GET'])
def controldeplanilla():
  datos = session['username']
  #Planillas pendientes
  mycursor = mydb.cursor()
  sql = "SELECT * FROM planillas WHERE estado = %s LIMIT 45"
  val = [0]
  mycursor.execute(sql, val)
  pp = mycursor.fetchall()
  print(pp)
  # Planillas aprobadas
  mycursor = mydb.cursor()
  sql = "SELECT * FROM planillas WHERE estado = %s LIMIT 45"
  val = [1]
  mycursor.execute(sql, val)
  pa = mycursor.fetchall()
  # Planillas desaprobadas
  mycursor = mydb.cursor()
  sql = "SELECT * FROM planillas WHERE estado = %s LIMIT 45"
  val = [2]
  mycursor.execute(sql, val)
  pd = mycursor.fetchall()
  if request.method == "POST":
    filtro = int(request.form.get("idfiltro"))
    print(filtro)
    if filtro == 1:
      return redirect(url_for('controldeplanilla'))
    else:
      return render_template('controlplanillas.html', datos=datos, planillas_a=pa, planillas=pp, planillas_d=pd,
                             filtro=filtro)
  return render_template('controlplanillas.html', datos=datos, planillas_a = pa, planillas = pp, planillas_d = pd, filtro = 1)

@app.route('/descargarplanilla/<int:id>')
def descargarplanilla(id):
  datos = session['username']
  print(id)
  ruta = pathlib.Path('./media/')
  mycursor = mydb.cursor()
  sql = "SELECT id_planillas, filename FROM planillas WHERE id_planillas = %s"
  val = [id]
  mycursor.execute(sql, val)
  p = mycursor.fetchall()
  planilla = p[0]
  print(planilla)
  filename = planilla[1]
  archivo = ruta / filename  # Si existe un docx con su nombre
  print(archivo)
  if archivo.exists():
    print("El arhivo existe")
    return send_file(archivo, as_attachment=True)
  else:
    print("No existe")
  return redirect(url_for('controldeplanilla'))

@app.route('/aprobarplanilla/<int:id>')
def aprobarplanilla(id):
  datos = session['username']
  inf = datetime.now()
  # Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  mycursor = mydb.cursor()
  sql = "UPDATE planillas SET estado = %s, fecha_r = %s WHERE id_planillas = %s"
  val = (1,fecha, id)
  mycursor.execute(sql, val)
  mydb.commit()
  print("aprobado")
  # Auditoria
  sql = "SELECT id_planillas, des_p FROM planillas WHERE id_planillas = %s"
  val = [id]
  mycursor.execute(sql, val)
  p = mycursor.fetchall()
  planilla = p[0]
  inf = datetime.now()
  # Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  mycursor = mydb.cursor()
  mycursor.execute(
    'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
    (datos[0], "Aprobó la planilla: {a}".format(a= planilla[1]), fecha))
  mydb.commit()
  return redirect(url_for('controldeplanilla'))

@app.route('/desaprobarplanilla/<int:id>')
def desaprobarplanilla(id):
  datos = session['username']
  inf = datetime.now()
  # Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  mycursor = mydb.cursor()
  sql = "UPDATE planillas SET estado = %s, fecha_r = %s WHERE id_planillas = %s"
  val = (2,fecha, id)
  mycursor.execute(sql, val)
  mydb.commit()
  # Auditoria
  sql = "SELECT id_planillas, des_p FROM planillas WHERE id_planillas = %s"
  val = [id]
  mycursor.execute(sql, val)
  p = mycursor.fetchall()
  planilla = p[0]
  inf = datetime.now()
  # Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  mycursor = mydb.cursor()
  mycursor.execute(
    'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
    (datos[0], "Desaprobó la planilla: {a}".format(a=planilla[1]), fecha))
  mydb.commit()
  print("desaprobado")
  return redirect(url_for('controldeplanilla'))

@app.route('/generarcuotas', methods = ['POST', 'GET'])
def generarcuotas():
  #Alertas
  global band
  if band == 2:
    flash("","nod")
    band = 0
  if band == 3:
    flash("","ya")
    band = 0
  if band == 4:
    flash("", "ya2")
    band = 0
  if band == 1:
    flash("","ok")
    band = 0
  if band == 7:
    flash("", "del")
    band = 0
  datos = session['username']
  #El mes
  mes = datetime.today().month
  print(mes)
  inf = datetime.now()
  # Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  #Cuotas existentes
  mycursor = mydb.cursor()
  sql = "SELECT DISTINCT fecha, id_tipoc, mes, des_c, monto FROM cuotas ORDER BY cuotas.id_cuota DESC"
  val = []
  mycursor.execute(sql, val)
  cuotas = mycursor.fetchall()
  print(cuotas)
  if request.method == "POST":
    idcuota = int(request.form.get("idcuota"))
    monto = request.form.get("monto")
    print(monto)
    if idcuota == 2:
      desc = request.form.get("desc")
      # Comprueba que no halla generado una cuota de instituto aun
      sql = "SELECT DISTINCT fecha, id_tipoc, mes, des_c, monto FROM cuotas WHERE mes = %s and id_tipoc = %s and des_c = %s"
      val = [mes, idcuota,desc]
      mycursor.execute(sql, val)
      compc = mycursor.fetchall()
      if not desc:
        band = 2
        return redirect(url_for('generarcuotas'))
      if compc:
        band = 4
        return redirect(url_for('generarcuotas'))
    else:
      desc = ""
      # Comprueba que no halla generado una cuota de instituto aun
      sql = "SELECT DISTINCT fecha, id_tipoc, mes, des_c, monto FROM cuotas WHERE mes = %s and id_tipoc = %s"
      val = [mes, idcuota]
      mycursor.execute(sql, val)
      compc = mycursor.fetchall()
      if compc:
        band = 3
        print("ya generaste una cuota de instituto este mes")
        return redirect(url_for('generarcuotas'))
    print(idcuota, desc)
    #Quitamos los cursos existentes
    mycursor = mydb.cursor()
    sql = "SELECT id_curso, id_enfasis FROM cursos"
    val = []
    mycursor.execute(sql, val)
    cursos = mycursor.fetchall()
    for x in range(0, len(cursos)):
      aux = cursos[x]
      print(aux)
      mycursor = mydb.cursor()
      sql = "SELECT DISTINCT id_alumno, id_curso FROM matxalum WHERE id_curso = %s"
      val = [aux[0]]
      mycursor.execute(sql, val)
      alumnos = mycursor.fetchall()
      print(alumnos)
      if alumnos:
        for i in range(0, len(alumnos)):
          alumno = alumnos[i]
          print(alumno)
          mycursor.execute(
            'INSERT INTO cuotas (estado, fecha, id_tipoc, id_alumno, mes, des_c, monto) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (0, fecha, idcuota, alumno[0], mes, desc, monto))
          mydb.commit()
    band = 1
    # Auditoria
    inf = datetime.now()
    # Extraemos la fecha
    fecha = datetime.strftime(inf, '%Y/%m/%d')
    mycursor = mydb.cursor()
    if idcuota == 1:
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0], "Generó una nueva cuota del instituto", fecha))
      mydb.commit()
    else:
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0], "Generó una nueva cuota extraordinaria", fecha))
      mydb.commit()
    return redirect(url_for('generarcuotas'))
  return render_template('generarcuotas.html', datos=datos, cuotas = cuotas)

#Eliminar cuotas
@app.route('/eliminarcuota/<string:id>', methods = ['POST', 'GET'])
def eliminarcuotas(id):
  global band
  print(id)
  x = id.split("I")
  print(x)
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT * FROM cuotas WHERE fecha = %s and des_c = %s LIMIT 1"
  val = [x[0], x[1]]
  mycursor.execute(sql, val)
  cuota = mycursor.fetchall()
  cuota = cuota[0]
  print(cuota)
  if request.method == "POST":
    print("eliminar")
    mycursor = mydb.cursor()
    sql = "DELETE FROM cuotas WHERE fecha = %s and des_c = %s and id_tipoc = %s"
    val = [x[0], x[1], cuota[3]]
    mycursor.execute(sql, val)
    mydb.commit()
    band = 7
    # Auditoria
    inf = datetime.now()
    # Extraemos la fecha
    fecha = datetime.strftime(inf, '%Y/%m/%d')
    mycursor = mydb.cursor()
    if int(cuota[3]) == 1:
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0], "Eliminó una cuota del instituto", fecha))
      mydb.commit()
    else:
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0], "Eliminó una cuota extraordinaria", fecha))
      mydb.commit()
    return redirect(url_for('generarcuotas'))
  return render_template('eliminarcuota.html', datos=datos, cuota = cuota)

@app.route('/cuotapagada/<int:id>', methods = ['POST', 'GET'])
def marcarpagado(id):
  datos = session['username']
  print(id)
  global band
  mycursor = mydb.cursor()
  sql = "SELECT id_cuota, id_alumno, id_tipoc FROM cuotas WHERE id_cuota = %s"
  val = [id]
  mycursor.execute(sql, val)
  cuotas = mycursor.fetchall()
  cuotas = cuotas[0]
  print(cuotas)
  #Marca como pagado
  mycursor = mydb.cursor()
  sql = "UPDATE cuotas SET estado = %s WHERE id_cuota = %s"
  val = (1,id)
  mycursor.execute(sql, val)
  mydb.commit()
  print("pagaado")
  band = 1
  # Auditoria
  inf = datetime.now()
  # Extraemos la fecha
  fecha = datetime.strftime(inf, '%Y/%m/%d')
  mycursor = mydb.cursor()
  sql = "SELECT nmb_a, ape_a FROM alumnos WHERE id_alumno = %s"
  val = [cuotas[1]]
  mycursor.execute(sql, val)
  alumno = mycursor.fetchall()
  alumno = alumno[0]
  if int(cuotas[2]) == 1:
    mycursor.execute(
      'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
      (datos[0], "Marcó como pagado una cuota del instituto al alumno {a}, {b}".format(a=alumno[0], b=alumno[1]), fecha))
    mydb.commit()
  else:
    mycursor.execute(
      'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
      (datos[0], "Marcó como pagado una cuota extraordinaria al alumno {a}, {b}".format(a=alumno[0], b=alumno[1]), fecha))
    mydb.commit()
  return redirect(url_for('vercuotasdelalumno', id=cuotas[1]))
#Ver log
@app.route('/verlog', methods = ['POST', 'GET'])
def verlog():
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT log.id_user, nmb_ad, ape_ad, fecha, accion FROM log, admin WHERE admin.id_admin = log.id_user ORDER BY log.id_log DESC LIMIT 60"
  val = []
  mycursor.execute(sql, val)
  registros = mycursor.fetchall()
  print(registros)
  if request.method == "POST":
    filtro = int(request.form.get("idfiltro"))
    print(filtro)
    if filtro == 2:
      print("a")
      mycursor = mydb.cursor()
      sql = "SELECT log.id_user, nmb_ad, ape_ad, fecha, accion FROM log, admin WHERE admin.id_admin = log.id_user ORDER BY log.id_log DESC LIMIT 10"
      val = []
      mycursor.execute(sql, val)
      registros = mycursor.fetchall()
      print(registros)
      return render_template('verlog.html', datos=datos, registros=registros, filtro = filtro)
    if filtro == 3:
      mycursor = mydb.cursor()
      sql = "SELECT log.id_user, nmb_ad, ape_ad, fecha, accion FROM log, admin WHERE admin.id_admin = log.id_user ORDER BY log.id_log DESC LIMIT 20"
      val = []
      mycursor.execute(sql, val)
      registros = mycursor.fetchall()
      return render_template('verlog.html', datos=datos, registros=registros, filtro = filtro)
    if filtro == 1:
      return redirect(url_for('verlog'))
  return render_template('verlog.html', datos=datos, registros=registros, filtro = 1)

def createpassword(password):
  return generate_password_hash(password)

def conv_b(foto):
  with open(foto, 'rb') as f:
    blob= f.read()
  return blob

def guar_f(id_u,foto):
  with open('media/foto_{}.png'.format(id_u), 'wb') as f:
    f.write(foto)

#Archivos permitidos para documentos de inscripcion de alumnos o docentes
def archpermi(filename):
  filename = filename.split('.')
  if filename[len(filename) - 1] in ext_p:
    return True
  return False
if __name__=='__main__':
    app.run(debug = True, port= 8000)