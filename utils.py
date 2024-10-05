import itertools
import platform
import sys
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Site(webdriver.Chrome):
  def __init__(self, driver=None):
      # Initialize options once
      self.options = webdriver.ChromeOptions()
      self.options.add_argument("--log-level=3")
      self.options.add_argument("--disable-popup-blocking")  # Prevents new tabs from opening

      if driver == "test":
          self.driver = super().__init__(options=self.options)  
      elif driver == "profile":
          self.setup_profile()
          self.driver = super().__init__(options=self.options)  
          self.get("https://wvc.instructure.com/login?needs_cookies=1")
      elif driver == "remote":
          self.options.add_experimental_option("debuggerAddress", "127.0.0.1:6080")
          self.driver = super().__init__(options=self.options)  # Initialize the base class
      else:
          self.driver = super().__init__(options=self.options)  
          self.options.add_argument('--headless')  

  def set_url(self, url):
      self.driver.get(url)
      print(self.driver.title)
  
  def setup_profile(self, profile=os.path.join(".", "profiles", "main")): #could make more than one profile
      if not os.path.exists(profile):
          print(f"Profile not found, creating it at {profile}")
          os.makedirs(profile)  # Create the profile directory

      # Add profile-related options
      self.options.add_argument(f"--user-data-dir={profile}")
      self.options.add_argument("--no-first-run")
      self.options.add_argument("--no-default-browser-check")
      

  def button_search(self, searchbar_id, button_id, search_query, method=By.ID):
    search = self.driver.find_element(method, searchbar_id)
    search.clear()
    search.send_keys(search_query)
    button = self.driver.find_element(method, button_id)
    button.click()
  
  def wait_for(self, method, id, time=10):
    wait = WebDriverWait(self.driver, time)
    wait.until(EC.presence_of_element_located((method, id)))
  
  def wait_for_all(self, method, ids, time=10):
    wait = WebDriverWait(self.driver, time)
    wait.until(EC.presence_of_all_elements_located((method, ids)))
  
  def get_containers(self, id, method=By.CLASS_NAME):
    containers = self.driver.find_elements(method, id)
    return containers
  
  def current_url(self):
    return self.driver.current_url

  def quit(self):
    self.driver.quit()

  def search_container_for_url(self, container, _filter=""):
    for item in container:
      # item_name = item.find_element(By.XPATH, '//h3[class="title"]').find_element(By.TAG_NAME, "a").text.lower()
      title_class = item.find_element(By.CLASS_NAME, "title")
      item_name = title_class.find_element(By.TAG_NAME, "a").text
      item_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
      if _filter:
        if is_similar(item_name, _filter):
          return item_url
      else:
        return item_url
  
  def search_container_for_urls(self, container, _filter=""):
    names = []
    urls = []
    for item in container:
      # item_name = item.find_element(By.XPATH, '//h3[class="title"]').find_element(By.TAG_NAME, "a").text.lower()
      title_class = item.find_element(By.CLASS_NAME, "title")
      item_name = title_class.find_element(By.TAG_NAME, "a").text
      item_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
      if _filter:
        if is_similar(item_name, _filter):
          names.append(item_name)
          urls.append(item_url)
      else:
          names.append(item_name)
          urls.append(item_url)
    return names, urls
  


def search_retry_prompt(origional_anime):
  user_choice = input("Search failed. Retry (y/n/s(kip)) or enter new name: ").lower()
  if user_choice == 'n':
    sys.exit("exiting")
  elif user_choice == 's':
    return 'skip'
  elif user_choice == 'y':
    return origional_anime
  else:
    anime = user_choice
    return anime

def extract_numbers(string): # takes 1 arg no list
  decimal = False
  numbers = re.findall(r'-?\d+\.?\d*', string)
  for num in numbers:
    if is_decimal(num):
      decimal = True
  if decimal:
    return [float(num) for num in numbers]
  else:
    return [int(num) for num in numbers]
