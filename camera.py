from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5050)

import io
from counterfit_shims_picamera import PiCamera

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

image = io.BytesIO()
camera.capture(image, 'jpeg')
image.seek(0)

with open('image.jpg', 'wb') as image_file:
    image_file.write(image.read())

prediction_url = 'https://southeastasia.api.cognitive.microsoft.com/customvision/v3.0/Prediction/2f82df96-608d-4650-a3fe-c588de9852e9/classify/iterations/Iteration3/image'

prediction_key = '4b48f607e3414712b8112d162a7a4419'

parts = prediction_url.split('/')
endpoint = 'https://' + parts[2]
project_id = parts[6]
iteration_name = parts[9]

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

image.seek(0)
results = predictor.classify_image(project_id, iteration_name, image)

for prediction in results.predictions:
    print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')