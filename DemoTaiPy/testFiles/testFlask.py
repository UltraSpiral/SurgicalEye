from flask import Flask, send_from_directory
from taipy.gui import Gui
import threading
import os
from taipy.gui import Gui, notify
from PIL import Image
from io import BytesIO
import base64
import os
import pandas as pd

fixed = True

# Set up Flask app
app = Flask(__name__)

@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.getcwd(), filename)

# Start Flask in a separate thread to serve video files
def start_flask():
    app.run(port=5001, use_reloader=False, debug=True)

flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

# Taipy GUI setup
video_url = "http://127.0.0.1:5001/video/exVid.mp4"  # URL to the video served by Flask on port 5001
