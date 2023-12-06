
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


folder = os.path.abspath("./media/")
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


@app.route('/recuperar', methods = ['GET', 'POST']) #Recuperar cuenta ❌
def recuperar():
  user = userform.User(request.form)
  return render_template('recuperar.html', user=user)


@app.route('/inscribiral', methods = ['GET', 'POST']) #Inscripcion de alumnos. Parte de la Carga
def inscribirdir():
  alumno = userform.Alumno(request.form)
  datos = session['username']
  global band
  global tipoins
  tipoins = 1 #Alumnos
  print(band)
  if band == 1:
    flash("", "si")
    band = 0
  if request.method == "POST":
    cedu = request.files["cedu"]
    ante = request.files["ante"]
    auto = request.files["auto"]
    ficha = request.files["ficha"]
    fecha = (request.form['fec_n'])
    print(fecha)
    if fecha:
      # Parte Cedula.. Preguntar si conviene hacer funcion o q
      if "cedu" not in request.files:
        #print("No envio nada")
        pass
      elif cedu.filename == "":
        #print("No mando nada")
        pass
      elif cedu and archpermi(cedu.filename):
        filename = secure_filename(cedu.filename)
        extc = filename.split('.')
        #print(extc)
        #print(filename)
        #print(alumno.num_c.data)
        filename = "cedula_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        cedu.save(os.path.join(app.config["folder"], filename))
        flash("", "") #Ya guarda el archivo
      else:
        print("archivo no permitido")
      #Parte Antecedentes
      if "ante" not in request.files:
        #print("No envio nada")
        pass
      elif ante.filename == "":
        #print("No mando nada")
        pass
      elif ante and archpermi(ante.filename):
        filename = secure_filename(ante.filename)
        extc = filename.split('.')
        print(extc)
        print(filename)
        print(alumno.num_c.data)
        filename = "antecedente_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        ante.save(os.path.join(app.config["folder"], filename))
        flash("", "")  # Ya guarda el archivo
      else:
        print("archivo no permitido")
      #Parte Autorizacion de Padres
      if "auto" not in request.files:
        #print("No envio nada")
        pass
      elif auto.filename == "":
        #print("No mando nada")
        pass
      elif auto and archpermi(auto.filename):
        filename = secure_filename(auto.filename)
        extc = filename.split('.')
        print(extc)
        print(filename)
        print(alumno.num_c.data)
        filename = "autorizacion_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        auto.save(os.path.join(app.config["folder"], filename))
        flash("", "")  # Ya guarda el archivo
      else:
        print("archivo no permitido")
      # Parte de ficha medica
      if "ficha" not in request.files:
        # print("No envio nada")
        pass
      elif ficha.filename == "":
        # print("No mando nada")
        pass
      elif ficha and archpermi(ficha.filename):
        filename = secure_filename(ficha.filename)
        extc = filename.split('.')
        print(extc)
        print(filename)
        print(alumno.num_c.data)
        filename = "ficha_" + alumno.num_c.data + "." + extc[1]
        print(filename)
        ficha.save(os.path.join(app.config["folder"], filename))
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
      sql = "SELECT ci_a FROM alumnos WHERE ci_a = %s"
      val = [ci]
      mycursor.execute(sql, val)
      comp_a = mycursor.fetchall()
      if comp_a:
        print(comp_a)
        flash("", "error")
      else:
        # Inserta en tabla alumnnos todos los datos
        mycursor.execute(
          'INSERT INTO alumnos (nmb_a, ape_a, tel_a, ci_a, edad, email, loc_a, nmb_tu, tel_tu, fec_a, bar_a) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
          (alumno.nombre.data, alumno.apellido.data, alumno.num_t.data, alumno.num_c.data, alumno.edad.data,
           alumno.email.data, alumno.localidad.data, alumno.nmb_pa.data, alumno.num_pa.data, fecha, alumno.barrio.data))
        mydb.commit()
        # Auditoria
        inf = datetime.now()
        # Extraemos la fecha
        fecha = datetime.strftime(inf, '%Y/%m/%d')
        mycursor = mydb.cursor()
        mycursor.execute(
          'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
          (datos[0], "Matriculó al alumno {a}, {b} al sistema".format(a=alumno.nombre.data, b=alumno.apellido.data), fecha))
        mydb.commit()
        return redirect(url_for('sacarmat'))
    else:
      print("no fehca")
      flash("fecha","fecha")
  return render_template('inscribiral.html', datos = datos, alumno = alumno)

