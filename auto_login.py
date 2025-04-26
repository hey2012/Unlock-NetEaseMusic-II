# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00E563CC91A85B75C59B63AA3C238E17E8E543F2BBA4F10868422214594B43ED68BCD196A5CF1A4DCC7DFFEA5D90FDC3E3902E138E381B180358A0E7323F9509806D25B9F241D9F1838DA756FFABEA4D7AB23688F0A20B9ECB0130912058300058D381AEE8817E4188E36B4EA9EDE3C4179ADC07ABD113E4EF6E0E58CB09AB9E83739D6F898B2F86A05F2D74FE01DFD0E31EBF9ACCE67394C5FB19C6DA056A4256103D452289CAF19D7A744F68FD9E86142EB231E1E98B4E334DFAE9F0331F5C9BD7AE091D5076FEF222D634AE2E20CFAD1F3407C9C6626B5B4D34B3AD5C61CA7FC2B87C6593AA284086B164613C6E1031719EC488E052A3F2F599C82912518DAB560B74CF358EB1CE8F48C594D3541CB47E8A79524A2FC386243204642DE284D7852657AF7E5A2850B36129980E482B568E6ACB15BD224D48486C721C07FDB9543C79720606B1604737DB8214B315B59E059656E92C19AB3A8537195961939C26"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
