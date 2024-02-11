from flask import Flask, send_from_directory, Response, jsonify  
from taipy.gui import Gui
import threading
from taipy.gui import Gui, notify
from PIL import Image
from io import BytesIO
import base64
import os
import pandas as pd
import downloadAudio
import cv2
from ultralytics import YOLO
import threading
import math
import requests
import json
from requests_toolbelt import MultipartEncoder
import os
from typing import Dict
from typing import List
import pprint
import requests
from bs4 import BeautifulSoup
import random


def get_file_type(filename: str) -> str:
    if filename.lower().endswith('.png'):
        return 'image/png'
    if filename.lower().endswith('.jpg') or filename.endswith('.jpeg'):
        return 'image/jpeg'
    if filename.lower().endswith('.mp4'):
        return 'video/mp4'

def post_files_fileName(filename: str, api_key: str) -> Dict:
    url = 'https://api.archetypeai.dev/v0.3/files'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    with open(filename, 'rb') as file_handle:
        encoder = MultipartEncoder({'file': (os.path.basename(filename), file_handle.read(), get_file_type(filename))})
        response = requests.post(url, data=encoder, headers={**auth_headers, 'Content-Type': encoder.content_type})
        response_data = response.json() if response.status_code == 200 else {}
        return response.status_code, response_data

def post_files(image_array, api_key: str) -> Dict:
    url = 'https://api.archetypeai.dev/v0.3/files'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    _, buffer = cv2.imencode('.jpg', image_array)
    file_like_object = BytesIO(buffer)
    encoder = MultipartEncoder({
        'file': ('image.jpg', file_like_object, 'image/jpeg')  # Adjust the filename and MIME type accordingly
    })
    response = requests.post(url, data=encoder, headers={**auth_headers, 'Content-Type': encoder.content_type})
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data

def summarize(query: str, file_ids: List[str], api_key: str):
    url = 'https://api.archetypeai.dev/v0.3/summarize'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    data_payload = {'query': query, 'file_ids': file_ids}
    response = requests.post(url, data=json.dumps(data_payload), headers=auth_headers)
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data

def describe(query: str, file_ids: List[str], api_key: str):
    url = 'https://api.archetypeai.dev/v0.3/describe'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    data_payload = {'query': query, 'file_ids': file_ids}
    response = requests.post(url, data=json.dumps(data_payload), headers=auth_headers)
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data

def fetch_and_parse_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.get_text())
        return soup.get_text()
    else:
        return "Waiting for Archetype API ..."


#global archetypeResponse
latest_response = {"text": "Waiting for Archetype API ..."}

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."


# THIS IS ALL THE FLASK TO HOST THE VIDEO
# --------------------------------------------------------
model = YOLO("best.pt")  # Make sure the model file 'best.pt' is in the correct path

# Flask app to serve the video stream
app = Flask(__name__)

def generate_frames():
    global latest_response
    # classNames = ['0', '1', '2', '3']
    classNames = ['forceps', 'forceps', 'mayo scissors', 'straight scissors']
    cap = cv2.VideoCapture("exVid.mp4")  # Make sure the video file 'exVid2.mp4' is in the correct path

    frame_counter = 0  # Initialize a frame counter
    last_boxes = []  # Initialize a list to store the last detected boxes
    while True:
        success, img = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset the video to start from the beginning
            continue  # End of video file or error
        if frame_counter % 10 == 0:
            # Process the frame with YOLO only on every 10th frame
            results = model(img)
            last_boxes.clear()  # Clear the previous boxes
            for r in results:
                boxes = r.boxes
                last_boxes.extend(boxes)  # Store the current boxes
            
            #print(img)
            post_status_code, post_response_data = post_files(img, 'gt51b6ea')
            sum_status_code, sum_response_data = summarize("Describe the image", [post_response_data['file_id']], 'gt51b6ea')
            archetypeResponseValue = sum_response_data['response']['processed_text']
            print(archetypeResponseValue)
            latest_response["text"] = archetypeResponseValue
        else:
            boxes = last_boxes  # Use the last detected boxes for drawing

        for box in boxes:
            #bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence: ", confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name: ", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_counter += 1  # Increment the frame counter after each loop

@app.route('/video_feed')
def video_feed():
    #print(archetypeResponse)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#print(archetypeResponse)
@app.route('/get_latest_response')
def get_latest_response():
    # Serve the latest response
    return latest_response['text']
def run_flask_app():
    app.run(port=5001, debug=True, use_reloader=False, threaded=True)

# Start Flask server in a separate thread
threading.Thread(target=run_flask_app, daemon=True).start()

# Taipy GUI setup
video_url = "http://127.0.0.1:5001/video_feed"  # URL to the video served by Flask on port 5001
# --------------------------------------------------------


# This is for the LOGO but not working
# --------------------------------------------------------
logo_image_path = "../LogoImages/logoNoBk.png"
#logo_base64 = convert_image_to_base64(logo_image_path)
# The logo not working need to work on it 
# <|image|src={logo_base64}|style=height: 100px; width: auto;|> **SMTG**{: .color-primary}
# --------------------------------------------------------


