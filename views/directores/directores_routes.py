#Blueprint libreria para vistas basandome en modulos
from flask import Blueprint
#Flask imports
from flask import url_for, redirect, render_template, request, session, flash, current_app, send_file
#SQL
import mysql.connector
#Date time
from datetime import datetime
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
#System
import pathlib
import os
#extensiones permitidas
ext_p = set(["pdf"])
#Seguridad
from werkzeug.utils import secure_filename
directores_views = Blueprint('directores', __name__, template_folder='templates')
#Variables globales que ya no me anime a cambiar :c
global cur
global enf
global sec
global ci
global tel
global tipoins
global idmaterias
#Conexion a SQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)

#Vista main, listado de cursos
@directores_views.route('/listadocursos') 
def listadocursos():
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
  print(cursos_s)
  return render_template('listadocursos.html', datos=datos, cursos_c = cursos_c, cursos_s= cursos_s)

#Listado de alumnos del curso
@directores_views.route('/listadoalumnos/<int:id>', methods = ['POST', 'GET'])
def listadoalumnos(id):
  current_app.config['tipoins'] = 1
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  print(cursos)
  sql = "SELECT id_matxcur, matxcur.id_curso, matxcur.id_materia, des_m, car_h FROM matxcur, materias WHERE matxcur.id_curso = %s and matxcur.id_materia = materias.id_materia "
  val = [id]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  materias = sorted(materias, key=lambda materias: materias[3])
  print(materias)
  sql = "SELECT DISTINCT matxalum.id_alumno, nmb_a, ape_a FROM matxalum, alumnos WHERE matxalum.id_curso = %s and matxalum.id_alumno = alumnos.id_alumno"
  val = [id]
  mycursor.execute(sql, val)
  alum_t = mycursor.fetchall()
  alum_t = sorted(alum_t, key=lambda alum_t: alum_t[2])
  print(alum_t)
  current_app.config['band'] = id
  filtro = 0
  materia = []
  if request.method == 'POST':
    filtro = 1
    idmat = request.form.get("idmat")
    print(idmat)
    idmat = int(idmat)
    if idmat > 6: #Comprueba que no marque todos los alumnos
      sql = "SELECT DISTINCT matxalum.id_alumno, nmb_a, ape_a FROM matxalum, alumnos WHERE matxalum.id_curso = %s and matxalum.id_materia = %s and matxalum.id_alumno = alumnos.id_alumno "
      val = [id, idmat]
      mycursor.execute(sql, val)
      alum_t = mycursor.fetchall()
      alum_t = sorted(alum_t, key=lambda alum_t: alum_t[2])
      print(alum_t)
      sql = "SELECT des_m FROM materias WHERE id_materia = %s"
      val = [idmat]
      mycursor.execute(sql, val)
      materia = mycursor.fetchall()
      materia = materia[0]
    else:
      sql = "SELECT DISTINCT matxalum.id_alumno, nmb_a, ape_a FROM matxalum, alumnos WHERE matxalum.id_curso = %s and matxalum.id_alumno = alumnos.id_alumno"
      val = [id]
      mycursor.execute(sql, val)
      alum_t = mycursor.fetchall()
      alum_t = sorted(alum_t, key=lambda alum_t: alum_t[2])
      print(alum_t)
      filtro = 0
  return render_template('listadoalumnosad.html', datos=datos, cursos = cursos[0], materias = materias, alum_t = alum_t, filtro = filtro, materia = materia)

