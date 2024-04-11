
from counterfit_connection import CounterFitConnection
from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X
import io
from counterfit_shims_picamera import PiCamera
from counterfit_shims_grove.grove_led import GroveLed
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import time

# Initialize CounterFit Connection
CounterFitConnection.init('127.0.0.1', 5050)

# Initialize the distance sensor, camera, and LED
distance_sensor = VL53L0X()
distance_sensor.begin()
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0
led = GroveLed(5)

#Azure Custom Vision Service parameters
prediction_key = '4b48f607e3414712b8112d162a7a4419'
prediction_endpoint = 'https://southeastasia.api.cognitive.microsoft.com/'
project_id = '2f82df96-608d-4650-a3fe-c588de9852e9'  
publish_iteration_name = 'Iteration3'

credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(prediction_endpoint, credentials)


def capture_image():
    image = io.BytesIO()
    camera.capture(image, 'jpeg')
    image.seek(0)
    with open('image.jpg', 'wb') as image_file:
        image_file.write(image.read())
    return image


def classify_image(image):
    image.seek(0)
    results = predictor.classify_image(project_id, publish_iteration_name, image)
    return max(results.predictions, key=lambda p: p.probability)

# Main loop
while True:
    distance = distance_sensor.get_distance()
    print(f'Distance = {distance} mm')

    if distance <= 100:
        print("Distance threshold reached. Capturing and classifying image.")
        image = capture_image()
        classification_result = classify_image(image)
        
        
        print(f'Classified as {classification_result.tag_name} with probability {classification_result.probability * 100:.2f}%')
        
        
        if classification_result.tag_name in ['Unripe tomatoes']:
            print("Tomato is unripe. Turning on LED.")
            led.on()
        elif classification_result.tag_name in ['Rotten tomatoes']:
            print("Tomato is rotten. Turning on LED.")
            led.on()
                
        else:
            print("Tomato is ripe. Turning off LED.")
            led.off()

    time.sleep(100)