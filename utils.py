import itertools
import sys
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# not using
class Driver:
  def __init__(self):
    self.options = Options()
    self.options = webdriver.ChromeOptions() 
    self.options.add_argument("--log-level=3")
    self.options.add_argument('--headless')
    self.driver = webdriver.Chrome(options=self.options)
  def search(self, url):
    return self.driver.get(url)
  def wait(self, time):
    return WebDriverWait(self.driver, time)


def test_driver(url, time=10):
  driver = webdriver.Chrome()
  driver.get(url)
  wait = WebDriverWait(driver, time)
  return driver, wait
    
def make_driver(url, time=10):
  options = Options()
  options = webdriver.ChromeOptions() 
  options.add_argument("--log-level=3")
  options.add_argument('--headless')
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  wait = WebDriverWait(driver, time)

  return driver, wait
  

def is_similar(str1, str2, max_diff=2):
  if abs(len(str1) - len(str2)) > max_diff:
    return False
  diff_count = 0
  for i in range(min(len(str1), len(str2))):
    if str1[i] != str2[i]:
      diff_count += 1
      if diff_count > max_diff:
        return False
  return True

def non_specialify(word):
  pattern = r"[^\w\s]"
  non_special_word = re.sub(pattern, '', word)
  return non_special_word.replace(',', '')


def dearray(nested_list):
  return list(itertools.chain.from_iterable(nested_list))

def is_decimal(number: str):
  if isinstance(number, str) and '.' in number:
    return True
  return False

def has_decimal(numbers):
  for num in numbers:
    if isinstance(num, float):
      return True
  return False  

def get_folder_files(path):
    folder_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            folder_files.append(file_path)
    return folder_files
     


def cammel_case(words):
  split_words = words.split()
  capital = [word.capitalize() for word in split_words]
  capital_words = ' '.join(capital)
  return capital_words
  

class Site(webdriver.Chrome):
  def __init__(self, driver=None):
      # Initialize options once
      options = Options()
      options.add_argument("--log-level=3")
      options.add_argument("--disable-popup-blocking")  # Prevents new tabs from opening

      if driver and isinstance(driver, webdriver.Chrome):
          self.driver = driver
      elif driver == "test":
          super().__init__(options=options)  
          self.get("https://ctclink.okta.com/app/ctclink_canvaswenatcheevalleycollege_1/exk8ykhtdcsBEjxNz4x7/sso/saml?SAMLRequest=fVLLbsIwELz3KyLfkzhpgNYCJCititQHKrSHXpBxFnBx7NTr8OjX14RWpQe4zs7s7Iy2jbxQJetVbqlf4LMCdMG2UBpZPeiQympmOEpkmheAzAk27j0%2BsDSirLTGGWEUOZKcV3BEsE4aTYLhoEOmzVZGm8k1DbMrnodZzmk4oyIPG0mzdS2ajUQAJ8EbWPSaDvErvBCxgqFGx7XzEE2zMKEhTSc0ZZeUNRrvJBj4HFJzV6uWzpXI4lg4oaReRWbleCRMEfOy%2FAWngus1xw14kVgCrLlSsPPZFCxgmsSwXV3tVkuXC%2BzffmyfvrJtK0Y08T4zCXq%2FuW6MxqoAOwa7lgJeXx7%2B%2FDdrEUl%2Ft62EqyzUJyizkPpnyeinzr7UudSL803ODiRk95PJKBw9jyek297vYXU%2Ftrt3PWG6p6Xt%2BJjdPvzBk%2FcZDkZGSbEL7owtuDt9RhIlNSLzcF5TWaWxBCHnEnLfiVJmc2OBO%2BgQ7w8k7h5M%2F%2F9b9%2BIb")
      elif driver == "remote":
          options.add_experimental_option("debuggerAddress", "127.0.0.1:6080")
          super().__init__(options=options)  # Initialize the base class
      else:
          super().__init__(options=options)  
          options.add_argument('--headless')  
  def set_url(self, url):
      self.driver.get(url)
      print(self.driver.title)

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
