import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Setup Chrome webdriver."""
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=500,500")  
    #options.add_argument("--headless") 
    #options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver


def navigate_to_page(driver, url):
    """Navigate to a specific page."""
    try:
        driver.get(url)
    except Exception as e:
        print(f"Failed to navigate: {e}")
        driver.quit()
        raise


def wait_for_element_and_click(driver, xpath):
    """Wait for an element to be clickable and click."""
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except Exception as e:
        print(f"Failed to wait for element and click: {e}")
        driver.quit()
        raise
def wait_for_element_and_click_extra(driver, xpath):
    """Wait for an element to be clickable and click."""
    try:
        element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except Exception as e:
        print(f"Failed to wait for element and click: {e}")
        driver.quit()
        raise

def check_and_click_checkbox(driver, checkbox_xpath):
    """Check if a checkbox is present and click."""
    try:
        checkbox = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, checkbox_xpath))
        )
        if not checkbox.is_selected():
            checkbox.click()
    except Exception as e:
        print(f"Failed to check and click checkbox: {e}")
        driver.quit()
        raise

def check_clear_inputText(driver, checkbox_xpath, text):
    """Check if a checkbox is present and click."""
    try:
        textInput = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, checkbox_xpath))
        )
        textInput.clear()
        textInput.send_keys(text)

    except Exception as e:
        print(f"Failed to checkclear and send text: {e}")
        driver.quit()
        raise

"""driver = setup_driver()
navigate_to_page(driver, "https://audiobox.metademolab.com/capabilities/tts_description_condition")
# This is for the consent forms
check_and_click_checkbox(driver, "/html/body/div/div[3]/div/div/div[2]/div/input")
wait_for_element_and_click(driver, "/html/body/div/div[3]/div/div/div[3]/button")
wait_for_element_and_click(driver, "/html/body/div/div[1]/div/div[2]/button[2]")
description = "The scalpel in the video is cutting the carotid artery to clean out build"
check_clear_inputText(driver, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div[1]/textarea", description)
styleSpeech = "Act like a doctor who is teaching information in a clear yet strong instructor voice"
check_clear_inputText(driver, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/textarea", styleSpeech)
wait_for_element_and_click(driver, "/html/body/div/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[2]/button[1]")
wait_for_element_and_click_extra(driver, "/html/body/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]")
time.sleep(2)"""

def main(description):
    driver = setup_driver()
    navigate_to_page(driver, "https://audiobox.metademolab.com/capabilities/tts_description_condition")
    # This is for the consent forms
    check_and_click_checkbox(driver, "/html/body/div/div[3]/div/div/div[2]/div/input")
    wait_for_element_and_click(driver, "/html/body/div/div[3]/div/div/div[3]/button")
    wait_for_element_and_click(driver, "/html/body/div/div[1]/div/div[2]/button[2]")
    #description = "The scalpel in the video is cutting the carotid artery to clean out build"
    check_clear_inputText(driver, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div[1]/textarea", description)
    styleSpeech = "Act like a doctor who is teaching information in a clear yet strong instructor voice"
    check_clear_inputText(driver, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/textarea", styleSpeech)
    wait_for_element_and_click(driver, "/html/body/div/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[2]/button[1]")
    wait_for_element_and_click_extra(driver, "/html/body/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]")
    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    description = "The scalpel in the video is cutting the carotid artery to clean out build"
    main(description)