@app.route('/inscribiral/<filename>') #Parte de buscar el archivo o documento del alumno, falta testear mejor
def getfile(filename):
  return send_file(os.path.join(app.config["folder"], filename))

@app.route('/inscribiralum', methods = ['GET', 'POST']) #Parte de inscripcion, carga de materias por alumno
def inscurmat():
  bver = 0
  datos = session['username']
  global idmaterias #Contiene el nombre de las materias y sus id
  global ci
  global tel
  fecha = datetime.now()
  fecha = datetime.strftime(fecha, '%Y')
  print(fecha)
  print("a")
  if request.method == 'POST':
    print("a")
    if ci == 0 or tel == 0:
      print("a2")
      return redirect(url_for('inscribirdir'))
    idmat = request.form.getlist(('idmat')) #Aca si tengo los id de las materias en q se insc
    mycursor = mydb.cursor()
    sql = "SELECT id_alumno FROM alumnos WHERE ci_a = %s and tel_a = %s"
    val = [ci,tel]
    mycursor.execute(sql, val)
    id_a = mycursor.fetchall()
    id_a = id_a[0]
    print(cur)
    print("q pasa")
    if id_a:
      print(id_a[0])
    if idmaterias:
      print(idmat)
      bver = 1
      for x in range(0, len(idmat)):
        aux = idmat[x]
        #print(aux)
        #print(x)
        sql = "SELECT id_profesor FROM matxpro WHERE id_materia = %s and id_curso = %s"
        val = [aux, cur]
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        if data:
          data = data[0]
          print(id_a[0])
          print(data[0])
          mycursor = mydb.cursor()
          mycursor.execute(
             'INSERT INTO matxalum (id_alumno, id_materia, id_curso, ano_m, id_profesor) VALUES (%s, %s, %s, %s, %s)',
            (id_a[0], aux, cur, fecha, data[0]))
          mydb.commit()
        else:
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO matxalum (id_alumno, id_materia, id_curso, ano_m, id_profesor) VALUES (%s, %s, %s, %s, %s)',
            (id_a[0], aux, cur, fecha, 0))
          mydb.commit()
      print("termino")
      #time.sleep(3.5)
      flash("", "si")
      global band
      band = 1
      print(band)
      print("a")
      return redirect(url_for('inscribirdir'))
    else:
      print("a")
      return redirect(url_for('inscribirdir'))
  return render_template('inscribiral2.html', datos = datos, cursos = cursos, materias=idmaterias, bver = bver)

@app.route('/sacarmat', methods = ['GET', 'POST']) #Va antes que inscurmat #Parte de Inscripcion de Alumnos, saca las materias con nombre y ID.
def sacarmat():
  global cur
  global enf
  global sec
  global ci
  global tel
  global tipoins
  if tipoins == 1: # Osea Alumnos
    if enf == "Sociales":  # Dependiendo del enfasis para no consultar la bd
      enf = 2
    else:
      enf = 1
    print(cur)
    print(enf)
    mycursor = mydb.cursor()
    sql = "SELECT id_curso FROM cursos WHERE des_c = %s and sec_c = %s and id_enfasis = %s"
    val = [cur, sec, enf]
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    if data:
      print(data[0])
      data = data[0]
    #Test
    #print(ci)
    #print(tel)
    # Updatea con el curso asignado
    sql = "UPDATE alumnos SET id_curso = %s WHERE ci_a = %s and tel_a = %s"
    val = (data[0],ci, tel)
    mycursor.execute(sql, val)
    mydb.commit()
    cur = data[0]
    #Sacar los nombres de materia y sus id
    sql = "SELECT matxcur.id_materia, des_m FROM matxcur, materias WHERE matxcur.id_curso = %s and matxcur.id_enfasis = %s " \
          "and matxcur.id_materia = materias.id_materia "
    val = [data[0], enf]
    mycursor.execute(sql, val)
    mat = mycursor.fetchall()
    print(mat)
    bver = 1
    global idmaterias
    idmaterias = mat
    return redirect(url_for('inscurmat'))


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


