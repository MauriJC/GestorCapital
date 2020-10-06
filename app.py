from datetime import datetime

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configuracion de la bd
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'capital_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicializacion del objeto db de sqlalchemy

#db.init_app(app)
db = SQLAlchemy(app)

#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

class Empleado(db.Model):

    dni = db.Column(db.Integer)
    legajo = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.Integer)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    domicilio = db.Column(db.String(250))
    fecha_ingreso = db.Column(db.DateTime)
    fecha_salida = db.Column(db.DateTime)
    fecha_nacimiento = db.Column(db.DateTime)
    fecha_cese = db.Column(db.DateTime)
    estado_general = db.Column(db.String(250))
    sexo = db.Column(db.String(250))
    foto = db.Column(db.LargeBinary)

    def __str__(self):
        return (

            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'Domicilio: {self.domicilio}'
            f'Legajo: {self.legajo}'
            f'DNI: {self.dni}'
        )

@app.route('/')
@app.route('/index')
@app.route('/index.html')

def inicio():
    #Listado de empleados
    empleados = Empleado.query.all()
    #personas = Persona.query.order_by('id')
    total_empleados = Empleado.query.count()
    app.logger.debug(f'Listado Empleados: {empleados}')
    app.logger.debug(f'Total Empleados: {total_empleados}')
    return  render_template('index.html', empleados= empleados, total_empleados= total_empleados)

@app.route('/ver/<int:legajo>')
def ver_detalle(legajo):

    #recuperamos la persona segun el id proporcionado
    #persona = Persona.query.get(id)
    empleado = Empleado.query.get_or_404(legajo)
    app.logger.debug(f'Ver Empleado: {empleado}')
    return  render_template('detalle.html', empleado = empleado)