from selenium import webdriver
from time import sleep
import datetime
import json

# need to download the webdrivers
# https://sites.google.com/a/chromium.org/chromedriver/downloads

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
        sleep(1)
    
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

        today_sched = self.data[day_str]
        for shift, info in today_sched.items():
            print(shift)
            # Contiue here
    
    def fill_time(self, start, end):
        # Enter Start time
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtStartHourQuick\"]").send_keys(start[0])
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtStartMinuteQuick\"]").send_keys(start[1])
        if start[2] == "PM":
            self.driver.find_element_by_xpath("//*[@id=\"ContentPane_rdoStartPMQuick\"]").click()

        # Enter end time
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtEndHourQuick\"]").send_keys(end[0])
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_txtEndMinuteQuick\"]").send_keys(end[1])
        if end[2] == "PM":
            self.driver.find_element_by_xpath("//*[@id=\"ContentPane_rdoEndPMQuick\"]").click()


b = Bot("tam.t.nguyen", "123456Qwe!")
schedule = b.get_schedule()
b.process_shifts(schedule)