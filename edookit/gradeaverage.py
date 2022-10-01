from edookit.scraper import Scraper

def gradeAverage(access1, access2):
    print("Loading Chrome webdriver...")
    scraper = Scraper(access1, access2)
    print("Loaded!")
    scraper.login()
    marks = scraper.getMarks()
    scraper.logout()

    avrg = []

    for subj, markList in marks.items():
        total = 0
        amount = 0
        for markDict in markList:
            for mark, wage in markDict.items():
                if wage == '0.5':
                    wage = 1
                else:
                    wage = int(wage) * 2
                wagedMark = int(mark) * wage
                total = total + wagedMark
                amount = amount + wage
        avrg.append({subj: total / amount})
    
    return avrg
