from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
from outlook.subjects import validsubj

def stringToList(string):
        listRes = list(string.split("\n"))
        return listRes

os.system('color')
from termcolor import colored


class Scraper():
    def __init__(self, access1, access2) -> None:
        self.access1 = access1
        self.access2 = access2
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        op.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        self.driver.get("https://gyby.edookit.net/user/login")
        self.actions = ActionChains(self.driver)

    def login(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'plus4ULoginButton'))).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'accessCode1'))).click()
        self.actions.send_keys(self.access1).perform()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'accessCode2'))).click()
        self.actions.send_keys(self.access2).perform()

        element = self.driver.find_element(By.XPATH, "/html/body/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[3]/div/div[1]/form/button[1]")
        element.click()

        print(colored("scraper.py:", "cyan"), "LOGIN")

    def gethw(self):
        self.driver.find_element(By.ID, 'menu-icon').click()
        self.driver.find_element(By.CLASS_NAME, 'assignments ').click()
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/ul/li[4]/ul/li[1]/a/span').click()
        time.sleep(1)
        gethomework = self.driver.find_elements(By.XPATH, '//*[@id="shownSelector1"]')

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
        subjectRAW = homework_list[1::7]
        name = homework_list[2::7]
        for count, x in enumerate(name):
            name[count] = f"{x} - {count}"
        description = homework_list[3::7]
        teacher = homework_list[5::7]

        subject = []
        for i in subjectRAW:
            for subj in validsubj():
                if subj in i:
                    subject.append(subj)
                else:
                    continue

        for count, i in enumerate(name):
            hw[i] = []
            hw[i].append({"description": description[count]})
            hw[i].append({"due": due[count]})
            hw[i].append({"subject": subject[count]})
            hw[i].append({"teacher": teacher[count]})

        with open('homework.json', 'w', encoding='utf-8') as file:
            json.dump(hw, file, indent=2, ensure_ascii=False)

        print(colored("scraper.py:", "cyan"), "FETCHED HOMEWORK DATA TO homework.json")

    def getMarks(self):
        self.driver.find_element(By.ID, 'menu-icon').click()
        self.driver.find_element(By.CLASS_NAME, 'evaluation ').click()
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/ul/li[3]/ul/li[2]/a/span').click()
        time.sleep(1)
        getmarks = self.driver.find_element(By.XPATH, '//div[@id="shownSelector1"]')
        marks = stringToList(getmarks.text)
        marks.remove("Předmět a téma")
        marks.remove("Hodnocení")
        marks.remove("Vytvořeno")

        getwage = self.driver.find_elements(By.XPATH, '//div[@id="shownSelector1"]/..//span[@title]')
        wage = []
        for p in range(len(getwage)):
            if "Váha" in getwage[p].get_attribute('title'):
                wage.append(getwage[p].get_attribute('title').replace("Váha: ", ""))

        md = {}

        subject = marks[0::7]
        mark = marks[3::7]

        for count, i in enumerate(subject):
                if i not in md:
                    md[i] = []
                md[i].append({mark[count]: wage[count]})
        print(colored("scraper.py:", "cyan"), "FETCHED MARKS")
        return md

    def logout(self):
        self.driver.find_element(By.ID, "headerAvatarMobile").click()
        self.driver.find_element(By.CLASS_NAME, "logout").click()
        print(colored("scraper.py:", "cyan"), "LOGOUT")
