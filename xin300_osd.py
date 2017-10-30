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

class Xin300Test(unittest.TestCase,unittest.TestResult):
    MAX_WAIT_TIME_IN_MS = 60000
    BASE_URL = "http://192.168.1.144"
    DRIVERHOST= 'http://192.168.2.175:4444/wd/hub'

    def setUp(self):
        self.driver = webdriver.Remote(
                command_executor=self.DRIVERHOST,
                desired_capabilities={'browserName' : "internet explorer",
                        'ignoreProtectedModeSettings' : False,
			'requireWindowFocus' : False})
        self.wait = WebDriverWait(self.driver, 500)
    def tearDown(self):
        self.driver.quit()
    def test_Calibrate(self):
        """Calibrate test"""
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
        setpara_btn = driver.find_element_by_id("selectsetpara")
        setpara_btn.click()
        EC.frame_to_be_available_and_switch_to_it("iframeconfig")
        time.sleep(1)
        driver.switch_to_frame("iframeconfig")
        driver.find_element_by_id("oStation").click()
        for i in range(0, 1000):
            driver.find_element_by_id("oCommonSetting").click()
            driver.find_element_by_id("oSetMenuOSD").click()
            driver.find_element_by_id("targetFrame_wacOSD").click()
            driver.find_element_by_id("deviceName_wacOSD").send_keys(Keys.CONTROL + "a")
            driver.find_element_by_id("deviceName_wacOSD").send_keys(u"新180-test-" + str(i))
            setbtn=driver.find_element_by_id("buttons_wacOSD")
            setbtn.find_element_by_id("oSetup").click()
            self.wait.until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            alert_text = alert.text
            with self.subTest(i=i):
                self.assertIn(u'succe',alert_text)
                print("pass %d" % i)
            alert.accept()
if __name__ == '__main__':
       unittest.main()
