from flask import Flask, request, jsonify
from flask_restx import Resource, Api, fields
from flask_cors import CORS
from datetime import datetime
import psycopg2

app = Flask(__name__)
api = Api(app, doc="/api")
CORS(app)


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

@api.route("/get_all_sensors", methods=['GET'])
class Sensor(Resource):
    def get(self):
        conn = set_db_connection()
        db = conn.cursor()
        db.execute('SELECT * FROM sensors ORDER BY id;')
        sensors = db.fetchall()
        return sensors


@api.route("/get_sensor/<id>", methods=['GET'])
class Sensor(Resource):
    def get(self, id):
        conn = set_db_connection()
        db = conn.cursor()
        sql = "SELECT * FROM sensors where id = %s ORDER BY id;" % (str(id))
        db.execute(sql)
        sensor_data = db.fetchall()
        return sensor_data


sensor = api.model('SENSOR', {
    'name': fields.String(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
})


@api.route("/create_sensor", methods=['POST'])
@api.expect(sensor)
class Sensor(Resource):
    def post(self):
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


@api.route("/update_sensor/<id>", methods=['PUT'])
@api.expect(sensor)
class Sensor(Resource):
    def put(self, id):
        data = request.get_json()
        conn = set_db_connection()
        db = conn.cursor()
        update_query = '''
            UPDATE sensors
            SET name = %s,
                latitude = %s,
                longitude = %s
            WHERE id = %s
        '''
        db.execute(update_query, (data['name'], data['latitude'], data['longitude'], int(id)))
        conn.commit()
        return {'message': 'sensor updated'}, 200


@api.route("/get_all_measures", methods=['GET'])
class Measure(Resource):
    def get(self):
        conn = set_db_connection()
        db = conn.cursor()
        db.execute('SELECT * FROM measurements ORDER BY id;')
        measurements = db.fetchall()
        res = []
        for measurement in measurements:
            measurement_dict = {
                'id': measurement[0],
                'temperature': measurement[1],
                'humidity': measurement[2],
                'date': measurement[3],
                'sensor_id': measurement[4],
            }
            res.append(measurement_dict)
        return jsonify(res)


@api.route("/get_sensor_measure/<sensor_id>", methods=['GET'])
class Measure(Resource):
    def get(self, sensor_id):
        conn = set_db_connection()
        db = conn.cursor()
        sql = "SELECT * FROM measurements where sensor_id = %s ORDER BY id;" % (str(sensor_id))
        db.execute(sql)
        measure_data = db.fetchall()
        res = []
        for measurement in measure_data:
            measurement_dict = {
                'id': measurement[0],
                'temperature': measurement[1],
                'humidity': measurement[2],
                'date': measurement[3],
                'sensor_id': measurement[4],
            }
            res.append(measurement_dict)
        return jsonify(res)


post_measure = api.model('MEASURE', {
    'temperature': fields.Float(required=True),
    'humidity': fields.Float(required=True),
    'date': fields.DateTime(required=True),
    'sensor_id': fields.Integer(required=True),
})


@api.route("/measure", methods=['POST'])
@api.expect(post_measure)
class Measure(Resource):
    def post(self):
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
        date = datetime.today()
        db.execute('INSERT INTO measurements (temperature, humidity, sensor_id, date)'
                   'VALUES (%s, %s, %s, %s)',
                   (data['temperature'],
                    data['humidity'],
                    data['sensor_id'],
                    date))
        conn.commit()
        return {'message': 'measurements added' + date.strftime("%m/%d/%Y - %H:%M")}, 200


put_measure = api.model('MEASURE', {
    'temperature': fields.Float(required=True),
    'humidity': fields.Float(required=True),
    'sensor_id': fields.Integer(required=True),
})


@api.route("/update_measure/<id>", methods=['PUT'])
@api.expect(put_measure)
class Measure(Resource):
    def put(self, id):
        data = request.get_json()
        conn = set_db_connection()
        db = conn.cursor()
        update_query = '''
            UPDATE measurements
            SET temperature = %s,
                humidity = %s,
                sensor_id = %s
            WHERE id = %s
        '''
        db.execute(update_query, (data['temperature'], data['humidity'], data['sensor_id'], int(id)))
        conn.commit()
        return {'message': 'sensor updated'}, 200

# db.close()
# conn.close()