#Ver o modificar datos del alumno
@directores_views.route('/moddatos/<int:id>', methods = ['POST', 'GET']) 
def moddatos(id):
  if not current_app.config['tipoins']:
    return redirect(url_for('directores.listadocursos'))
  if current_app.config['band'] == 3:
    flash("", "ok")
    current_app.config['band'] = 0
  if current_app.config['band'] == 8:
    flash("", "nod")
    current_app.config['band'] = 0
  user = userform.User(request.form)
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT * FROM alumnos WHERE id_alumno = %s"
  val = [id]
  mycursor.execute(sql, val)
  data = mycursor.fetchall()
  #print(tipoins)
  if data:
    data = data[0]
    print(data)
    current_app.config['idcurso'] = 0
  if not data:
    sql = "SELECT * FROM profesores WHERE id_profesor = %s"
    val = [id]
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    data = data[0]
    print(data)
    if not data:
      return redirect(url_for('directores.listadocursos'))
  if request.method == 'POST':
    edad = request.form.get("edad")
    loca = request.form.get("loc")
    barr = request.form.get("bar")
    nume = request.form.get("num")
    emai = request.form.get("ema")
    nomt = request.form.get("nmt")
    numt = request.form.get("nut")
    print(edad)
    print(loca)
    print(barr)
    print(nume)
    print(emai)
    print(nomt)
    print(numt)
    if nomt and numt:
      print("mod alumno")
      sql = "UPDATE alumnos SET edad = %s, loc_a = %s, bar_a = %s, tel_a = %s, email = %s, nmb_tu = %s, tel_tu =%s" \
            " WHERE id_alumno = %s"
      val = (edad,loca,barr,nume,emai,nomt, numt, id)
      mycursor.execute(sql, val)
      mydb.commit()
      band = 3
      #Auditoria
      inf = datetime.now()
      # Extraemos la fecha
      fecha = datetime.strftime(inf, '%Y/%m/%d')
      mycursor = mydb.cursor()
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0],"Modificó los datos del alumno {a}, {b}".format(a= data[1], b=data[2]), fecha))
      mydb.commit()
      return redirect(url_for('directores.moddatos', id = id))
    else:
      print("mod profe")
      sql = "UPDATE profesores SET edad = %s, loc_p = %s, bar_p = %s, tel_p = %s, email = %s WHERE id_profesor = %s"
      val = (edad, loca, barr, nume, emai, id)
      mycursor.execute(sql, val)
      mydb.commit()
      band = 3
      # Auditoria
      inf = datetime.now()
      # Extraemos la fecha
      fecha = datetime.strftime(inf, '%Y/%m/%d')
      mycursor = mydb.cursor()
      mycursor.execute(
        'INSERT INTO log (id_user, accion, fecha) VALUES (%s, %s, %s)',
        (datos[0], "Modificó los datos del docente {a}, {b}".format(a=data[1], b=data[2]), fecha))
      mydb.commit()
      return redirect(url_for('directores.moddatos', id=id))
  return render_template('moddatosal.html', datos=datos, data = data, band=current_app.config['band'], user = user, tipo = current_app.config['tipoins'], id = current_app.config['idcurso'], id2 = id)

