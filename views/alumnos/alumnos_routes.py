from flask import Blueprint
from flask import url_for, redirect, render_template, request, session, flash, current_app
import mysql.connector

alumnos_views = Blueprint('alumnos', __name__, template_folder='templates')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)

@alumnos_views.before_request
def before_request():
    #Si no estas autenticado, fuera
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Acceder a la variable global desde la aplicación
    band = current_app.config['band']
    
    if band == 6:
        flash("", "noa")
        # Restablecer la variable global en la aplicación
        current_app.config['band'] = 0
        
#Parte de vista de alumnos materias
@alumnos_views.route('/bienvenidoalumno')
def vermaterias():
  datos = session['username']
  print(datos)
  #Materias el cual esta matriculado el alumno
  mycursor = mydb.cursor()
  sql = "SELECT matxalum.id_materia,des_m, des_c, sec_c, ano_m, des_e, id_profesor FROM matxalum, materias, cursos, enfasis" \
        " WHERE id_alumno = %s and cursos.id_curso =%s and matxalum.id_materia = materias.id_materia and cursos.id_enfasis = enfasis.id_enfasis"
  val = [datos[0], datos[4]]
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  print(data)
  return render_template('materias.html', datos=datos, materias=data)

@alumnos_views.route('/vermateria/<string:id>') #Ver proceso de la materia seleccionada.
def verproceso(id):
  datos = session['username']
  #print(id) #Pimer digito materia, segundo id del profe
  x = [int(a) for a in str(id)]
  #print(x)
  #Trabajos primera etapa
  mycursor = mydb.cursor()
  sql = "SELECT trabajos.id_trabajo,des_t, trabajos.fec_t, pun_t, pun_l FROM trabajos, traxalum WHERE trabajos.id_trabajo = traxalum.id_trabajo and id_materia = %s and id_alumno = %s and etapa = %s"
  val = [id, datos[0], 1]
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  print(data)
  #Trabajos segunda etapa
  sql = "SELECT trabajos.id_trabajo,des_t, trabajos.fec_t, pun_t, pun_l FROM trabajos, traxalum WHERE trabajos.id_trabajo = traxalum.id_trabajo and id_materia = %s and id_alumno = %s and etapa = %s"
  val = [id, datos[0], 2]
  mycursor.execute(sql, val)
  data2 = mycursor.fetchall()
  print(data2)
  sql = "SELECT DISTINCT nmb_p, ape_p, des_m FROM profesores, matxalum, materias WHERE matxalum.id_materia = %s and matxalum.id_profesor = profesores.id_profesor " \
        "and matxalum.id_materia = materias.id_materia and matxalum.id_curso = %s"
  val = [id, datos[4]]
  mycursor.execute(sql, val)
  profesor = mycursor.fetchall()
  print(profesor)
  #Sumatoria de el puntaje del alumno
  #Segunda Etapa
  sql = "SELECT cal, cal2 FROM matxalum WHERE id_alumno = %s and id_curso = %s and id_materia = %s"
  val = [datos[0], datos[4], id]
  mycursor.execute(sql, val)
  cal = mycursor.fetchall()
  print(cal)
  suml2 = 0
  sumt2 = 0
  if data2:
    profesor = profesor[0]
    print(profesor)
    for x in range(0, len(data2)):
      aux = data2[x]
      pl = aux[4]
      pt = aux[3]
      suml2 += pl
      # print(suml)
      sumt2 += pt
    print(suml2)
  #Primera etapa
  suml = 0
  sumt = 0
  if data:
    #print(data)
    for x in range(0, len(data)):
      aux = data[x]
      pl=aux[4]
      pt=aux[3]
      suml+= pl
      #print(suml)
      sumt+= pt
  #En caso de no tener proceso tira una alerta y redirige
  else:
    flash("no", "nom")
    return redirect(url_for('alumnos.vermaterias'))
  return render_template('vermateria.html', datos=datos, procesos = data, suml = suml, sumt = sumt, data = profesor, data2 = data2, suml2 = suml2, sumt2 = sumt2,
                         cal = cal[0])

@alumnos_views.route('/vermitrabajo/<int:id>')
def vermitrabajo(id):
  datos = session['username']
  #print(datos)
  print(id)
  #Saca el trabajo
  mycursor = mydb.cursor()
  sql = "SELECT des_t, pun_t, fec_t, id_materia FROM trabajos WHERE trabajos.id_trabajo = %s"
  val = [id]
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  data = data[0]
  print(data)
  #Saca los indicadores
  mycursor = mydb.cursor()
  sql = "SELECT indxalum.id_indicador, des_i, indxalum.id_trabajo, pun_l, pun_i FROM indxalum, indicadores WHERE indxalum.id_trabajo = %s and id_alumno = %s and " \
        "indxalum.id_indicador = indicadores.id_indicador"
  val = [id, datos[0]]
  mycursor.execute(sql, val)
  indi = mycursor.fetchall()
  print(indi)
  return render_template('vermitrabajo.html', datos=datos, data=data, indicadores = indi)

