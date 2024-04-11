# import time
# from counterfit_connection import CounterFitConnection
# from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
# from counterfit_shims_grove.grove_led import GroveLed
# import paho.mqtt.client as mqtt
# from counterfit_connection import CounterFitConnection

# CounterFitConnection.init('127.0.0.1', 5050)

# light_sensor = GroveLightSensor(0)
# led = GroveLed(5)

# id = 'a30e9830-af2e-4385-b499-d44206cd41e8'

# client_name = id + 'nightlight_client'

# mqtt_client = mqtt.Client(client_name)
# mqtt_client.connect('test.mosquitto.org')

# mqtt_client.loop_start()

# print("MQTT connected!")

# while True:
#     light = light_sensor.light
#     print('Light level:', light)

#     if light < 300:
#         led.on()
#     else:
#         led.off()
    
#     time.sleep(1)


    
# from counterfit_connection import CounterFitConnection
# CounterFitConnection.init('127.0.0.1', 5050)

# import io
# import requests
# from counterfit_shims_picamera import PiCamera

# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.rotation = 0

# image = io.BytesIO()
# camera.capture(image, 'jpeg')
# image.seek(0)

# with open('image.jpg', 'wb') as image_file:
#     image_file.write(image.read())

# prediction_url = 'http://4.144.162.217/image' #The Public IP address of the virtual machine in on Azure portal: 13.76.179.94
# headers = {
#     'Content-Type' : 'application/octet-stream'
# }
# image.seek(0)
# response = requests.post(prediction_url, headers=headers, data=image)
# results = response.json()

# #print (results)
# for prediction in results['predictions']:
#     print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')



# import time
# from counterfit_connection import CounterFitConnection
# from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
# from counterfit_shims_grove.grove_led import GroveLed
# import paho.mqtt.client as mqtt
# import json

# CounterFitConnection.init('127.0.0.1', 5050)

# light_sensor = GroveLightSensor(0)
# led = GroveLed(5)

# id = 'a30e9830-af2e-4385-b499-d44206cd41e8'

# client_telemetry_topic = id + '/telemetry'
# client_name = id + 'nightlight_client'

# mqtt_client = mqtt.Client(client_name)
# mqtt_client.connect('test.mosquitto.org')

# mqtt_client.loop_start()

# print("MQTT connected!")

# while True:
#     light = light_sensor.light
#     telemetry = json.dumps({'light' : light})

#     print("Sending telemetry ", telemetry)

#     mqtt_client.publish(client_telemetry_topic, telemetry)

#     time.sleep(5)





from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5050)

import time
import counterfit_shims_serial
import pynmea2
import json
from azure.iot.device import IoTHubDeviceClient, Message

connection_string = 'HostName=fruit-quality-detector-hovietbach061204.azure-devices.net;DeviceId=proximity;SharedAccessKey=GD+8PrbC0NJnslkqjOBHK6iMxTmf3DIwpAIoTFJqMNk='

serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

def send_gps_data(line):
    msg = pynmea2.parse(line)
    if msg.sentence_type == 'GGA':
        lat = pynmea2.dm_to_sd(msg.lat)
        lon = pynmea2.dm_to_sd(msg.lon)

        if msg.lat_dir == 'S':
            lat = lat * -1

        if msg.lon_dir == 'W':
            lon = lon * -1

        message_json = { "gps" : { "lat":lat, "lon":lon } }
        print("Sending telemetry", message_json)
        message = Message(json.dumps(message_json))
        device_client.send_message(message)

while True:
    line = serial.readline().decode('utf-8')

    while len(line) > 0:
        send_gps_data(line)
        line = serial.readline().decode('utf-8')

    time.sleep(10)