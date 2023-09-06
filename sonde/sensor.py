import random
import requests
import time

api = "http://127.0.0.1:5000/create_sensor"
sensor_name = input("Entrez le nom de la sonde à créer : ")
print("")

def main(sensor_name):

    latitude_value = round(random.uniform(-90.0, 90.0), 2)
    longitude_value = round(random.uniform(-180.0, 180.0), 2)
    data = {'name': sensor_name,
            'latitude': latitude_value,
            'longitude': longitude_value,
            }
    print('Data: ', data, time.asctime())
    requests.post(api, json=data)

main(sensor_name)