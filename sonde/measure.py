import random
import requests
import time

api = "http://127.0.0.1:5000/measure"

sensor_id = input("Entrez l'identifiant de la sonde à activer : ")
print("")

def main(sensor_id):
    # time.asctime() prints the current date & time in string.
    t_value = round(random.uniform(-5.0, 40.0), 2)
    h_value = round(random.uniform(0.0, 100.0), 2)
    data = {'temperature': t_value,
            'humidity': h_value,
            'sensor_id': sensor_id}
    print('Data: ', data, time.asctime())
    requests.post(api, json=data)

for x in range(5):
    main(sensor_id)
    time.sleep(2)