path_upload = ""
original_image = None
fixed = True
global audioPATH
audioPATH = "\"./extractedAudioFiles/audio_file.wav\""
print(audioPATH)
# THIS IS FOR THE INSTRUMENTS TABLE NEED TO BE UPDATED IN REAL TIME
# --------------------------------------------------------
instrumentDF = pd.DataFrame({
    "Instrument": ["Scalpel", "Forceps", "Retractor"],
    "Count": [2, 3, 4],
})
#Below functions now working  - need to work on it 
"""
# Function to apply row styling
def highlight_row(state, index, row):
    if row["Instrument"] in highlight_instruments:
        return "highlight-row"
    return ""

def even_odd_style(state, index, row):
    highlight_instruments = ["Scalpel", "Scissors"]
    if row['Instrument'] in highlight_instruments:
        return "yellow-cell"  # Apply this class if the condition is met
    else:
        return ""  # Return an empty string (no class) if the condition is not met

def table_style(state, index, row):
    return "highlight-row" if row.Instrument == "Scalpel" else ""
"""
# --------------------------------------------------------

def button_pressed(state):
    # Update the state with a new audio source
    #state.audio_src = "./extractedAudioFiles/audio_file.wav"
    print("Audio source updated.")
    state.audioPATH = "./extractedAudioFiles/audio_file.wav"
    downloadAudio.main(latest_response["text"])#GIVE THE WORDS HERE
    print(latest_response["text"])

show_audio= False

"""
I can't seem to get the audio thing working 

<audio controls="1" src="./extractedAudioFiles/audio_file.wav">Your browser does not support the audio tag.</audio>
<|{audioPATH}|>
<audio controls="1" src=<|{audioPATH}|>>Your browser does not support the audio tag.</audio>
<audio controls="1" src="./extractedAudioFiles/audio_file.wav">Your browser does not support the audio tag.</audio>

"""
dfInfo = pd.DataFrame({
    "Year": ["2017", "2018", "2019", "2020", "2021", "2022", "2023"],
    "Average Instruments Used": [15, 17, 18, 20, 22, 25, 28]
})
global archetypeStuff

archetypeStuff = latest_response["text"]
def reGetThing():
    archetypeStuff = fetch_and_parse_website("http://127.0.0.1:5001/get_latest_response")




def videoActions(state):
    # Assuming 'notify' is a function that sends notifications to the user interface
    notify(state, 'info', 'Uploading video...')
    
    print("The path of the file is: ")
    uploaded_file_path = state.path_upload  # Path of the uploaded file
    print(uploaded_file_path)
    
    # Get the absolute path of the uploaded file
    absolute_path = os.path.abspath(uploaded_file_path)
    print(absolute_path)
    
    # Define the original path for renaming (make sure this file exists or handle it appropriately)
    originalPath = "./exVid.mp4"
    
    # Generate a new path for the existing video file
    newPath = "./oldVideo_" + str(random.randint(0,100)) + ".mp4"
    
    # Rename the existing video file
    os.rename(originalPath, newPath)
    print(f"Renamed '{originalPath}' to '{newPath}'")
    
    # Now, move the uploaded file to replace the original video
    # Since 'rename' also moves files, we can use it to move and rename the uploaded file to 'originalPath'
    os.rename(absolute_path, originalPath)
    print(f"Moved uploaded file '{absolute_path}' to '{originalPath}'")




page = """
<|toggle|theme|>

<page|layout|columns=300px 1fr|
<|sidebar|



### Upload **Video**{: .color-primary}

<|{path_upload}|file_selector|on_action=videoActions|extensions=.mp4|label=Upload video|>

### Common **Surgical Instruments**{: .color-primary}

| Surgical Instrument          | Description                            |
|------------------------------|----------------------------------------|
| **Scalpel**                  | *Makes initial incisions; blade/handle.* |
| **Scissors**                 | *Cuts tissue, suture; straight/curved.*  |
| **Forceps**                  | *Grasps tissue/objects; toothed/smooth.* |
| **Clamps**                   | *Secures tissue/objects; hemostasis.*    |
| **Needles & Suture**         | *Various shapes; absorbable/permanent.*  |
| **Suction**                  | *Removes debris/fluid; needs source.*    |
| **Retractors**               | *Keeps incisions open; clears field.*    |
| **Laparoscopic Instruments** | *For minimally invasive procedures.*     |
| **Energy Systems**           | *Cuts/seals tissue; electrical/sonic.*   |
| **Staplers and Clips**       | *For reanastomosis; ligates vessels.*    |

|>


<|container|
# Surgical 👁️

<images|layout|columns=1 2|
<col1|card text-center|part|render={fixed}|
## Description
#### *Powered by Archetype*


<iframe src="http://127.0.0.1:5001/get_latest_response" width="100%" height="100" style="background-color: white;"></iframe>

*Reload Page for updates*
<br></br>
<|Listen|button|on_action=button_pressed|>
----

## **Instruments**{: .color-primary} Detected
<|{instrumentDF}|table|style=table_style|width='15%'|>

|col1>

<col2|card text-center|part|render={fixed}|
### Surgical Video Analysis 📷 
<|{original_image}|image|>
<img src="http://127.0.0.1:5001/video_feed" width="640" height="480" _/>
|col2>
|images>
|>

|page>


"""



if __name__ == "__main__":
    Gui(page=page).run(margin="0px", title='Hackalytics Project' )
