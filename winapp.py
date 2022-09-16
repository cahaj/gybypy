import edookit.scraper as scraper
import outlook.calendar as cal
import getpass

def synchw():
    try:
        access1 = getpass.getpass(prompt="Access code 1: ")
        access2 = getpass.getpass(prompt="Access code 2: ")
        scraper.login(access1, access2)
        scraper.gethw()
        scraper.logout()
        cal.create_event()

    except Exception as e:
        print(f"""
================================================
              EXCEPTION OCCURED        
   make sure you are using valid access codes
================================================
{e}       
        """)

if __name__ == '__main__':
    synchw()