@alumnos_views.route('/verasistenciaal/<int:id>', methods =  ['GET', 'POST'])
def verasistenciaal(id):
  datos = session['username']
  print(datos)
  mycursor = mydb.cursor()
  #Datos de la disciplina
  sql = "SELECT DISTINCT nmb_p, ape_p, des_m FROM profesores, matxalum, materias WHERE matxalum.id_materia = %s and matxalum.id_profesor = profesores.id_profesor " \
        "and matxalum.id_materia = materias.id_materia"
  val = [id]
  mycursor.execute(sql, val)
  profesor = mycursor.fetchall()
  print(profesor)
  #Datos de su asistencia
  sql = "SELECT id_asisalum, fecha, asistio FROM asistenciaalum WHERE id_alumno = %s and id_materia = %s and id_curso = %s ORDER BY asistenciaalum.fecha DESC LIMIT 7"
  val = [datos[0], id, datos[4]]
  mycursor.execute(sql, val)
  asistencias = mycursor.fetchall()
  print(asistencias)
  #Si no tienes asistencias tira alerta y redirige
  if not asistencias:
    current_app.config['band'] = 6
    return redirect(url_for('alumnos.vermaterias'))
  if request.method == "POST":
    #Filtro de tiempo..
    filtro = int(request.form.get("idfiltro"))
    if filtro == 1:
      return redirect(url_for('verasistenciaal', id= id))
    if filtro == 2:
      sql = "SELECT id_asisalum, fecha, asistio FROM asistenciaalum WHERE id_alumno = %s and id_materia = %s and id_curso = %s ORDER BY asistenciaalum.fecha DESC LIMIT 31"
      val = [datos[0], id, datos[4]]
      mycursor.execute(sql, val)
      asistencias = mycursor.fetchall()
      print(asistencias)
      return render_template('verasistenciaal.html', datos=datos, data=profesor[0], asistencias=asistencias, filtro=filtro, id=id)
    if filtro == 3:
      sql = "SELECT id_asisalum, fecha, asistio FROM asistenciaalum WHERE id_alumno = %s and id_materia = %s and id_curso = %s ORDER BY asistenciaalum.fecha DESC"
      val = [datos[0], id, datos[4]]
      mycursor.execute(sql, val)
      asistencias = mycursor.fetchall()
      print(asistencias)
      return render_template('verasistenciaal.html', datos=datos, data=profesor[0], asistencias=asistencias, filtro=filtro, id=id)
  return render_template('verasistenciaal.html', datos=datos, data = profesor[0], asistencias=asistencias, filtro = 1, id = id)

#Mis cuotas
@alumnos_views.route('/miscuotas', methods = ['POST', 'GET'])
def miscuotasal():
  datos = session['username']
  mycursor = mydb.cursor()
  # Cuotas del alumno
  sql = "SELECT DISTINCT id_cuota,fecha, id_tipoc, mes, des_c, monto FROM cuotas WHERE id_alumno = %s and estado = %s ORDER BY cuotas.id_cuota DESC"
  val = [datos[0], 0]
  mycursor.execute(sql, val)
  cuotas = mycursor.fetchall()
  print(cuotas)
  total = 0
  for x in range(0, len(cuotas)):
    aux = cuotas[x]
    total = total + float(aux[5])
    print(total)
  if request.method == "POST":
    filtro = int(request.form.get("idfiltro"))
    if filtro == 1:
      return redirect(url_for('miscuotasal'))
    if filtro == 2:
      sql = "SELECT DISTINCT id_cuota,fecha, id_tipoc, mes, des_c, monto FROM cuotas WHERE id_alumno = %s and estado = %s ORDER BY cuotas.id_cuota DESC"
      val = [datos[0], 1]
      mycursor.execute(sql, val)
      cuotas = mycursor.fetchall()
      print(cuotas)
      total = 0
      for x in range(0, len(cuotas)):
        aux = cuotas[x]
        total = total + float(aux[5])
        print(total)
      return render_template('miscuotas.html', datos=datos, cuotas=cuotas, filtro = filtro, total = total)
  return render_template('miscuotas.html', datos=datos, cuotas = cuotas, filtro = 1, total = total)