import requests
from bs4 import BeautifulSoup

def fetch_and_parse_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.get_text())
        return soup.get_text()
    else:
        return "Failed to fetch the website"
        
from taipy import Gui, Task, Config
import threading
import time

# Define the GUI
gui = Gui()

# Initial state
gui.text = "Initial text"

# Task to update the GUI with website content
def update_text_task():
    url = "http://127.0.0.1:5001/get_latest_response"  # URL of the website to fetch
    while True:
        new_text = fetch_and_parse_website(url)
        #print(type(text))
        gui.text = new_text
        time.sleep(1)  # Wait for 60 seconds before fetching again

# Run the task in a background thread
threading.Thread(target=update_text_task, daemon=True).start()

# Define the GUI layout
page="""

{gui.text}
"""
gui.add_page(name="main_page", page=page)

# Run the GUI
gui.run(port=5004)
