from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://gyby.edookit.net/user/login")
actions = ActionChains(driver)

def login(access1, access2):
    time.sleep(1)
    element = driver.find_element(By.ID, "plus4ULoginButton")
    element.click()
    time.sleep(1)

    window_before = driver.window_handles[0]
    window_after = driver.window_handles[1]

    driver.switch_to.window(window_after)
    driver.maximize_window()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'accessCode1'))).click()
    actions.send_keys(access1).perform()


    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'accessCode2'))).click()
    actions.send_keys(access2).perform()

    time.sleep(1)
    element = driver.find_element(By.XPATH, "/html/body/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[3]/div/div[1]/form/button[1]")
    element.click()

    driver.switch_to.window(window_before)

def gethw():
    def stringToList(string):
        listRes = list(string.split("\n"))
        return listRes

    time.sleep(2)
    driver.find_element(By.ID, 'menu-icon').click()
    driver.find_element(By.CLASS_NAME, 'assignments ').click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/ul/li[4]/ul/li[1]/a/span').click()
    time.sleep(1)
    gethomework = driver.find_elements(By.XPATH, '//*[@id="shownSelector1"]')

    homework = ""
    for p in range(len(gethomework)):
        homework += gethomework[p].text
    homework_list = stringToList(homework)
    homework_list.remove('Termín odevzdání')
    homework_list.remove('Popis')
    homework_list.remove('Postup')
    homework_list.remove('Vytvořeno')

    hw = {}

    due = homework_list[0::7]
    subject = homework_list[2::7]
    for count, x in enumerate(subject):
        subject[count] = f"{x} - {count}"
    description = homework_list[3::7]
    teacher = homework_list[5::7]

    for count, i in enumerate(subject):
        hw[i] = []
        hw[i].append({"description": description[count]})
        hw[i].append({"due": due[count]})
        hw[i].append({"teacher": teacher[count]})

    with open('homework.json', 'w', encoding='utf-8') as file:
        json.dump(hw, file, indent=2, ensure_ascii=False)

def logout():
    driver.find_element(By.ID, "headerAvatarMobile").click()
    driver.find_element(By.CLASS_NAME, "logout").click()
