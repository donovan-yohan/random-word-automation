import os
import sys
import time

import PySimpleGUI as sg

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

paths = [
    "all words",
    "noun",
    "verb",
    "adjective",
    "sentence",
    "question",
    "idiom",
    "vocabulary",
]


layout = [
    [sg.T("        "), sg.Button("Start Reading", size=(20, 4))],
]
for path in paths:
    layout.append(
        [
            sg.Radio(
                path,
                1,
                default=True if path == paths[0] else False,
                key=path,
            )
        ]
    )
layout.append([sg.Text("Delay between words"), sg.InputText("30", key="TIME")])
###Setting Window
window = sg.Window("Random Word Reader", layout, size=(300, 400))

###Showing the Application, also GUI functions can be placed here.

launchProgram = False
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Start Reading":
        launchProgram = True
        break

window.close()


### Selenium logic
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


if launchProgram == True:
    url = "https://randomword.com/"
    delay = int(values["TIME"])
    for path in paths:
        if values[path] == True and path != "all words":
            url += path

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        executable_path=resource_path("./chromedriver.exe"), options=options
    )
    action = webdriver.ActionChains(driver)

    driver.get(url)
    speak_word_script = """    
        window.speechSynthesis.cancel();
        utterance = new SpeechSynthesisUtterance(document.getElementById("random_word").innerText);
        window.speechSynthesis.speak(utterance);
    """

    next_word_script = """
        document.getElementById("next_random_word").querySelector("a").click();
    """
    try:
        action.move_to_element(
            WebDriverWait(driver, delay)
            .until(EC.presence_of_element_located((By.ID, "next_random_word")))
            .find_element_by_tag_name("a")
        ).click().perform()
        while True:
            driver.execute_script(speak_word_script)
            time.sleep(delay)
            driver.execute_script(next_word_script)
    except TimeoutException:
        print("Loading took too long")
