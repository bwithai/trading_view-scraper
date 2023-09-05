import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from scripts import scrap_script


def load_controller(url):
    # Create a new instance of the Chrome driver (make sure you have chromedriver installed)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)

    # Open a website
    driver.get(url)

    # Wait until the page is fully loaded
    wait = WebDriverWait(driver, 20)  # Wait up to 10 seconds

    # Close the modal (if it's present) using the close icon "login pop-up"
    script_selector = ".tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited"

    scripts = driver.find_elements(By.CSS_SELECTOR, script_selector)
    script_urls = []

    print("total scripts are: ", len(scripts))

    for i, script in enumerate(scripts, start=1):
        try:
            script_url = script.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            print(f"{i}...", script_url)
            script_urls.append(script_url)
        except Exception as e:
            print(f"Could not extract the URL for script {i}:", str(e))

    driver.quit()
    print("1______________________________________________ Driver closed")
    time.sleep(3)
    #
    for i, url in enumerate(script_urls, start=1):
        scrap_script(i, url)
        time.sleep(3)
        continue

    print("---___=== Operation Success ===___---")
    return True