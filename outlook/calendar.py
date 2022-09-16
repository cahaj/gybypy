import win32com.client as client
from outlook.subjects import validsubj
from datetime import datetime, date, timedelta
import time
import json

def convertdate(due):
    r = ["do ", " ", ",", "\u2009"]
    for i in r:
        due = due.replace(i, "")
    due = due.replace(".", "/", 1)
    y = time.strftime("%y", time.localtime())
    due = due.replace(".", f"/{y} ")
    date = datetime.strptime(due, '%d/%m/%y %H:%M')
    return date

def fetchcalendar():
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
            calendarlist.append(appointmentItem.Body.removesuffix(" \r\n"))

    return calendarlist


def create_event():
    with open('homework.json', 'r', encoding='utf-8') as file:
        hw = json.load(file)
        for i in hw:
            if hw.get(i)[0]["description"] in fetchcalendar():
                print(f"calendar.py: {i} already synced")
            elif hw.get(i)[0]["description"] not in fetchcalendar():
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
                print(f"calendar.py: Synced {i}")