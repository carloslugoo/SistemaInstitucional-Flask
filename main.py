from flask import Flask, url_for, redirect, render_template, request, session, send_file
import mysql.connector
from flask import flash
from config import DevConfig
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import userform
from datetime import datetime
import string
import random
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)

app.config.from_object(DevConfig)


folder = os.path.abspath("./media/")
ext_p = set(["doc", "docx", "pdf"])
app.config['folder'] = folder

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)
global bcurso
bcurso =0
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
#@app.before_request
def antes():
  # Verificar si existe una sesion o no, en algun punto de acceso
  datos = session['username']
  print(datos)
  if 'datos' not in session and request.endpoint in ['bienvenidoalumno', 'bienvenidoadmin', 'bienvenidoprofe', 'proceso']:
    print("sin")
    return redirect(url_for('login'))
  if 'datos' in session and request.endpoint in ['login', 'registro']:
    print("con")
    return redirect(url_for('bienvenidoalumno'))


@app.route('/bienvenidoprofe')
def bienvenidoprofe():
  datos = session['username']
  print(datos)
  return render_template('profesorview.html', datos = datos)

@app.route('/bienvenidoalumno')
def bienvenidoalumno():
  datos = session['username']
  print("estoy en def")
  print(datos)
  return render_template('materias.html', datos = datos)

@app.route('/bienvenidoadmin')
def bienvenidoadmin():
  datos = session['username']
  print(datos)
  return render_template('directorview.html', datos = datos)


@app.route('/', methods = ['GET', 'POST']) #Login, funciona pero falta ver el bug de la alerta de inicio de sesion
def login():
  user = userform.User(request.form)
  username = user.username.data
  password = user.password.data
  t_u = 0
  #print(username)
  if request.method == 'POST':
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM user WHERE username = %(username)s', {'username': username})
    data = mycursor.fetchall()
    if data:
      userdata = data[0]
      #print(userdata)
      if userdata:
        passcheck = userdata[3]
        #print(passcheck)
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
          #flash("Correcto", "success")
          time.sleep(1)
          return redirect(url_for('vermaterias'))
        if userdata[4] == 2:
          sql = "SELECT * FROM profesores WHERE id_user = %s"
          val = [userdata[0]]
          mycursor.execute(sql, val)
          data = mycursor.fetchall()
          datos = data[0]
          session['username'] = datos
          #flash("Correcto", "success")
          return redirect(url_for('bienvenidoprofe'))
        if userdata[4] == 3:
          sql = "SELECT * FROM admin WHERE id_user = %s"
          val = [userdata[0]]
          mycursor.execute(sql, val)
          data = mycursor.fetchall()
          datos = data[0]
          session['username'] = datos
          #flash("Correcto", "success")
          return redirect(url_for('bienvenidoadmin'))
      else:
        flash("Contra", "error_p")
    else:
      flash("Not found", "error_n")

  return render_template('login.html', user = user)

@app.route('/registro', methods = ['GET', 'POST']) #Registro, falta ver username cambiar por cedula ❌
def registro():
  user = userform.User(request.form)
  #pasw = user.password.data
  if request.method == 'POST' and user.validate():
    password = createpassword(user.password.data)
    mycursor = mydb.cursor()
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

    if data:
      print("a")
      data = data[0]
      print(data)
      if data[6]:
        create = False
        flash("Ya tiene cuenta", "existe_ci")
        print("test")
    else:
        create = False
        flash("Error", "ci_e")
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
        aux = aux[0]
        print(aux)
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
        flash("Correcto", "success")
        # return redirect(url_for('login'))
      else:
        print("e")
        flash("Error", "psw")
  return render_template('register.html', user = user)

@app.route('/recuperar', methods = ['GET', 'POST']) #Recuperar cuenta ❌
def recuperar():
  user = userform.User(request.form)
  return render_template('recuperar.html', user=user)

