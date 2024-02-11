from taipy.gui import Gui

# Define the page content with the correct Taipy GUI syntax
page_content = """<img src="http://127.0.0.1:5001/video_feed" width="640" height="480" _/>"""

# Create the GUI object and set the page content
gui = Gui(page=page_content)

if __name__ == "__main__":
    # Run the GUI application
    gui.run(title="Live Image Stream Example")
