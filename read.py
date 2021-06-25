import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

url = "https://randomword.com/"
delay = 3
if len(sys.argv) > 1:
    url += sys.argv[1]

if len(sys.argv) > 2:
    delay = sys.argv[2]

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)
action = webdriver.ActionChains(driver)

driver.get(url)
speak_word_script = '''    
    window.speechSynthesis.cancel();
    utterance = new SpeechSynthesisUtterance(document.getElementById("random_word").innerText);
    window.speechSynthesis.speak(utterance);
'''

next_word_script = '''
    document.getElementById("next_random_word").querySelector("a").click();
'''
try:
    action.move_to_element(WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.ID, 'next_random_word'))).find_element_by_tag_name('a')).click().perform()
    while True:
        driver.execute_script(speak_word_script)
        time.sleep(delay)
        driver.execute_script(next_word_script)
except TimeoutException:
    print("Loading took too long")
