import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

self.driver = webdriver.Chrome()

class TestDetails():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_testgetuserdetails(self):
    self.driver.get("http://localhost:8000/")
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.LINK_TEXT, "Login with Google").click()
    self.driver.find_element(By.ID, "profileIdentifier").click()
    self.driver.find_element(By.LINK_TEXT, "jaime").click()
  
  def test_testCompleteVotingUserDetails(self):
    self.driver.get("http://localhost:8000/")
    self.driver.set_window_size(970, 748)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.LINK_TEXT, "Login with Linkedin").click()
    self.driver.find_element(By.LINK_TEXT, "Finish setting your profile here to access the platform").click()