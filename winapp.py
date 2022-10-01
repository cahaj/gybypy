from edookit.scraper import Scraper
import outlook.calendar as cal
import edookit.gradeaverage as ga
import getpass
import json
import time
import os
import sys
os.system('color')
from termcolor import colored


def synchw(access1, access2):
    try:
        print("Loading Chrome webdriver...")
        scraper = Scraper(access1, access2)
        print("Loaded!")
        scraper.login()
        scraper.gethw()
        scraper.logout()
        cal.create_event()

    except Exception as e:
        print(colored(f"""
================================================
              EXCEPTION OCCURED        
   make sure you are using valid access codes
================================================      
        """, "red"))
        print(e)
        raise Exception("Internal error. Could be caused by using invalid access codes.")

logins = 'edookit/local_logins.json'

def printAvrg(access1, access2):
    getavrg = ga.gradeAverage(access1, access2)
    print()
    for i in getavrg:
        for subj, avrg in i.items():
            print(f"\033[2;37;40m{subj}\033[1;30;40m ->", colored(avrg, "yellow") )

def main():
    file = open(logins, "r")
    json_object = json.load(file)
    file.close()
    print(colored("GYBYPY prerelease v0.2", "cyan"))
    print("Please select a program [\u001b[33msync\u001b[37m, \u001b[33mavrg\u001b[37m]")
    program = input("\u001b[33m>> \u001b[37m")
    validProg = ["sync", "avrg"]
    if program in validProg:
        if json_object["a1"] == None:
            try:
                access1 = getpass.getpass(prompt="Access code 1: ")
                access2 = getpass.getpass(prompt="Access code 2: ")
                if program == "sync":
                    synchw(access1, access2)
                elif program == "avrg":
                    printAvrg(access1, access2)
                json_object["a1"] = access1
                json_object["a2"] = access2
                file = open(logins, "w")
                json.dump(json_object, file)
                file.close()
                print()
                print(colored("Logins saved", "green"))
            except Exception as e:
                json_object["a1"] = None
                json_object["a2"] = None
                file = open(logins, "w")
                json.dump(json_object, file)
                file.close()
                print(colored("EXCEPTION:", "red"), e)
        else:
            uselogin = input("Use saved logins? [y/n] ")
            if uselogin == "y":
                file = open(logins, "r")
                json_object = json.load(file)
                file.close()
                if program == "sync":
                    synchw(json_object["a1"], json_object["a2"])
                elif program == "avrg":
                    printAvrg(json_object["a1"], json_object["a2"])
            elif uselogin == "n":
                remove = input("Remove saved logins? [y/n] ")
                if remove == "y":
                    json_object["a1"] = None
                    json_object["a2"] = None
                    file = open(logins, "w")
                    json.dump(json_object, file)
                    file.close()
                    print(colored("Logins removed.", "green"))
                else:
                    print(colored("Logins not removed.", "red"))
            else:
                print(colored("Invalid input.", "red"))
    else:
        print(colored("Invalid program", "red"))


while __name__ == '__main__':
    main()
    print()
    print("Press any key to restart...")
    input()
    print()
    print()
