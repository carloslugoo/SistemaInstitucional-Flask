from flask import Blueprint
from flask import url_for, redirect, render_template, request, session, flash, current_app
import mysql.connector

profesores_views = Blueprint('profesores', __name__, template_folder='templates')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto"
)

@profesores_views.before_request
def before_request():
    #Si no estas autenticado, fuera
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Acceder a la variable global desde la aplicación
    band = current_app.config['band']
    if band == 7:
        flash("","noclases")
        current_app.config['band'] = 0
    if band == 6:
        flash("","si")
        current_app.config['band'] = 0
    if band == 5:
        flash("", "ya")
        current_app.config['band'] = 0

@profesores_views.route('/miscursos') #Listar las materias que tiene por curso el prof
def miscursos():
  datos = session['username']
  print(datos)
  mycursor = mydb.cursor()
  sql = "SELECT id_mxp, matxpro.id_materia, matxpro.id_profesor, matxpro.id_curso, des_m, des_c, des_e, fecha" \
        " FROM matxpro, materias, cursos, enfasis WHERE id_profesor = %s and matxpro.id_materia = materias.id_materia " \
        "and matxpro.id_curso = cursos.id_curso and cursos.id_enfasis = enfasis.id_enfasis "
  val = [datos[0]]
  mycursor.execute(sql, val)
  mat = mycursor.fetchall()
  print(mat)
  global band

  return render_template('miscursos.html', datos = datos, materias = mat)