# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import apc

class Xin300Test(unittest.TestCase,unittest.TestResult):
    MAX_WAIT_TIME_IN_MS = 60000
    BASE_URL = "http://192.168.1.144"
    DRIVERHOST= 'http://192.168.2.174:4444/wd/hub'

    def setUp(self):
        self.driver = webdriver.Remote(
                command_executor=self.DRIVERHOST,
                desired_capabilities={'browserName' : "internet explorer",
                        'ignoreProtectedModeSettings' : False,
			'requireWindowFocus' : True})
        self.wait = WebDriverWait(self.driver, 10)
    def tearDown(self):
        self.driver.quit()
    def testReboot(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_id("idUsername")
        user.send_keys("admin")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin")
        lang = select.Select(driver.find_element_by_id("idselect"))
        lang.select_by_value("en")
        driver.find_element_by_id("oLogin").click()
        time.sleep(1)
        driver.find_element_by_id("selectsetpara").click()
        time.sleep(1)
        #self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID,"iframeconfig")))
        driver.switch_to_frame("iframeconfig")
        driver.find_element_by_id("oWacCamera").click()
        driver.find_element_by_id("oAdvanceOption").click()
        driver.find_element_by_id("oSetMenuMaintenance").click()
        driver.find_element_by_id("oReboot").click()
        alert = driver.switch_to_alert()
        alert.accept()

if __name__ == '__main__':
       unittest.main()
