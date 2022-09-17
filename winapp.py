import edookit.scraper as scraper
import outlook.calendar as cal
import getpass
import json
import time

import os
os.system('color')
from termcolor import colored

def synchw(access1, access2):
    try:
        scraper.login(access1, access2)
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

logins = 'edookit/local_logins.json'

def main():
    file = open(logins, "r")
    json_object = json.load(file)
    file.close()
    if json_object["a1"] == None:
        access1 = getpass.getpass(prompt="Access code 1: ")
        access2 = getpass.getpass(prompt="Access code 2: ")
        json_object["a1"] = access1
        json_object["a2"] = access2
        file = open(logins, "w")
        json.dump(json_object, file)
        file.close()
        synchw(access1, access2)
    else:
        uselogin = input("Use saved logins? [y/n] ")
        if uselogin == "y":
            file = open(logins, "r")
            json_object = json.load(file)
            file.close()
            synchw(json_object["a1"], json_object["a2"])
        elif uselogin == "n":
            remove = input("Remove saved logins? [y/n] ")
            if remove == "y":
                json_object["a1"] = None
                json_object["a2"] = None
                file = open(logins, "w")
                json.dump(json_object, file)
                file.close()
                print(colored("Logins removed. Exiting in 3 seconds", "green"))
                time.sleep(3)
                exit()
            else:
                exit()
        else:
            print(colored("Invalid input. Exiting in 3 seconds", "red"))
            time.sleep(3)
            exit()


if __name__ == '__main__':
    main()
