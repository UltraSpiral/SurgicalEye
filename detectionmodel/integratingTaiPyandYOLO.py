#This is the working code

from flask import Flask, Response
import cv2
from ultralytics import YOLO
import threading
import math
from taipy.gui import Gui

# Initialize the YOLO model
model = YOLO("best.pt")  # Make sure the model file 'best.pt' is in the correct path

# Flask app to serve the video stream
app = Flask(__name__)

def generate_frames():
    
    # classNames = ['0', '1', '2', '3']
    classNames = ['forceps', 'forceps', 'mayo scissors', 'straight scissors']
    cap = cv2.VideoCapture("exVid.mp4")  # Make sure the video file 'exVid2.mp4' is in the correct path

    while True:
        success, img = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset the video to start from the beginning
            continue   # End of video file or error

        # Process the frame with YOLO
        results = model(img)
        for r in results:
            boxes = r.boxes

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


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
def run_flask_app():
    app.run(port=5001, debug=True, use_reloader=False, threaded=True)

# Start Flask server in a separate thread
threading.Thread(target=run_flask_app, daemon=True).start()

# Taipy GUI setup
page_content = """<img src="http://127.0.0.1:5001/video_feed" width="640" height="480" _/>"""
gui = Gui(page=page_content)

if __name__ == "__main__":
    

    # Start Taipy GUI in the main thread
    gui.run(title="Live Image Stream Example")