@app.route('/crearseman') #Creacion de Semana de Clases
def crearsemana():
  global band
  if band == 6:
    flash("","si")
    band =0
  if band == 3:
    flash("","eliminado")
    band = 0
  if band == 4:
    flash("", "noh")
    band = 0
  if band == 5:
    flash("", "yae")
    band = 0
  if band != 0:
    band = 0
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT cursos.id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_enfasis = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [1]
  mycursor.execute(sql, val)
  cursos_c = mycursor.fetchall()
  sql = "SELECT cursos.id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_enfasis = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [2]
  mycursor.execute(sql, val)
  cursos_s = mycursor.fetchall()
  return render_template('crear_sem.html', datos=datos, cursos_c = cursos_c, cursos_s = cursos_s)

@app.route('/cargar/<int:id>' , methods = ['GET', 'POST']) #Sin utilizar
def asignarpof(id):
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  sql = "SELECT id_matxcur, matxcur.id_curso, matxcur.id_materia, des_m, car_h FROM matxcur, materias WHERE matxcur.id_curso = %s and matxcur.id_materia = materias.id_materia "
  val = [id]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  materias = sorted(materias, key=lambda materias: materias[3])
  sql = "SELECT id_materia, id_profesor FROM matxpro WHERE id_curso = %s"
  val = [id]
  mycursor.execute(sql, val)
  profesores = mycursor.fetchall()
  print(cursos)
  print(materias)
  print(profesores)
  create = True
  global band
  if request.method == 'POST':
    dias = request.form.getlist(('dias'))
    hora_i = request.form.getlist(('hora_i'))
    hora_f = request.form.getlist(('hora_f'))
    #Cantidad de dias
    clu = 0
    cma = 0
    cmi = 0
    cju = 0
    cvi = 0
    csa = 0
    for x in range(0, len(dias)):
      aux1 = dias[x]
      aux2 = hora_i[x]
      aux3 = hora_f[x]
      if aux1 and aux2 and aux3:
        hora1 = aux2.split(':')
        hora2 = aux3.split(':')
        print(hora2)
        if len(hora1) == 1:
          aux2 = aux2 + ":00"
        if len(hora2) == 1:
          aux3 = aux3 + ":00"
        print(aux2)
        print(aux3)
        if aux1 == "Lunes":
          clu += 1
        if aux1 == "Martes":
          cma += 1
        if aux1 == "Miercoles":
          cmi += 1
        if aux1 == "Jueves":
          cju += 1
        if aux1 == "Viernes":
          cvi += 1
        if aux1 == "Sabado":
          csa += 1
        if aux2 == aux3:
          flash("","misma")
          print("misma hora")
          create = False
    if clu > 5 or cma > 5 or cmi > 5 or cju > 5 or cvi > 5 or csa > 5: # Comprueba que no se asignen muchas materias a ese dia
      print("dias")
      create = False
    if create == True:
      band += 1
      for x in range(0, len(dias)):
        aux1 = dias[x]
        aux2 = hora_i[x]
        aux3 = hora_f[x]
        if aux1 and aux2 and aux3:
          hora1 = aux2.split(':')
          hora2 = aux3.split(':')
          aux4 = materias[x]
          if len(hora1) == 1:
            aux2 = aux2 + ":00"
          if len(hora2) == 1:
            aux3 = aux3 + ":00"
          if aux1 == "Lunes":
            aux1 = 1
          if aux1 == "Martes":
            aux1 = 2
          if aux1 == "Miercoles":
            aux1 = 3
          if aux1 == "Jueves":
            aux1 = 4
          if aux1 == "Viernes":
            aux1 = 5
          if aux1 == "Sabado":
            aux1 = 6
          print('Datos:')
          print(aux1)
          print(aux2)
          print(aux3)
          print(aux4)
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO horarios (id_curso, id_materia, id_dia, hora_i, hora_f) VALUES (%s, %s ,%s, %s, %s)',
            (id, aux4[2], aux1, aux2, aux3))
          mydb.commit()
    print(band)
    print(dias)
    print(hora_i)
    print(hora_f)
    if band == 6:
      return redirect(url_for('crearsemana'))
  return render_template('crear_dias_mantenimiento.html', datos=datos, cursos = cursos[0], materias = materias, band = band)

