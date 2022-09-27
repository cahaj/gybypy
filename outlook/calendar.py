import win32com.client as client
from outlook.subjects import validsubj
from datetime import datetime, date, timedelta
import time
import json
import re

import os
os.system('color')
from termcolor import colored

def convertdate(due):
    r = ["do ", " ", ",", "\u2009"]
    for i in r:
        due = due.replace(i, "")
    due = due.replace(".", "/", 1)
    y = time.strftime("%y", time.localtime())
    due = due.replace(".", f"/{y} ")
    date = datetime.strptime(due, '%d/%m/%y %H:%M')
    return date


def fetchcalendar(hw, i):
    outlook = client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    calendar = outlook.getDefaultFolder(9).Items

    begin = date.today()
    end = begin + timedelta(days = 30);

    calendar.IncludeRecurrences = True
    calendar.Sort('[Start]')

    restriction = "[Start] >= '" + begin.strftime('%m/%d/%Y') + "' AND [END] <= '" + end.strftime('%m/%d/%Y') + "'"
    calendar = calendar.Restrict(restriction)
    calendarlist = []

    for appointmentItem in calendar:
        if appointmentItem.Subject in validsubj():
            des = hw.get(i)[0]["description"]
            if des in appointmentItem.Body:
                calendarlist.append(des)
    return calendarlist

def body(hw, i):
    des = hw.get(i)[0]["description"]
    teacher = hw.get(i)[3]["teacher"]
    if " (" in i:
        return f"{des}\r\n\r\nTeacher: {teacher}"
    else:
        return f"{i}\r\n{des}\r\n\r\nTeacher: {teacher}"

def create_event():
    with open('homework.json', 'r', encoding='utf-8') as file:
        hw = json.load(file)
        for i in hw:
            if hw.get(i)[0]["description"] in fetchcalendar(hw, i):
                print(colored(f"calendar.py:", "cyan"), colored(f"{i} is already synced", "yellow"))
            elif hw.get(i)[0]["description"] not in fetchcalendar(hw, i):
                outlook = client.Dispatch("Outlook.Application")
                cal = outlook.CreateItem(1)
                cal.Subject = hw.get(i)[2]["subject"]
                cal.Body = body(hw, i)
                cal.Start = convertdate(hw.get(i)[1]["due"]).strftime("%Y-%m-%d %H:%M")
                cal.Duration = 45
                cal.Importance = 2
                cal.Save()
                print(colored(f"calendar.py:", "cyan"), colored(f"Synced {i}", "green"))
