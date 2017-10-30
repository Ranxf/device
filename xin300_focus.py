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
import re
import telnetlib
import sys

def execute_telnet(host,username,password,finish,commands,output):
    tn = telnetlib.Telnet(host,port=23,timeout=10)
    #tn.set_debuglevel(2)
    tn.read_until('login:')
    tn.write(username + '\n')
    tn.read_until('assword:')
    tn.write(password + '\n')
    tn.read_until(finish)
    for command in commands:
        tn.write('%s\n'%command)
        output = output + tn.read_until(finish)
    tn.close()
    return output

class Xin300Test(unittest.TestCase,unittest.TestResult):
    MAX_WAIT_TIME_IN_MS = 60000
    BASE_URL = "http://192.168.1.194"
    DRIVERHOST= 'http://192.168.2.175:4444/wd/hub'

    def setUp(self):
        self.driver = webdriver.Remote(
                command_executor=self.DRIVERHOST,
                desired_capabilities={'browserName' : "internet explorer",
                        'ignoreProtectedModeSettings' : False,
			'requireWindowFocus' : True})
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
        time.sleep(3)
        EC.frame_to_be_available_and_switch_to_it("iframeview")
        driver.switch_to_frame("iframeview")
        for i in range(0,30):
            start_btn = driver.find_element_by_id("divset2_wacCloud")
            start_btn.find_element_by_id("btnFixFocal").click()
            start_btn.find_element_by_id("oStart").click()
            self.wait.until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            alert.accept()
            time.sleep(3)
            self.wait.until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            alert_text = alert.text
            with self.subTest(i=i):
                self.assertIn(u'success',alert_text)
                print("pass %d" % i)
            alert.accept()
            time.sleep(3)
            if "success" in alert_text:
                save_btn = driver.find_element_by_id("default_wacCloud")
                save_btn.find_element_by_id("oSave").click()
                self.wait.until(EC.alert_is_present())
                alert = driver.switch_to_alert()
                alert.accept()
                # get ip address from url
                host = self.BASE_URL[7:]
                user = 'root'
                password = 'xzrsP@ssw0rd'
                prompt = '~#'
                commands = ['/opt/dvr_rdk/ti816x/read_db | grep DB_KEYID_PTZ_CORRECT_FOCUS -A 3']
                out = ''
                out = execute_telnet(host,user,password,prompt,commands,out)
                focus = ''
                for i in out.split('\n'):
                    print i
                    focus_data = re.match(r'([- 0-9]+)',i)
                    if focus_data:
                        focus_data = focus_data.group(1)
                        focus = focus + focus_data
                for i in focus.split():
                    self.assertLess(int(i),6000)
if __name__ == '__main__':
       unittest.main()
