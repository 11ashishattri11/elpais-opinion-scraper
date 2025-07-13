from selenium import webdriver

USERNAME = 'ashishattri_NUHbrC'
ACCESS_KEY = 'Mj6umKgxho8ssKNCXs2M'

# Set the BrowserStack endpoint
bstack_url = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Define BrowserStack options
bstack_options = {
    "os": "Windows",
    "osVersion": "10",
    "buildName": "Debug_Build_1",
    "sessionName": "SingleBrowserTest"
}

# Create ChromeOptions and attach BrowserStack options
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability('browserName', 'Chrome')
chrome_options.set_capability('browserVersion', 'latest')
chrome_options.set_capability('bstack:options', bstack_options)

# Connect to BrowserStack using only options (no desired_capabilities)
driver = webdriver.Remote(
    command_executor=bstack_url,
    options=chrome_options
)


# Load the website
driver.get("https://elpais.com/opinion/")
print("Page title is:", driver.title)
driver.quit()