#Ver estado academico del alumno
@directores_views.route('/estado/<int:id>', methods = ['POST', 'GET'])
def verestado(id):
  datos = session['username']
  print(id)
  #Saca el idcurso
  mycursor = mydb.cursor()
  sql = "SELECT id_alumno, id_curso, nmb_a, ape_a FROM alumnos WHERE id_alumno = %s"
  val = [id]
  mycursor.execute(sql, val)
  idcurso = mycursor.fetchall()
  idcurso = idcurso[0]
  print(idcurso[1])
  #Puntaje total en primera etapa
  sql = "SELECT id_alumno, matxalum.id_materia, des_m, cal, id_curso, pun_ac, ano_m, id_profesor FROM matxalum, materias WHERE id_alumno = %s and id_curso = %s and matxalum.id_materia = materias.id_materia"
  val = [id, idcurso[1]]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  print(materias)
  puntos_t = []
  estado_a = []
  total = 0
  for x in range(0, len(materias)): #Busca trabajos asociados a la materia en segunda etapa
    aux = materias[x]
    #print(aux)
    sql = "SELECT id_materia, pun_t FROM trabajos WHERE id_materia = %s and id_curso = %s and etapa = %s"
    val = [aux[1], idcurso[1], 1]
    mycursor.execute(sql, val)
    trabajos = mycursor.fetchall()
    if trabajos:
      #print(trabajos)
      for x in range(0, len(trabajos)): #puntaje total por materia
        aux2 = trabajos[x]
        aux3 = int(aux2[1])
        total = total + aux3
      puntos_t.append(total)
      total = 0
    else:
      puntos_t.append(trabajos)
  print(puntos_t)
  for x in range(0, len(materias)): #Calcula el estado en la materia
    aux = materias[x]
    aux2 = puntos_t[x]
    if aux2:
      estado = (70 * aux2) / 100 #Calcula el 70% del total
      if aux[5] >= estado:
        estado = "bien"
        #print(estado)
        estado_a.append(estado)
      else:
        estado = "mal"
        #print(estado)
        estado_a.append(estado)
    else:
      estado = "bien"
      estado_a.append(estado)
  print(estado_a)
  # Puntaje total en segunda etapa
  sql = "SELECT id_alumno, matxalum.id_materia, des_m, cal2, id_curso, pun_ac2, ano_m, id_profesor FROM matxalum, materias WHERE id_alumno = %s and id_curso = %s and matxalum.id_materia = materias.id_materia"
  val = [id, idcurso[1]]
  mycursor.execute(sql, val)
  materias2 = mycursor.fetchall()
  print(materias2)
  puntos_t2 = []
  estado_a2 = []
  total2 = 0
  pre = [] #presentes
  aus = [] #ausentes
  for x in range(0, len(materias2)): #Busca trabajos asociados a la materia en segunda etapa
    aux = materias2[x]
    #print(aux)
    sql = "SELECT id_materia, pun_t FROM trabajos WHERE id_materia = %s and id_curso = %s and etapa = %s"
    val = [aux[1], idcurso[1], 2]
    mycursor.execute(sql, val)
    trabajos2 = mycursor.fetchall()
    # Asistencias
    sql = "SELECT id_alumno, asistio FROM asistenciaalum WHERE id_alumno = %s and id_curso = %s and id_materia = %s"
    val = [id, idcurso[1], aux[1]]
    mycursor.execute(sql, val)
    compa = mycursor.fetchall()
    #print(compa)
    countp = 0
    counta = 0
    if compa:
      for x in range(0, len(compa)):
        a = compa[x]
        print(compa)
        if a[1] == 'P':
          countp += 1
        else:
          counta += 1
        if x == len(compa) - 1:
          pre.append(countp)
          aus.append(counta)
          print(countp, counta)
    else:
      pre.append(countp)
      aus.append(counta)
    if trabajos2:
      #print(trabajos)
      for x in range(0, len(trabajos2)): #puntaje total por materia
        aux2 = trabajos2[x]
        aux3 = int(aux2[1])
        total2 = total2 + aux3
      puntos_t2.append(total2)
      total2 = 0
    else:
      puntos_t2.append(trabajos2)
  print(puntos_t2)
  print(pre, aus)
  for x in range(0, len(materias2)): #Calcula el estado en la materia
    aux = materias2[x]
    aux2 = puntos_t2[x]
    if aux2:
      estado = (70 * aux2) / 100 #Calcula el 70% del total

      if aux[5] >= estado:
        estado = "bien"
        #print(estado)
        estado_a2.append(estado)
      else:
        estado = "mal"
        #print(estado)
        estado_a2.append(estado)
    else:
      estado = "bien"
      estado_a2.append(estado)
  print(estado_a2)
  estado_a3 = []
  #Calcula el estado del alumno en su asistencia por materia
  for x in range(0, len(materias2)):
    aux = aus[x]
    aux2 = pre[x]
    total = aux + aux2
    if total > 0:
      print(total)
      estado = (60 * total) / 100
      print(estado)
      if aux2 >= estado:
        estado = "bien"
        estado_a3.append(estado)
      else:
        estado = "mal"
        estado_a3.append(estado)
    else:
      estado = "bien"
      estado_a3.append(estado)
  print(estado_a3)
  if request.method == 'POST':
    filtro = int(request.form.get("idfiltro"))
    print(filtro)
    if filtro == 1:
      return render_template('verestadoadmin.html', datos=datos, materias=materias, puntos_t=puntos_t,
                             estado_a=estado_a, materias2=materias2, puntos_t2=puntos_t2, estado_a2=estado_a2, presentes=pre,
                             ausencias=aus, estado_a3=estado_a3, data=idcurso, filtro=1)
    if filtro == 2:
      return render_template('verestadoadmin.html', datos=datos, materias=materias, puntos_t=puntos_t,
                             estado_a=estado_a, materias2=materias2, puntos_t2=puntos_t2, estado_a2=estado_a2,
                             presentes=pre,
                             ausencias=aus, estado_a3=estado_a3, data=idcurso, filtro=2)
    if filtro == 3:
      return render_template('verestadoadmin.html', datos=datos, materias=materias, puntos_t=puntos_t,
                             estado_a=estado_a, materias2=materias2, puntos_t2=puntos_t2, estado_a2=estado_a2,
                             presentes=pre,
                             ausencias=aus, estado_a3=estado_a3, data=idcurso, filtro=3)
    if filtro == 4:
      return redirect(url_for('directores.verestado', id=id))
  return render_template('verestadoadmin.html', datos=datos, materias = materias, puntos_t = puntos_t, estado_a=estado_a,
                         materias2 = materias2, puntos_t2 = puntos_t2, estado_a2 = estado_a2, presentes = pre, ausencias = aus,
                         estado_a3 = estado_a3, data = idcurso, filtro = 4)

