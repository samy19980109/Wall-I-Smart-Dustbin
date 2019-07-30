# ----------------------------------------------------------------------------------
# MIT License
#
# Copyright(c) Microsoft Corporation. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# ----------------------------------------------------------------------------------
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests
import os
from azure.storage.blob import *
import cv2
import numpy as np
import time
from time import sleep
from threading import Thread
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import serial

url = "http://100.64.220.6:8080/shot.jpg"
SAMPLE_PROJECT_NAME = "garbage_recognition"
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
training_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.2/Training/"
prediction_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/"
training_key = "**********************************"
prediction_key = "****************************************"

#Connection to Arduino
ser = serial.Serial("/dev/cu.usbmodem14501", 9600)


# function to send data to arduino based on the type of garbage
# Legend : 0::Organic, 1::Recycle
def sendUpdateToArduino(w_type):
    print("----Sending update to Arduino----")
    if (w_type != "recycle"):
        ser.write('a'.encode()) #Organic is represented` by a
    else:
        ser.write('b'.encode()) #Recycle is represented by b 

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

def run_sample():
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='functionsimgpro9756', account_key='****************************************')

        # Create a container called 'quickstartblobs'.
        container_name ='samples-workitems'
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        local_file_name = "Mobile_camera_Feed.jpg"
        full_path_to_file = "./Mobile_camera_Feed.jpg"

        predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)
        project = find_project()


        while True:
            print("HI!!!")
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            time.sleep(0.1)
            try:
                img = cv2.imdecode(img_arr, -1)
            except:
                print("An exception occurred")

            cv2.imwrite("Mobile_camera_Feed.jpg", img)
            block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

            #Make Prediction
            print("Make prediction")
            with open("Mobile_camera_Feed.jpg", mode="rb") as test_data:
                results = predictor.predict_image(project.id, test_data.read())

            waste_type = results.predictions[0].tag_name
            # Display the results.
            print(waste_type)

            sendUpdateToArduino(waste_type)
            # for prediction in results.predictions:
            #     # print(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
            #     print(prediction.tag_name)

            if cv2.waitKey(1) == 27:
                break
            sleep(10)

    except Exception as e:
        os.remove(full_path_to_file)
        print(e)



# Main method.
if __name__ == '__main__':
    thread = Thread(target = run_sample())
    thread.start()
    thread.join()