@app.route('/cargar2/<int:id>' , methods = ['GET', 'POST'])
def cargarhora(id):
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  sql = "SELECT id_matxcur, matxcur.id_curso, matxcur.id_materia, des_m, car_h FROM matxcur, materias WHERE matxcur.id_curso = %s and matxcur.id_materia = materias.id_materia "
  val = [id]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  materias = sorted(materias, key=lambda materias: materias[3])
  global band
  create = True
  print(band)
  #Comprueba que exista un horario cargado
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
  #En caso que exista no permite crear otro horario
  if h_lu and h_ma and h_mi and h_ju and h_vi and h_sa:
    band = 5
    return redirect(url_for('crearsemana'))
  if request.method == 'POST':
    idmat = request.form.getlist(('idmat'))
    hora_i = request.form.getlist(('hora_i'))
    hora_f = request.form.getlist(('hora_f'))
    print(idmat)
    print(hora_i)
    print(hora_f)
    for x in range(0, len(idmat)):
      aux = idmat[x]
      if not aux:
        create = False
    if create == True:
      for x in range(0, len(idmat)):
        aux = idmat[x]
        aux2 = hora_i[x]
        aux3 = hora_f[x]
        sql = "SELECT id_mxp, id_profesor FROM matxpro WHERE id_materia = %s and id_curso = %s"
        val = [aux, id]
        mycursor.execute(sql, val)
        aux4 = mycursor.fetchall()
        if aux4:
          aux4 = aux4[0]
          aux4 = aux4[1]
          print(aux4)
        if aux4 and aux4 != 0: #Osea que tiene profesor
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO horarios (id_curso, id_materia, id_dia, hora_i, hora_f, id_profesor) VALUES (%s, %s ,%s, %s, %s, %s)',
            (id, aux, band + 1, aux2, aux3, aux4))
          mydb.commit()
        else:
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO horarios (id_curso, id_materia, id_dia, hora_i, hora_f, id_profesor) VALUES (%s, %s ,%s, %s, %s, %s)',
            (id, aux, band + 1, aux2, aux3, 0))
          mydb.commit()
      band += 1
      if band == 1:
        data = cursos[0]
        # Auditoria
        inf = datetime.now()
        # Extraemos la fecha
        fecha = datetime.strftime(inf, '%Y/%m/%d')
        mycursor = mydb.cursor()
        mycursor.execute(
          'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
          (datos[0], "Cargó un nuevo horario al {a}, {b}, {c}".format(a=data[1], b=data[3], c = data[2]), fecha))
        mydb.commit()
      if band == 6:
        return redirect(url_for('crearsemana'))
  return render_template('crear_dias.html', datos=datos, cursos=cursos[0], materias=materias, band=band)

@app.route('/eliminarhorario/<int:id>' , methods = ['GET', 'POST'])
def eliminarhora(id):
  datos = session['username']
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
    if x == 1:  # Lunes
      h_lu = mycursor.fetchall()
      print(h_lu)
    if x == 2:  # Martes
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
  if request.method == 'POST':
    mycursor = mydb.cursor()
    sql = "DELETE FROM horarios WHERE id_curso = %s"
    val = [id]
    mycursor.execute(sql, val)
    mydb.commit()
    band = 3
    # Auditoria
    inf = datetime.now()
    # Extraemos la fecha
    fecha = datetime.strftime(inf, '%Y/%m/%d')
    mycursor = mydb.cursor()
    data = cursos[0]
    mycursor.execute(
      'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
      (datos[0], "Eliminó el horario al {a}, {b}, {c}".format(a=data[1], b=data[3], c=data[2]), fecha))
    mydb.commit()
    return redirect(url_for('crearsemana'))
  return render_template('eliminarhorario.html', cursos=cursos[0], datos=datos, h_lu=h_lu, h_ma=h_ma, h_mi=h_mi, h_ju=h_ju, h_vi=h_vi, h_sa=h_sa)

##########################################################
#Vista genericas - Comparten todos los usuarios
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
      band = 4
      return redirect(url_for('crearsemana'))
  
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

