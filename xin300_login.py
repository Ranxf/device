# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest2 as unittest
import time
import xin300_8148
import apc

class Xin300Test(unittest.TestCase,unittest.TestResult):
    MAX_WAIT_TIME_IN_MS = 60000
    BASE_URL = "http://192.168.1.180"
    DRIVERHOST= 'http://192.168.2.175:4444/wd/hub'

    def setUp(self):
        self.driver = webdriver.Remote(
                command_executor=self.DRIVERHOST,
                desired_capabilities={'browserName' : "internet explorer",
                        'ignoreProtectedModeSettings' : False,
			'requireWindowFocus' : False})
        self.wait = WebDriverWait(self.driver, 2)
        self.con = xin300_8148.xin300_8148()
        self.apc = apc.apc()
        self.apc.connect("192.168.1.90", "> ")
        self.apc.login("ap","ap")
        self.con.connect('/dev/ttyUSB1','8148_EVM#')
    def tearDown(self):
        self.driver.quit()
    def test_Calibrate(self):
        """login test"""
        self.apc.enter_outlet_menu()
        for i in range(200):
            self.apc.outlet_cmd("3",3)
            time.sleep(5)
            self.con.reset_to_system()
            driver = self.driver
            driver.get(self.BASE_URL)
            user = driver.find_element_by_id("oReset").click()
            time.sleep(1)
            user = driver.find_element_by_name("strUsername")
            user.send_keys("admin")
            passwd = driver.find_element_by_name("strPassword")
            passwd.send_keys("admin")
            lang = select.Select(driver.find_element_by_id("idselect"))
            lang.select_by_value("en")
            driver.find_element_by_id("oLogin").click()
            time.sleep(2)
            try:
                self.wait.until(EC.alert_is_present())
                alert = driver.switch_to_alert()
                alert.accept()
            except Exception:
                pass
            driver.find_element_by_id("oLogoff").click()
            alert = driver.switch_to_alert()
            alert.accept()
            time.sleep(2)
            print("%s times" % i)
if __name__ == '__main__':
       unittest.main()
