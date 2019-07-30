# Install Custom Vision Service SDK
# pip install azure-cognitiveservices-vision-customvision
# Python SDK Samples https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/tree/master/samples

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
# from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
# import time
import os

# Set these variables based on the settings of your trained project
SAMPLE_PROJECT_NAME = "garbage_recognition"
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
training_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.2/Training/"
prediction_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/"
training_key = "*****************************"
prediction_key = "*************************************"


#  function to fetch project object from Custom Vision Service
def find_project():
    try:
        print("Get trainer")
        trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

        print("get project")
        for proj in trainer.get_projects():
            if (proj.name == SAMPLE_PROJECT_NAME):
                return proj
    except Exception as e:
        print(str(e))


print("Set path for folder containign image to predict")
IMAGES_FOLDER = os.path.dirname(os.path.realpath(__file__))
# print(str(IMAGES_FOLDER))
# print(str(os.path.join(IMAGES_FOLDER, "TestImages", "testelephant2.jpg")))

# Get predictor and project objects
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)
project = find_project()

print("Make prediction")
try:
    with open(os.path.join(IMAGES_FOLDER, "TestImages", "can.jpeg"), mode="rb") as test_data:
        results = predictor.predict_image(project.id, test_data.read())
except Exception as e:
    print(str(e))
    input()
# Display the results.
for prediction in results.predictions:
    # print(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
    print(prediction.tag_name)
    input()
