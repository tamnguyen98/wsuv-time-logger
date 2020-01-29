from selenium import webdriver
from time import sleep
import datetime
import json

# need to download the webdrivers
# https://sites.google.com/a/chromium.org/chromedriver/downloads

SID = "tam.t.nguyen"
user_pass = ""

dropdown_sect = {"HelpDesk": "//*[@id=\"ContentPane_ddlLocationsQuick\"]/option[4]",
                "VCS": "//*[@id=\"ContentPane_ddlLocationsQuick\"]/option[2]",
                "Labs": "//*[@id=\"ContentPane_ddlLocationsQuick\"]/option[1]"
                }

                            #  regular                                          Work study
itemID =    {"HelpDesk": ["//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[2]", "//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[8]"],
            "VCS": ["//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[5]", "//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[7]"],
            "Labs": ["//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[3]", "//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[9]"]
            }

class Bot:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def init_browser(self):
        self.driver = webdriver.Chrome(executable_path='chromedriver_79.exe')
        self.driver.get("https://cougarmanager.it.wsu.edu/breakdown/NewBreakdown.aspx")
        sleep(1)

        self.driver.find_element_by_xpath("//*[@id=\"okta-signin-username\"]").send_keys(self.user)
        self.driver.find_element_by_xpath("//*[@id=\"okta-signin-password\"]").send_keys(self.password)
        sleep(1)

        self.driver.find_element_by_xpath("//*[@id=\"okta-signin-submit\"]").click()
        sleep(2)

        # Click log time
        self.driver.get("https://cougarmanager.it.wsu.edu/breakdown/NewBreakdown.aspx?")
        # self.driver.find_element_by_xpath()
        # self.driver.find_element_by_xpath()
        # self.driver.find_element_by_xpath()
        sleep(2)
    
    # Get Schedule of the day
    def get_schedule(self):
        print("Ha")
        start = ["3", "57", "PM"]
        end = [ "4", "57", "PM"]

        content = ''
        with open('schedule', 'r') as file:
            content = file.read().replace('\n', '')

        self.data = json.loads(content)

    def process_shifts(self, schedule):
        now = datetime.datetime.now()
        day_str = now.strftime("%A")
        print(day_str)

        today_sched = self.data[day_str]
        for shift, info in today_sched.items():
            print(shift)
            print(info['start']['hour'])
            self.fill_time(shift, info)
            # Contiue here
    
    def fill_time(self, shift, info):
        # Enter Start time
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtStartHourQuick\"]").send_keys(info['start']['hour'])
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtStartMinuteQuick\"]").send_keys(info['start']['min'])
        if info['start']['period'] == "PM":
            self.driver.find_element_by_xpath("//*[@id=\"ContentPane_rdoStartPMQuick\"]").click()

        # Enter end time
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtEndHourQuick\"]").send_keys(info['end']['hour'])
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtEndMinuteQuick\"]").send_keys(info['end']['min'])
        if info['end']['period'] == "PM":
            self.driver.find_element_by_xpath("//*[@id=\"ContentPane_rdoEndPMQuick\"]").click()

        # Pick from drop down
        self.driver.find_element_by_xpath(dropdown_sect[shift]).click()
        pay_rate = itemID[shift][1] if info['isWorkStudy'] else itemID[shift][0]
        print(pay_rate)
        self.driver.find_element_by_xpath(pay_rate).click()
        sleep(.5)
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_ddlDutiesQuick\"]/option[2]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_btnSaveQuick\"]").click()



b = Bot(SID, user_pass)
b.init_browser()
schedule = b.get_schedule()
b.process_shifts(schedule)