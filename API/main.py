from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
import psycopg2

app = Flask(__name__)
CORS(app)


# CORS(app, origins='http://localhost:8080')

def set_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="meteo",
        user='alice',
        password='alice')
    return conn


conn = set_db_connection()
# Open a cursor to perform database operations
db = conn.cursor()


# Database tables init
# db.execute('DROP TABLE IF EXISTS measurements;')

@app.route("/get_all_sensors", methods=['GET'])
def get_all_sensors():
    conn = set_db_connection()
    db = conn.cursor()
    db.execute('SELECT * FROM sensors;')
    sensors = db.fetchall()
    return sensors


@app.route("/get_sensor/<id>", methods=['GET'])
def get_sensor(id):
    conn = set_db_connection()
    db = conn.cursor()
    sql = "SELECT * FROM sensors where id = %s;" % (str(id))
    db.execute(sql)
    sensor_data = db.fetchall()
    return sensor_data


@app.route("/create_sensor", methods=['POST'])
def create_sensor():
    data = request.get_json()
    conn = set_db_connection()
    db = conn.cursor()
    # db.execute('DROP TABLE sensors cascade;')
    db.execute('CREATE TABLE IF NOT EXISTS sensors (id serial PRIMARY KEY,'
               'name varchar(50) NOT NULL,'
               'latitude float NOT NULL,'
               'longitude float NOT NULL)'
               )

    db.execute('INSERT INTO sensors (name, latitude, longitude)'
               'VALUES (%s, %s, %s)',
               (data['name'],
                data['latitude'],
                data['longitude']
                ))
    conn.commit()
    return {'message': 'sensor added'}, 200


@app.route("/update_sensor/<id>", methods=['PUT'])
def update_sensor(id):
    data = request.get_json()
    conn = set_db_connection()
    db = conn.cursor()
    # db.execute('DROP TABLE sensors cascade;')
    db.execute('CREATE TABLE IF NOT EXISTS sensors (id serial PRIMARY KEY,'
               'name varchar(50) NOT NULL,'
               'latitude float NOT NULL,'
               'longitude float NOT NULL)'
               )

    db.execute('INSERT INTO sensors (name, latitude, longitude)'
               'VALUES (%s, %s, %s)',
               (data['name'],
                data['latitude'],
                data['longitude']
                ))
    conn.commit()
    return {'message': 'sensor added'}, 200


@app.route("/get_all_measures", methods=['GET'])
def get_all_measures():
    conn = set_db_connection()
    db = conn.cursor()
    db.execute('SELECT * FROM measurements;')
    measurements = db.fetchall()
    return measurements


@app.route("/get_sensor_measure/<sensor_id>", methods=['GET'])
def get_sensor_measure(sensor_id):
    conn = set_db_connection()
    db = conn.cursor()
    sql = "SELECT * FROM measurements where sensor_id = %s;" % (str(sensor_id))
    db.execute(sql)
    measure_data = db.fetchall()
    return measure_data


@app.route("/measure", methods=['POST'])
def create_measurements():
    data = request.get_json()
    conn = set_db_connection()
    db = conn.cursor()
    # db.execute('DROP TABLE IF EXISTS measurements;')

    db.execute('CREATE TABLE IF NOT EXISTS measurements (id serial PRIMARY KEY,'
               'temperature float NOT NULL,'
               'humidity float NOT NULL,'
               'date timestamp NOT NULL,'
               'sensor_id integer REFERENCES sensors (id))'
               )

    # date = datetime.today().strftime("%m/%d/%Y - %H:%M")
    date = datetime.today()

    db.execute('INSERT INTO measurements (temperature, humidity, sensor_id, date)'
               'VALUES (%s, %s, %s, %s)',
               (data['temperature'],
                data['humidity'],
                data['sensor_id'],
                date))
    conn.commit()
    return {'message': 'measurements added' + date.strftime("%m/%d/%Y - %H:%M")}, 200

# db.close()
# conn.close()