@app.route('/editarhorario/<string:id>' , methods = ['GET', 'POST'])
def editarhorario(id):
  datos = session['username']
  aux = id.split('D')
  id_c = int(aux[0])
  id_d = int(aux[1])
  #print(id_c)
  #print(id_d)
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id_c]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  sql = "SELECT id_horario, des_m FROM horarios, materias WHERE id_curso = %s and id_dia = %s and horarios.id_materia = materias.id_materia ORDER BY horarios.hora_f ASC"
  val = [id_c, id_d]
  mycursor.execute(sql, val)
  horarios = mycursor.fetchall()
  #print(horarios)
  sql = "SELECT id_matxcur, matxcur.id_curso, matxcur.id_materia, des_m, car_h FROM matxcur, materias WHERE matxcur.id_curso = %s and matxcur.id_materia = materias.id_materia "
  val = [id_c]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  materias = sorted(materias, key=lambda materias: materias[3])
  create = True
  if request.method == 'POST':
    idmat = request.form.getlist(('idmat'))
    print(idmat)
    for x in range(0, len(idmat)):
      aux = idmat[x]
      if not aux:
        create = False
    if create == True:
      for x in range(0, len(idmat)):
        aux = idmat[x]
        print(aux)
        sql = "SELECT id_mxp, id_profesor FROM matxpro WHERE id_materia = %s and id_curso = %s"
        val = [aux, id_c]
        mycursor.execute(sql, val)
        aux4 = mycursor.fetchall()
        print(aux4)
        aux5 = horarios[x]
        print(aux5)
        if aux4:
          aux4 = aux4[0]
          aux4 = aux4[1]
          print(aux4)
        if aux4 and aux4 != 0: #Osea que tiene profesor
          mycursor = mydb.cursor()
          aux5 = aux5[0]
          print(aux5)
          print(aux)
          sql = "UPDATE horarios SET id_materia = %s, id_profesor = %s WHERE id_horario = %s"
          val = (aux, aux4, aux5)
          mycursor.execute(sql, val)
          mydb.commit()
        else:
          mycursor = mydb.cursor()
          aux5 = aux5[0]
          print(aux5)
          print(aux)
          sql = "UPDATE horarios SET id_materia = %s, id_profesor = %s WHERE id_horario = %s"
          val = (aux, 0, aux5)
          mycursor.execute(sql, val)
          mydb.commit()
      # Auditoria
      inf = datetime.now()
      # Extraemos la fecha
      fecha = datetime.strftime(inf, '%Y/%m/%d')
      mycursor = mydb.cursor()
      data = cursos[0]
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0], "Editó el horario al {a}, {b}, {c}".format(a=data[1], b=data[3], c=data[2]), fecha))
      mydb.commit()
      return redirect(url_for('verhorarioadmin', id = id_c))
  return render_template('editarhorario.html', datos = datos, cursos=cursos[0], horarios = horarios, materias = materias, band = id_d)
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

@app.route('/verasisad/<int:id>', methods = ['POST', 'GET'])
def verasisad(id):
  #print(id)
  datos = session['username']
  #datos del profe
  mycursor = mydb.cursor()
  sql = "SELECT id_profesor, nmb_p, ape_p FROM profesores WHERE id_profesor = %s"
  val = [id]
  mycursor.execute(sql, val)
  profe = mycursor.fetchall()
  profe = profe[0]
  #print(profe)
  # Sacamos las veces que marco asistencia
  mycursor = mydb.cursor()
  sql = "SELECT hora_e, hora_s, fec_a FROM asistenciaprof WHERE id_profesor = %s ORDER BY asistenciaprof.id_asisprof DESC LIMIT 7"
  val = [id]
  mycursor.execute(sql, val)
  asistencias = mycursor.fetchall()
  #print(asistencias)

  dt = 0  # Dias trabajados
  dp = 0  # Dias no trabajados
  dr = 0  # Dias que no marco salida
  for x in range(0, len(asistencias)):
    aux = asistencias[x]
    if aux[0] or aux[1]:
      dt += 1
    if not aux[0] and not aux[1]:
      dp += 1
    if aux[0] and not aux[1]:
      dr += 1
  #print(dt, dp, dr)
  if request.method == "POST":
    dt = 0
    dp = 0
    dr = 0
    filtro = int(request.form.get("idfiltro"))
    #print(filtro)
    if filtro == 2:
      sql = "SELECT hora_e, hora_s, fec_a FROM asistenciaprof WHERE id_profesor = %s ORDER BY asistenciaprof.id_asisprof DESC LIMIT 31"
      val = [datos[0]]
      mycursor.execute(sql, val)
      asistencias = mycursor.fetchall()
      for x in range(0, len(asistencias)):
        aux = asistencias[x]
        if aux[0] or aux[1]:
          dt += 1
        if not aux[0] and not aux[1]:
          dp += 1
        if aux[0] and not aux[1]:
          dr += 1
      return render_template('verasisad.html', datos=datos, asistencias=asistencias, profe=profe, filtro=filtro, dt=dt, dp=dp, dr=dr)
    if filtro == 3:
      sql = "SELECT hora_e, hora_s, fec_a FROM asistenciaprof WHERE id_profesor = %s ORDER BY asistenciaprof.id_asisprof DESC"
      val = [datos[0]]
      mycursor.execute(sql, val)
      asistencias = mycursor.fetchall()
      for x in range(0 , len(asistencias)):
        aux = asistencias[x]
        if aux[0] or aux[1]:
          dt += 1
        if not aux[0] and not aux[1]:
          dp += 1
        if aux[0] and not aux[1]:
          dr += 1
      return render_template('verasisad.html', datos=datos,asistencias=asistencias, profe=profe, filtro=filtro, dt=dt, dp=dp, dr=dr)
    if filtro == 1:
      return redirect(url_for('verasisad', id=id))
  return render_template('verasisad.html', datos=datos, asistencias=asistencias, profe = profe, filtro = 1, dt = dt, dp = dp, dr = dr)
