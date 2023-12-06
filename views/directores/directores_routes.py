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

directores_views = Blueprint('directores', __name__, template_folder='templates')

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
  return render_template('moddatosal.html', datos=datos, data = data, band=current_app.config['band'], user = user, tipo = current_app.config['tipoins'], id = idcurso, id2 = id)

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