#Exportar listado de alumnos del curso en PDF
@directores_views.route('/exportaralumnosad/<int:id>', methods = ['GET', 'POST'])
def exportaralumnosad(id):
  datos = session['username']
  # Datos del curso
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  cursos = cursos[0]
  print(cursos)
  #Saca los alumnos
  sql = "SELECT DISTINCT matxalum.id_alumno, nmb_a, ape_a, ci_a, edad FROM matxalum, alumnos WHERE matxalum.id_curso = %s and matxalum.id_alumno = alumnos.id_alumno"
  val = [id]
  mycursor.execute(sql, val)
  alum_t = mycursor.fetchall()
  alum_t = sorted(alum_t, key=lambda alum_t: alum_t[2])
  if request.method == 'POST':
    pdf = SimpleDocTemplate(
      "./static/resources/pdfs_creados/{a}{b}_alumnos.pdf".format(a=cursos[1], b=cursos[3]),
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
    text = ''' <strong><font size=14>Alumnos matriculados</font></strong>
          '''
    text2 = '''
              <strong><font size=10>Director/a: {a}, {b}</font></strong>
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
      Paragraph('<strong><font size=6>Numero de Cedula</font></strong>', styles['Center']),
      Paragraph('<strong><font size=6>Edad</font></strong>', styles['Center'])
    )]
    # Aqui acomplamos los registros o datos a nuestra tabla data, estos seran los datos mostrados de bajo de los headers
    for x in range(0, len(alum_t)):
      aux = alum_t[x]
      count = str(x + 1)
      alumno = aux[1] + ", " + aux[2]
      ci = aux[3]
      edad = aux[4]
      data.append((
        Paragraph('<font size=6>%s</font>' % count, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % alumno, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % ci, styles['Normal']),
        Paragraph('<font size=6>%s</font>' % edad, styles['Normal']),
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
    ruta = pathlib.Path('./static/resources/pdfs_creados')
    filename = "{a}{b}_alumnos.pdf".format(a=cursos[1], b=cursos[3])
    archivo = ruta / filename  # Si existe un pdf con su nombre
    print(archivo)
    if archivo.exists():
      return send_file(archivo, as_attachment=True)
  return redirect(url_for('directores.listadoalumnos', id=id))

#Listado de docentes del curso
@directores_views.route('/listadodocentes/<int:id>', methods = ['POST', 'GET'])
def listadodocentes(id):
  current_app.config['tipoins'] = 2
  datos = session['username']
  current_app.config['idcurso'] = id
  #Datos del curso
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  cursos = cursos[0]
  print(cursos)
  #Saca las materias del curso
  sql = "SELECT id_matxcur, matxcur.id_curso, matxcur.id_materia, des_m, car_h FROM matxcur, materias WHERE matxcur.id_curso = %s and matxcur.id_materia = materias.id_materia "
  val = [id]
  mycursor.execute(sql, val)
  materias = mycursor.fetchall()
  materias = sorted(materias, key=lambda materias: materias[3])
  print(materias)
  #Saca los profesores
  sql = "SELECT DISTINCT matxpro.id_profesor, nmb_p, ape_p, des_m FROM matxpro, profesores, materias WHERE matxpro.id_curso = %s " \
        "and matxpro.id_profesor = profesores.id_profesor and matxpro.id_materia = materias.id_materia"
  val = [id]
  mycursor.execute(sql, val)
  profe_t = mycursor.fetchall()
  profe_t = sorted(profe_t, key=lambda profe_t: profe_t[2])
  print(profe_t)
  materia = []
  filtro = 0
  if request.method == 'POST':
    idmat = request.form.get("idmat")
    print(idmat)
    idmat = int(idmat)
    filtro = 1
    if idmat > 6: #Comprueba que no marque todos los docentes
      sql = "SELECT DISTINCT matxpro.id_profesor, nmb_p, ape_p, des_m FROM matxpro, profesores, materias WHERE matxpro.id_curso = %s and matxpro.id_materia = %s " \
            "and matxpro.id_profesor = profesores.id_profesor and matxpro.id_materia = materias.id_materia "
      val = [id, idmat]
      mycursor.execute(sql, val)
      profe_t = mycursor.fetchall()
      profe_t = sorted(profe_t, key=lambda profe_t: profe_t[2])
      print(profe_t)
      if profe_t:
        materia = profe_t[0]
      else:
        flash("","nop")
        return redirect(url_for('directores.listadodocentes', id=id))
  return render_template('listadodocentesad.html', datos=datos, cursos = cursos, materias = materias, profesores = profe_t, materia = materia, filtro = filtro)

#Ver asistencia del docente
@directores_views.route('/verasisad/<int:id>', methods = ['POST', 'GET'])
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
      return redirect(url_for('directores.verasisad', id=id))
  return render_template('verasisad.html', datos=datos, asistencias=asistencias, profe = profe, filtro = 1, dt = dt, dp = dp, dr = dr)

#Exportar aasistencia del docente
@directores_views.route('/exportasistenciaad/<string:id>', methods = ['GET', 'POST'])
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
  return redirect(url_for('directores.verasisad', id=id))

#Ver cuotas del curso seleccionado
@directores_views.route('/vercuotasad/<int:id>', methods = ['POST', 'GET'])
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

#Ver cuotas de cada alumno
@directores_views.route('/vercuotasdelalumno/<int:id>', methods = ['POST', 'GET'])
def vercuotasdelalumno(id):
  datos = session['username']
  #alertas
  if current_app.config['band'] == 1:
    flash("ok","ok")
    current_app.config['band']
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

#Pestaña de horario de clases
@directores_views.route('/crearseman') 
def crearsemana():
  if current_app.config['band'] == 6:
    flash("","si")
    current_app.config['band'] =0
  if current_app.config['band'] == 3:
    flash("","eliminado")
    current_app.config['band'] = 0
  if current_app.config['band'] == 4:
    flash("", "noh")
    current_app.config['band'] = 0
  if current_app.config['band'] == 5:
    flash("", "yae")
    current_app.config['band'] = 0
  if current_app.config['band'] != 0:
    current_app.config['band'] = 0
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

#Crear horario de la semana del curso seleccionado
@directores_views.route('/cargar2/<int:id>' , methods = ['GET', 'POST'])
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
  create = True
  #print(band)
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
    current_app.config['band']  = 5
    return redirect(url_for('directores.crearsemana'))
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
            (id, aux, current_app.config['band'] + 1, aux2, aux3, aux4))
          mydb.commit()
        else:
          mycursor = mydb.cursor()
          mycursor.execute(
            'INSERT INTO horarios (id_curso, id_materia, id_dia, hora_i, hora_f, id_profesor) VALUES (%s, %s ,%s, %s, %s, %s)',
            (id, aux, current_app.config['band'] + 1, aux2, aux3, 0))
          mydb.commit()
      current_app.config['band']  += 1
      if current_app.config['band'] == 1:
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
      if current_app.config['band'] == 6:
        return redirect(url_for('directores.crearsemana'))
  return render_template('crear_dias.html', datos=datos, cursos=cursos[0], materias=materias, band= current_app.config['band'])

@directores_views.route('/editarhorario/<string:id>' , methods = ['GET', 'POST'])
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

@directores_views.route('/eliminarhorario/<int:id>' , methods = ['GET', 'POST'])
def eliminarhora(id):
  datos = session['username']
  mycursor = mydb.cursor()
  sql = "SELECT id_curso, des_c, sec_c, des_e FROM cursos, enfasis WHERE cursos.id_curso = %s and cursos.id_enfasis = enfasis.id_enfasis"
  val = [id]
  mycursor.execute(sql, val)
  cursos = mycursor.fetchall()
  mycursor = mydb.cursor()
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
    current_app.config['band'] = 3
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
    return redirect(url_for('directores.crearsemana'))
  return render_template('eliminarhorario.html', cursos=cursos[0], datos=datos, h_lu=h_lu, h_ma=h_ma, h_mi=h_mi, h_ju=h_ju, h_vi=h_vi, h_sa=h_sa)

#Inscripcion de alumnos. Parte de la Carga
@directores_views.route('/inscribiral', methods = ['GET', 'POST'])
def inscribirdir():
  alumno = userform.Alumno(request.form)
  datos = session['username']
  global tipoins
  tipoins = 1 #Alumnos
  print(current_app.config['band'])
  if current_app.config['band'] == 1:
    flash("", "si")
    current_app.config['band'] = 0
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
        cedu.save(os.path.join(os.path.abspath("./static/resources/documentos/"), filename))
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
        ante.save(os.path.join(os.path.abspath("./static/resources/documentos/"), filename))
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
        auto.save(os.path.join(os.path.abspath("./static/resources/documentos/"), filename))
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
        ficha.save(os.path.join(os.path.abspath("./static/resources/documentos/"), filename))
        flash("", "")  # Ya guarda el archivo
      else:
        print("archivo no permitido")
      mycursor = mydb.cursor()
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
        return redirect(url_for('directores.sacarmat'))
    else:
      print("no fehca")
      flash("fecha","fecha")
  return render_template('inscribiral.html', datos = datos, alumno = alumno)

#Archivos permitidos para documentos de inscripcion de alumnos o docentes
def archpermi(filename):
  filename = filename.split('.')
  if filename[len(filename) - 1] in ext_p:
    return True
  return False

#Parte de Inscripcion de Alumnos, saca las materias con nombre y ID.
@directores_views.route('/sacarmat', methods = ['GET', 'POST']) 
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
    return redirect(url_for('directores.inscurmat'))
  
#Parte de inscripcion, carga de materias por alumno
@directores_views.route('/inscribiralum', methods = ['GET', 'POST']) 
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
      return redirect(url_for('directores.inscribirdir'))
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
      current_app.config['band'] = 1
      print("a")
      return redirect(url_for('directores.inscribirdir'))
    else:
      print("a")
      return redirect(url_for('directores.inscribirdir'))
  return render_template('inscribiral2.html', datos = datos, materias=idmaterias, bver = bver)