#Exportar aasistencia del docente
@app.route('/exportasistenciaad/<string:id>', methods = ['GET', 'POST'])
def exportarasistenciaad(id):
  datos = session['username']
  #datos del profe
  mycursor = mydb.cursor()
  sql = "SELECT id_profesor, nmb_p, ape_p FROM profesores WHERE id_profesor = %s"
  val = [id]
  mycursor.execute(sql, val)
  profe = mycursor.fetchall()
  profe = profe[0]
  print(profe)
  if request.method == 'POST':
    pdf = SimpleDocTemplate(
      "./static/resources/pdfs_creados/{a}{b}_asistencia.pdf".format(a=profe[1], b=profe[2]),
      pagesize=A4,
      rightMargin=inch,
      leftMargin=inch,
      topMargin=inch,
      bottomMargin=inch / 2
    )
    filtro = request.form.get("idfiltro")
    print(filtro)
    if filtro == "1":
      # Sacamos las veces que marco asistencia
      mycursor = mydb.cursor()
      sql = "SELECT hora_e, hora_s, fec_a FROM asistenciaprof WHERE id_profesor = %s ORDER BY asistenciaprof.id_asisprof DESC"
      val = [id]
      mycursor.execute(sql, val)
      asistencias = mycursor.fetchall()
      print(asistencias)
    else:
      # Sacamos la asistencia de la fecha
      mycursor = mydb.cursor()
      sql = "SELECT hora_e, hora_s, fec_a FROM asistenciaprof WHERE id_profesor = %s and fec_a = %s ORDER BY asistenciaprof.id_asisprof DESC"
      val = [id, filtro]
      mycursor.execute(sql, val)
      asistencias = mycursor.fetchall()
      print(asistencias)
    Story = []
    # Estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    # Cabecera
    text = ''' <strong><font size=14>Asistencia del Docente</font></strong>
             '''
    text2 = '''
                 <strong><font size=10>Director/a: {a}, {b}</font></strong>
             '''.format(a=datos[1], b=datos[2])
    text3 = '''
                 <strong><font size=10>Docente: {a}, {b}</font></strong>
             '''.format(a=profe[1], b=profe[2])
    # Adjuntamos los titulos declarados mas arriba, osea las cabeceras
    Story.append(Paragraph(text2))
    Story.append(Paragraph(text3))
    Story.append(Paragraph(text, styles['Center']))
    Story.append(Spacer(1, 20))
    data = [(
      Paragraph('<strong><font size=6>#</font></strong>', styles['Center']),
      Paragraph('<strong><font size=6>Fecha</font></strong>', styles['Center']),
      Paragraph('<strong><font size=6>Hora de entrada</font></strong>', styles['Center']),
      Paragraph('<strong><font size=6>Hora de salida</font></strong>', styles['Center'])
    )]
    # Aqui acomplamos los registros o datos a nuestra tabla data, estos seran los datos mostrados de bajo de los headers
    for x in range(0, len(asistencias)):
      aux = asistencias[x]
      count = str(x + 1)
      fecha = aux[2]
      he = aux[0]
      hs = aux[1]
      data.append((
        Paragraph('<font size=6>%s</font>' % count, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % fecha, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % he, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % hs, styles['Normal']),
      ))
    # Declaramamos que la tabla recibira como dato los datos anteriores y le damos la dimensiones a cada uno de nuestros campos
    table = Table(
      data,
      colWidths=[20, 140, 80, 80]
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
    ruta = pathlib.Path('./static/resources/pdfs_creados/')
    filename =  "{a}{b}_asistencia.pdf".format(a=profe[1], b=profe[2])
    archivo = ruta / filename  # Si existe un pdf con su nombre
    print(archivo)
    if archivo.exists():
      return send_file(archivo, as_attachment=True)
  return redirect(url_for('verasisad', id=id))

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

@app.route('/vercuotasad/<int:id>', methods = ['POST', 'GET'])
def vercuotasad(id):
  datos = session['username']
  # Datos del curso
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  print(cursos)
  #Saca los alumnos
  pendiente = []
  sql = "SELECT DISTINCT matxalum.id_alumno, nmb_a, ape_a FROM matxalum, alumnos WHERE matxalum.id_curso = %s and matxalum.id_alumno = alumnos.id_alumno"
  val = [id]
  mycursor.execute(sql, val)
  alum_t = mycursor.fetchall()
  alum_t = sorted(alum_t, key=lambda alum_t: alum_t[2])
  print(alum_t)
  #Cuotas pendientes de cada alumno
  for x in range(0, len(alum_t)):
    alumno = alum_t[x]
    sql = "SELECT id_cuota, mes, id_tipoc FROM cuotas WHERE id_alumno = %s and estado = %s"
    val = [alumno[0], 0]
    mycursor.execute(sql, val)
    cuotas = mycursor.fetchall()
    if cuotas:
      print(cuotas)
      pendiente.append(len(cuotas))
    else:
      p = 0
      pendiente.append(p)
  print(pendiente)
  return render_template('vercuotas.html', datos=datos, cursos= cursos[0], alumnos = alum_t, pendientes = pendiente)

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

#Ver cuotas de cada alumno
@app.route('/vercuotasdelalumno/<int:id>', methods = ['POST', 'GET'])
def vercuotasdelalumno(id):
  datos = session['username']
  #alertas
  global band
  if band == 1:
    flash("ok","ok")
    band = 0
  #Datos del alumno
  mycursor = mydb.cursor()
  sql = "SELECT id_alumno, id_curso, ape_a, nmb_a FROM alumnos WHERE id_alumno = %s"
  val = [id]
  mycursor.execute(sql, val)
  alumno = mycursor.fetchall()
  alumno = alumno[0]
  #Cuotas del alumno
  sql = "SELECT DISTINCT id_cuota,fecha, id_tipoc, mes, des_c, monto FROM cuotas WHERE id_alumno = %s and estado = %s ORDER BY cuotas.id_cuota DESC"
  val = [id, 0]
  mycursor.execute(sql, val)
  cuotas = mycursor.fetchall()
  print(cuotas)
  total = 0
  for x in range(0, len(cuotas)):
    aux = cuotas[x]
    total = total + float(aux[5])
    print(total)
  if request.method == "POST":
    #Cuotas pagadas
    sql = "SELECT DISTINCT id_cuota,fecha, id_tipoc, mes, des_c, monto FROM cuotas WHERE id_alumno = %s and estado = %s ORDER BY cuotas.id_cuota DESC"
    val = [id, 1]
    mycursor.execute(sql, val)
    cuotas = mycursor.fetchall()
    total = 0
    for x in range(0, len(cuotas)):
      aux = cuotas[x]
      total = total + float(aux[5])
      print(total)
    return render_template('vercuotasdelalumno.html', datos=datos, data=alumno, cuotas=cuotas, filtro = 2, total = total)
  return render_template('vercuotasdelalumno.html', datos=datos, data = alumno, cuotas = cuotas, filtro = 1, total = total)

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

#Para documentos de inscripcion de alumnos o docentes
def archpermi(filename):
  filename = filename.split('.')
  if filename[len(filename) - 1] in ext_p:
    return True
  return False

if __name__=='__main__':
    app.run(debug = True, port= 8000)