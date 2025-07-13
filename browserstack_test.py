from selenium import webdriver
import time
from concurrent.futures import ThreadPoolExecutor

USERNAME = 'ashishattri_NUHbrC'
ACCESS_KEY = 'Mj6umKgxho8ssKNCXs2M'
BSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

browsers = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Test on Chrome",
            "buildName": "ElPais_MultiBrowser_Assignment"
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Test on Firefox",
            "buildName": "ElPais_MultiBrowser_Assignment"
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Test on Safari",
            "buildName": "ElPais_MultiBrowser_Assignment"
        }
    },
    {
        "browserName": "Chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S22",
            "realMobile": "true",
            "osVersion": "12.0",
            "sessionName": "Test on Galaxy S22",
            "buildName": "ElPais_MultiBrowser_Assignment"
        }
    },
    {
        "browserName": "Safari",
        "bstack:options": {
            "deviceName": "iPhone 14",
            "realMobile": "true",
            "osVersion": "16",
            "sessionName": "Test on iPhone 14",
            "buildName": "ElPais_MultiBrowser_Assignment"
        }
    }
]

def run_test(cap):
    options = webdriver.ChromeOptions()
    for key, value in cap.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=BSTACK_URL,
        options=options
    )

    try:
        driver.get("https://elpais.com/opinion/")
        print(f"[{cap.get('browserName', cap['bstack:options'].get('deviceName'))}] Page title: {driver.title}")
        time.sleep(3)
    finally:
        driver.quit()


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_test, browsers)