#Parte de Proceso de Alumnos, Carga de trabajos
@app.route('/proceso', methods = ['GET', 'POST']) #Procesos ✔
def proceso():
  global bcurso
  global balumno
  datos = session['username']
  #print(datos)
  mycursor = mydb.cursor()
  sql = "SELECT * FROM matxpro WHERE id_profesor = %s"
  val = [datos[0]]
  mycursor.execute(sql, val)
  profe = mycursor.fetchall()
  #print(profe) #ID, Id Materia, Id profe, Carga horaria, Id curso
  profemat = []
  profemati = []
  cantm = 0
  global cursos
  global alumnos
  for x in range(0, len(profe)):
    #print(x)
    aux = profe[x]
    sql = "SELECT * FROM materias WHERE id_materia = %s"
    val = [aux[1]]
    mycursor.execute(sql, val)
    aux = mycursor.fetchall()
    aux = aux[0]
    #print(aux)
    #print(x)
    if x == 0:
      profemat.append(aux)
      #print(profemat)
      cantm += 1
      #print(x)
      #print(cantm)
    elif profemat[x-cantm-1] != aux:
      #print(cantm)
      cantm += 1
      profemat.append(aux)
      #print(profemat)
  #print(profemat)
  task = userform.Task(request.form)
  if request.method == 'POST' and task.validate(): #ID prof = datos[0],
    tipo_t = request.form.get(('tipo_t'))
    idalumnos = request.form.getlist(('idalum'))
    puntalum = request.form.getlist(('punt_a'))
    global idmaterias
    global idcurso
    #print(idalumnos)
    #print(puntalum)
    #print(tipo_t)
    #print(task.nombre.data)
    #print(task.puntaje.data)
    fecha = datetime.now()
    fecha = datetime.strftime(fecha, '%Y/%m/%d')
    cargar = True
    #print(fecha)
    if idmaterias != 0:
      if idcurso !=0:
        #Comprobar si se cargo bien el form
        for x in range(0, len(idalumnos)):
          aux = idalumnos[x]
          aux2 = 0
          if puntalum[x]:
            aux2 = int(puntalum[x])
          else:
            cargar = False
            print("sin punt")
            flash("puntaje", "pun_e")
          puntajeform = int(task.puntaje.data)
          print("Puntaje")
          #print(aux2)
          #print(aux)
          print("Puntaje form")
          print(task.puntaje.data)
          if aux2 != 0:
            if aux2 > puntajeform:
              cargar = False
              print("si es ma")
            if aux2 > puntajeform:
              flash("puntajem", "pun_m")
          else:
            flash("puntajem", "no_p")
        if cargar == True:
          for x in range(0, len(idalumnos)):
            aux = idalumnos[x]
            aux2 = int(puntalum[x])
            if x ==0:
              clavet = crearclavet()
              print(clavet)
              #Ingresa el trabajo
              mycursor.execute(
                'INSERT INTO trabajos (fec_t, des_t, pun_t, id_profesor, id_materia, tipo_t, clave_t) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (fecha, task.nombre.data, task.puntaje.data, datos[0], idmaterias, tipo_t, clavet))
              mydb.commit()
              #Saca el id del trabajo
              sql = "SELECT id_trabajo FROM trabajos WHERE id_materia = %s and id_profesor = %s and fec_t = %s and des_t= %s and pun_t = %s and tipo_t = %s and clave_t = %s"
              val = [idmaterias, datos[0], fecha, task.nombre.data, task.puntaje.data, tipo_t, clavet]
              mycursor.execute(sql, val)
              idtra = mycursor.fetchall()
              idtra = idtra[0]
              mydb.commit()
            #Updatea el puntaje acumulado
            sql = "UPDATE matxalum SET pun_ac = (pun_ac + %s) WHERE id_alumno = %s and id_materia = %s and id_curso = %s"
            val = (aux2, aux, idmaterias, idcurso)
            mycursor.execute(sql, val)
            mydb.commit()
            # Inserta el trabajo al alumno
            mycursor.execute('INSERT INTO traxalum (id_alumno, pun_l, fec_t, id_trabajo) VALUES (%s, %s, %s, %s)',
                             (aux, aux2, fecha, idtra[0]))
            mydb.commit()
            flash("Bien", "car")
            bcurso = 1
      else:
        cargar = False
        flash("Error", "cur")
    else:
      cargar = False
      flash("Error", "mat")


  return render_template('procesotest.html', task = task, datos = datos, materias = profemat,bcurso = bcurso, cursos = cursos,
                         alumnos = alumnos, balumno = balumno )

@app.route('/procesoss', methods = ['POST']) #Parte de procesos, aca quitamos la materia ✔
def procesoss():
  if request.method == 'POST':
    id_mat = request.form.get(('idmat'))
    if id_mat:
      global bcurso
      bcurso = 1
    print(id_mat)
    datos = session['username']
    mycursor = mydb.cursor()
    print(datos[0])
    print(id_mat)
    sql = "SELECT * FROM matxpro WHERE id_profesor = %s and id_materia =%s"
    val = [datos[0], id_mat]
    global idmaterias
    idmaterias = id_mat
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    print("Cursos con esa materia:")
    print(data)
    #print(cursos[0])
    #print(len(cursos))
    global balumno
    global cursos
    cursos = []
    if cursos:
      balumno = 1
    for x in range(0, len(data)):
      print(x)
      aux = data[x]
      mycursor = mydb.cursor()
      sql = "SELECT id_curso, des_c, sec_c,des_e FROM cursos,enfasis WHERE id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
      val = [aux[3]]
      mycursor.execute(sql, val)
      aux = mycursor.fetchall()
      aux = aux[0]
      cursos.append(aux)
    print("Cursos procesados:")
    print(cursos)
  return redirect(url_for('proceso'))

@app.route('/alumnos', methods = ['POST']) #Parte de procesos, quitamos los cursos y los alumnos relacionados con la materia ✔
def alumnosproceso():
  if request.method == 'POST':
    id_curso = request.form.get(('idcurso'))
    datos = session['username']
    global balumno
    balumno = 1
    global cursos
    global idmaterias
    mycursor = mydb.cursor()
    sql = "SELECT alumnos.id_alumno,nmb_a, ape_a FROM alumnos, " \
          "matxalum WHERE matxalum.id_curso =%s and alumnos.id_alumno = matxalum.id_alumno " \
          "and matxalum.id_materia = %s"

    val = [id_curso, idmaterias]
    mycursor.execute(sql, val)
    global idcurso
    idcurso = id_curso
    data = mycursor.fetchall()
    print(id_curso)
    print(idmaterias)
    print("Alumnos con esta materia:")
    print(data)
    global alumnos
    alumnos = data
  return redirect(url_for('proceso'))

#Parte de vista de alumnos materias
@app.route('/materias')
def vermaterias():
  datos = session['username']
  print(datos)
  mycursor = mydb.cursor()
  sql = "SELECT matxalum.id_materia,des_m, des_c, sec_c, ano_m, des_e, id_profesor FROM matxalum, materias, cursos, enfasis" \
        " WHERE id_alumno = %s and cursos.id_curso =%s and matxalum.id_materia = materias.id_materia and cursos.id_enfasis = enfasis.id_enfasis"
  val = [datos[0], datos[4]]
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  cont = [1,2,3,4,5,6,7,8,9,10,11,12]
  return render_template('materias.html', datos=datos, materias=data, cont = cont)

@app.route('/vermateria/<string:id>') #Ver proceso de la materia seleccionada.
def verproceso(id):
  datos = session['username']
  #print(id) #Pimer digito materia, segundo id del profe
  x = [int(a) for a in str(id)]
  #print(x)
  mycursor = mydb.cursor()
  sql = "SELECT trabajos.id_trabajo,des_t, trabajos.fec_t, pun_t, pun_l FROM trabajos, traxalum WHERE trabajos.id_trabajo = traxalum.id_trabajo and id_materia = %s and id_alumno = %s"
  val = [x[0], datos[0]]
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  if data:
    print(data)
    suml = 0
    sumt = 0
    for x in range(0, len(data)):
      aux = data[x]
      pl=aux[4]
      pt=aux[3]
      suml+= pl
      print(suml)
      sumt+= pt
      porcl = int((suml * 100) / sumt)
      print(porcl)
  else:
    flash("no", "nom")
    return redirect(url_for('vermaterias'))
  return render_template('vermateria.html', datos=datos, procesos = data, suml = suml, sumt = sumt, porcl = porcl)

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
      categf = "si"
      mensf(categf)
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

@app.route('/sacarmat', methods = ['GET', 'POST']) #Parte de Inscripcion de Alumnos, saca las materias con nombre y ID.
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
        filename = "constancia_cargos" + alumno.num_c.data + "." + extc[1]
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
        return redirect(url_for('inscmatxprof'))
    else:
      print("no fehca")
      flash("fecha", "fecha")
  return render_template('inscribirprof.html', datos=datos, alumno=alumno, profe = idmaterias)

@app.route('/inscribirprofee', methods = ['GET', 'POST']) #Parte de inscripcion, carga de materias por alumno
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
    sql = "SELECT id_profesor FROM profesores WHERE ci_p = %s and tel_p = %s"
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
          sql = "SELECT profesores.id_profesor, nmb_p, des_m FROM matxpro, profesores, materias WHERE matxpro.id_materia = %s and id_curso = %s and " \
                "matxpro.id_profesor = profesores.id_profesor and matxpro.id_materia = materias.id_materia"
          val = [aux2, aux3]
          mycursor.execute(sql, val)
          comp_m = mycursor.fetchall()
          if comp_m:
            print(comp_m[0])
            band = 4
            idmaterias = comp_m[0]
            return redirect(url_for('inscribirprof'))
          else:
            mycursor.execute(
              'INSERT INTO matxpro (id_materia, id_profesor, id_curso, fecha) VALUES (%s, %s, %s, %s)',
              (aux2, id_p[0], aux3, fecha))
            mydb.commit()
        band = 1
        print(band)
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
@app.route('/misdatos') #Nav Bar, Boton "Mis Datos"
def misdatos():
  datos = session['username']
  print(datos)
  if datos[7] == 1: #alumnos
    return render_template('verdatos.html', datos = datos)
  if datos[6] == 2: #profesores
    return render_template('verdatosprof.html', datos=datos)
  if datos[6] ==3: #Admin
    return render_template('verdatosad.html', datos=datos)

@app.route('/miconfig', methods = ['GET', 'POST']) #Nav Bar, Boton "Configuracion de Cuenta"
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
  if datos[7] == 1:  # alumnos
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE id_user = %s"
    val = [datos[6]]
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
              val = (us,datos[6])
              mycursor.execute(sql, val)
              mydb.commit()
              band = 1
              return redirect(url_for('misconfig'))
            else:
              flash("","psw")
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
    return render_template('miconfig.html', datos=datos, data = data[0], user = user)



def mensf(cat):
  #para testear
  print('a')
  print(cat)
  flash("", cat)
  return flash("", cat)
def createpassword(password):
  return generate_password_hash(password)
def crearclavet(): #Una clave random para el trabajo.
  length = 5
  letters = string.ascii_letters + string.digits
  clave = ''.join(random.choice(letters) for i in range(length))
  return clave
def conv_b(foto):
  with open(foto, 'rb') as f:
    blob= f.read()
  return blob
def guar_f(id_u,foto):
  with open('media/foto_{}.png'.format(id_u), 'wb') as f:
    f.write(foto)
def archpermi(filename):
  filename = filename.split('.')
  print(filename)
  if filename[1] in ext_p:
    return True
  return False

def guardararchivo():

  return
if __name__=='__main__':
    app.run(debug = True, port= 8000)