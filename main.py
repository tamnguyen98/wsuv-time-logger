from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from login_creds import *
import datetime
import json
import platform


dropdown_sect = {"HelpDesk": "//*[@id=\"ContentPane_ddlLocationsQuick\"]/option[4]",
                "VCS": "//*[@id=\"ContentPane_ddlLocationsQuick\"]/option[2]",
                "Labs": "//*[@id=\"ContentPane_ddlLocationsQuick\"]/option[1]"
                }

                            #  regular                                         ,  Work study
itemID =    {"HelpDesk": ["//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[2]", "//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[8]"],
            "VCS": ["//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[5]", "//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[7]"],
            "Labs": ["//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[3]", "//*[@id=\"ContentPane_ddlPositionsQuick\"]/option[9]"]
            }

class Bot:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.os = platform.system()
        print (self.os)

    def init_browser(self):
        if self.os == "Windows":
            self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        elif self.os == "Darwin": # If mac
            self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

        self.driver.get("https://cougarmanager.it.wsu.edu/breakdown/NewBreakdown.aspx")
        sleep(1)

        self.driver.find_element_by_xpath("//*[@id=\"okta-signin-username\"]").send_keys(self.user)
        self.driver.find_element_by_xpath("//*[@id=\"okta-signin-password\"]").send_keys(self.password)
        sleep(1)

        self.driver.find_element_by_xpath("//*[@id=\"okta-signin-submit\"]").click()
        sleep(2)

        # Click log time
        self.driver.get("https://cougarmanager.it.wsu.edu/breakdown/NewBreakdown.aspx?")
        if not self.check_if_cssSelector_exist("div#ContentPane_pnlSubmitQuickBreakdown"):
            print("Not on Time Log page, trying alternative...")
            try:
                # self.driver.find_element_by_css_selector("div#repNavigationCategory_pnlNav_3").click()
                butt = self.driver.find_element_by_css_selector("a#repNavigationCategory_repNavigationPage_3_lnkPageLink_1")
                self.driver.implicitly_wait(1)
                butt.click()
            except ElementNotInteractableException:
                print("Can't access the time logging page, please manually direct to that page.")
                input("Press Enter to continue...")


    def check_if_cssSelector_exist(self, str):
        try:
            val = self.driver.find_element_by_css_selector(str)
        except:
            return None
        return val
    
    # Get Schedule of the day
    def get_schedule(self):

        content = ''
        with open('schedule.json', 'r') as file:
            content = file.read().replace('\n', '')

        self.data = json.loads(content)

    def process_shifts(self, schedule):
        now = datetime.datetime.now()
        day_str = now.strftime("%A")
    
        today_sched = self.data.get(day_str)
        if not today_sched:
            print(day_str, ": No scheduled shift")
            return
        
        for shift, info in today_sched.items():
            print(shift)
            print(info['start']['hour'])
            self.fill_time(shift, info)
            sleep(3)
    
    def fill_time(self, shift, info):

        # Check to see if the page is loaded
        if not self.check_if_cssSelector_exist("table#tblHourMinuteQuick"):
            print('Reloading page.')
            self.driver.get("https://cougarmanager.it.wsu.edu/breakdown/NewBreakdown.aspx?")
            sleep(2)

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
        self.driver.find_element_by_xpath(pay_rate).click()
        sleep(.5)

        # Leave this part, it's the last drop down
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_ddlDutiesQuick\"]/option[2]").click()
        sleep(1)

        # Submit
        self.driver.find_element_by_xpath("//*[@id=\"ContentPane_btnSaveQuick\"]").click()

    def history(self):
        card_range = self.check_if_cssSelector_exist("span#ContentPane_lblDateRange1").text

        submitted_time = self.driver.find_elements_by_class_name("timecardheader")
        if submitted_time:
            last_event = submitted_time[len(submitted_time)-1]
            last_day = last_event.text.split(', ')[1].split(' ')[1]
            current_day = datetime.datetime.today().day
            print(f'It been {int(current_day)-int(last_day)} since last log.')


def main():
    b = Bot(SID, user_pass)
    b.init_browser()
    schedule = b.get_schedule()
    b.process_shifts(schedule)
    b.history()

if __name__ == "__main__":
    main()