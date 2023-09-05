import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrap_script(i, url):
    print(f"2_______________________________ In the test.py for {i} time")
    # Initialize a Selenium WebDriver (assuming you have ChromeDriver installed)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 20)  # Wait up to 10 seconds

    title = "N_A"
    description = "N_A"
    code = "N_A"
    max_retries = 3

    for retry in range(max_retries):
        try:
            # Check for and close an ad or pop-up if it appears
            ad_close_button = driver.find_element(By.CLASS_NAME, 'close-button-ggQH9Zyp')
            ad_close_button.click()
            time.sleep(1)  # Add a short sleep to allow the ad to close
            break
        except Exception as e:
            print("add not appear")
            pass

    title_selector = ".tv-chart-view__title-name.js-chart-view__name"
    for retry in range(max_retries):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, title_selector))
            )
            title = title_element.text
            # Clean up the title to remove or replace invalid characters
            title = re.sub(r'[\\/*?:"<>|]', '_', title)
            break
        except Exception as e:
            print(f"Could not extract the script title for script for script {i}")

    description_selector = ".tv-chart-view__description-wrap.js-chart-view__description"

    for retry in range(max_retries):
        try:
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, description_selector))
            )
            description = description_element.text
            break
        except Exception as e:
            print(f"Could not extract the script description for script for script {i}")

    # driver.execute_script("window.scrollBy(0, 3500);")

    # Scroll down to the button using JavaScript
    button_class_name = "collapseBtn-PWda3OiR"
    for retry in range(max_retries):
        try:
            show_more_code_button_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, button_class_name)))
            show_more_code_button_element.click()
            driver.execute_script("arguments[0].scrollIntoView();", show_more_code_button_element)
            # Click the button

            # Scroll down continuously to the end of the page
            while True:
                # Scroll down using JavaScript
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for a short moment to let the page load more content
                time.sleep(2)

                # Check if we've reached the end of the page
                if driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight"):
                    break
            break
        except Exception as e:
            print(f"Expand code button clicking failed for script for script {i}")

    code_selector = ".view-lines.monaco-mouse-cursor-text"

    for retry in range(max_retries):
        try:
            code_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, code_selector))
            )
            code = code_element.text
            break
        except Exception as e:
            print(f"Could not extract the script code for script for script {i}")

    # Create a text file for each script
    with open(f"data/{title}.txt", "w", encoding="utf-8") as file:
        file.write(f"Title: {title}\n")
        file.write(f"Job Description:\n{description}\n")
        file.write(f"Code Description:\n{code}\n")

        print(f"{i}....{title} stored in data directory successfully")

    driver.quit()
