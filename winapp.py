import win32com.client as client
import server.scraper as scraper
from datetime import datetime
import time
import json
import getpass

def scrape():
    access1 = getpass.getpass(prompt="Access code 1: ")
    access2 = getpass.getpass(prompt="Access code 2: ")
    scraper.login(access1, access2)
    scraper.gethw()
    scraper.logout()

def convertdate(due):
    r = ["do ", " ", ",", "\u2009"]
    for i in r:
        due = due.replace(i, "")
    due = due.replace(".", "/", 1)
    y = time.strftime("%y", time.localtime())
    due = due.replace(".", f"/{y} ")
    date = datetime.strptime(due, '%d/%m/%y %H:%M')
    return date

def create_event():
    with open('homework.json', 'r', encoding='utf-8') as file:
        hw = json.load(file)
        for i in hw:
            outlook = client.Dispatch("Outlook.Application")
            cal = outlook.CreateItem(1)
            subj = i[i.index("(") + 1 : ]
            subj = subj.split(")", 1)[0]
            cal.Subject = subj
            cal.Body = hw.get(i)[0]["description"]            
            cal.Start = convertdate(hw.get(i)[1]["due"]).strftime("%Y-%m-%d %H:%M")
            cal.Duration = 45
            cal.Importance = 2
            cal.Save()
            print(f"Synced {i}")

if __name__ == '__main__':
    scrape()
    create_event()