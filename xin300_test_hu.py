# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
import time

class ExampleTest(unittest.TestCase):
    MAX_WAIT_TIME_IN_MS = 60000
    BASE_URL = "http://192.168.1.191"
    
    def setUp(self):
        self.driver = webdriver.Remote(
   		command_executor='http://192.168.2.145:4444/wd/hub',
   		 desired_capabilities={'browserName' : "internet explorer",
                        'ignoreProtectedModeSettings' : "true"})
        
    def tearDown(self):
        self.driver.close()
        
    def testLoginEn(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_name("strUsername")
        user.send_keys("admin")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin")
        lang = select.Select(driver.find_element_by_id("idselect"))
        lang.select_by_value("en")
        driver.find_element_by_id("oLogin").click()

    def testLoginCn(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_name("strUsername")
        user.send_keys("admin")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin")
        lang = select.Select(driver.find_element_by_id("idselect"))
        lang.select_by_value("cn")
        driver.find_element_by_id("oLogin").click()
    
if __name__ == '__main__':
    unittest.main()    
