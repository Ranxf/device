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

class Xin300Test(unittest.TestCase,unittest.TestResult):
    MAX_WAIT_TIME_IN_MS = 60000
    BASE_URL = "http://192.168.1.144"
    DRIVERHOST= 'http://192.168.2.174:4444/wd/hub'
    
    def setUp(self):
        self.driver = webdriver.Remote(
   		command_executor=self.DRIVERHOST,
   		desired_capabilities={'browserName' : "internet explorer",
			'ignoreProtectedModeSettings' : True})
        self.wait = WebDriverWait(self.driver, 10)
    def tearDown(self):
        result = self.TestResult()
        print("get error screenshot")
        print(result.wasSuccessful())
        if not result.wasSuccessful:
            self.driver.get_screenshot_as_file('/tmp/1.png')
        self.driver.quit()
        
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
        time.sleep(2)
        self.assertIn("Xin-Intelligent Tracking Integrated System", driver.title)
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
        time.sleep(1)
        self.assertIn(u'Xin-智能跟踪一体化系统', driver.title)

    def testLoginEnErr(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_name("strUsername")
        user.send_keys("admin")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin1")
        lang = select.Select(driver.find_element_by_id("idselect"))
        lang.select_by_value("en")
        driver.find_element_by_id("oLogin").click()
        time.sleep(1)
        alert = driver.switch_to_alert()
        self.assertIn(u'Login failed!',alert.text)
        alert.accept()
        user = driver.find_element_by_name("strUsername")
        user.send_keys("admin1")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin1")
        driver.find_element_by_id("oLogin").click()
        alert = driver.switch_to_alert()
        self.assertIn(u'Login failed!',alert.text)

    def testSetWACName(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_name("strUsername")
        user.send_keys("admin")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin")
        lang = select.Select(driver.find_element_by_id("idselect"))
        lang.select_by_value("cn")
        driver.find_element_by_id("oLogin").click()
        time.sleep(1)
        driver.find_element_by_id("selectsetpara").click()
        time.sleep(1)
        #self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID,"iframeconfig")))
        driver.switch_to_frame("iframeconfig")
        wac_name=driver.find_element_by_id("deviceName_wacDevice")
        wac_name.clear()
        wac_name.send_keys("my-144-wac-test")
        setbtn = driver.find_element_by_id("buttons_wacDevice")
        #self.wait.until(EC.element_to_be_clickable((By.ID,"oSetup")))
        refresh = setbtn.find_element_by_id("oRefresh")
        setbtn = setbtn.find_element_by_id("oSetup")
        setbtn.click()
        time.sleep(1)
        #self.wait.until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        self.assertIn(u'参数配置成功',alert.text)
        alert.accept()
        refresh.click()
        time.sleep(1)
        wac_name = driver.find_element_by_id("deviceName_wacDevice")
        name = wac_name.get_attribute("value")
        self.assertIn(u'my-144-wac-test', name)

    def testSetPTZName(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_name("strUsername")
        user.send_keys("admin")
        passwd = driver.find_element_by_name("strPassword")
        passwd.send_keys("admin")
        lang = select.Select(driver.find_element_by_id("idselect"))
        lang.select_by_value("cn")
        driver.find_element_by_id("oLogin").click()
        time.sleep(1)
        driver.find_element_by_id("selectsetpara").click()
        time.sleep(1)
        #self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID,"iframeconfig")))
        driver.switch_to_frame("iframeconfig")
        driver.find_element_by_id("oPtzCamera").click()
        driver.find_element_by_id("ptzOSD").click()
        ptz_name = driver.find_element_by_id("deviceName_ptzOSD")
        ptz_name.clear()
        ptz_name.send_keys("my-144-ptz-test")
        setbtn = driver.find_element_by_id("buttons_ptzOSD")
        #self.wait.until(EC.element_to_be_clickable((By.ID,"oSetup")))
        refresh = setbtn.find_element_by_id("oRefresh")
        setbtn = setbtn.find_element_by_id("oSetup")
        setbtn.click()
        time.sleep(1)
        #self.wait.until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        self.assertIn(u'参数配置成功',alert.text)
        alert.accept()
        refresh.click()
        time.sleep(1)
        wac_name = driver.find_element_by_id("deviceName_ptzOSD")
        name = wac_name.get_attribute("value")
        self.assertIn(u'my-144-ptz-test', name)

    def testEnableRTSP(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        user = driver.find_element_by_name("strUsername")
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
        driver.find_element_by_id("oCommonSetting").click()
        driver.find_element_by_id("oSetMenuRTSP").click()
        time.sleep(1)
        driver.find_element_by_id("rtspEnabledFlag_wacRTSP").click()
        setbtn = driver.find_element_by_id("buttons_wacRTSP")
        #self.wait.until(EC.element_to_be_clickable((By.ID,"oSetup")))
        refresh = setbtn.find_element_by_id("oRefresh")
        setbtn = setbtn.find_element_by_id("oSetup")
        setbtn.click()
        time.sleep(5)
        alert = driver.switch_to_alert()
        self.assertIn(u'Configuration succeed',alert.text)
        alert.accept()
        
if __name__ == '__main__':
    # suite = unittest.TestSuite()  
    # suite.addTest(Xin300Test('testLoginEn'))  
    # suite.addTest(Xin300Test('testLoginCn'))  
    # suite.addTest(Xin300Test('testSetWACName'))  
    # 
    # count = 0
    # while(count<3000):
    #     unittest.TextTestRunner().run(suite)  
    #     count = count + 1
    #     print("Run count %d"%count)
    unittest.main()

