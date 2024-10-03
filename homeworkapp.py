import tkinter as Tk
from tkinter.ttk import *
from tkinter import *
from utils import *
import logging
import json
import pickle

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(levelname)s: %(message)s',  
    handlers=[
        logging.FileHandler('log.log'),  
        logging.StreamHandler()  
    ]
)

log = logging.getLogger(__name__) 

class HomeworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Homework Helper")
        self.frm = Frame(root)
        self.frm.grid(padx=10, pady=10)

        self.url_var = StringVar()
        self.driver = None
        self.cookie_file = "cookies.pkl"

        self.setup_ui()
    
    def show_current_url(self):
        if self.driver is not None:
            current_url = self.driver.current_url  # No parentheses needed
            # Update the label with the current URL
            self.url_label.config(text=f"Current Url: {current_url}")  
    

    def setup_ui(self):
        main_pady=3
        main_padx=3
        if self.driver != None:
            current_url = self.driver.current_url
        #row 0
        Label(self.frm, text="Enter HW URL:").grid(column=0, row=0, sticky=W, padx=main_padx, pady=main_pady)
        Entry(self.frm, textvariable=self.url_var).grid(column=1, row=0, sticky=W, padx=main_padx, pady=main_pady)
        
        #row 1
        Button(self.frm, text="Set URL", command=self.set_url, width=15).grid(column=0, row=1, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Go to Canvas", command=self.set_canvas_url, width=15).grid(column=1, row=1, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Load Canvas Cookies", command=self.load_cookies, width=15).grid(column=2, row=1, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Save Cookies", command=self.save_cookies, width=15).grid(column=3, row=1, sticky=W, padx=main_padx, pady=main_pady)
        #row 2
        Button(self.frm, text="Start", command=self.get_questions, width=15).grid(column=0, row=2, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Pause", command=self.root.destroy, width=15).grid(column=1, row=2, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Quit", command=self.root.destroy, width=15).grid(column=2, row=2, sticky=W, padx=main_padx, pady=main_pady)
    
    def remove_needs_cookie(self):
        current_url = self.driver.current_url()
        cookie_url = "login?needs_cookies=1"
        if cookie_url in current_url: 
            new_url = current_url.replace(cookie_url, "")
            self.set_url(new_url)
            log.info("Adjusted canvas url to login")

    def save_cookies(self):
        try:
            with open(self.cookie_file, 'wb') as file:
                pickle.dump(self.driver.get_cookies(), file)
            file.close()
        except Exception as e:
            log.error(e)

    def load_cookies(self):
        url = self.url_var.get().strip()
        self.set_url(url)
        # self.remove_needs_cookie()
        
        try:
            with open(self.cookie_file, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            log.info("Cookies Succesfully loaded")
            file.close()
        except FileNotFoundError:
            log.info("No cookies to load")
        except Exception as e:
            log.error(e)
    

    def set_url(self, url=""):
        if self.driver is None:
            self.driver = Site("profile")  # Assuming Site is a class that initializes the driver
        try:
            url = self.url_var.get().strip()
            self.driver.get(url)
            self.url_var.set("")  # Clear the input field
        except AttributeError or ValueError:
            log.info("no url in box")
        except Exception as e:
            log.error(f"{e}")

    def set_canvas_url(self):
        canvas_url = "https://wvc.instructure.com/login?needs_cookies=1"
        self.set_url(canvas_url)
    
    def query_chatgpt(self):
        print('lol')
    
    def do_multiple_choice(self):
        print("lol")
    
    def do_checkboxes(self): # Place holder code
        xpath_for_span = "//span[contains(@class, 'rvTxt') and normalize-space(text()) != '']"
        spans = self.driver.find_elements(By.XPATH, xpath_for_span)

        for span in spans:
            text_content = span.text.strip()
            print(f"Found span with text: {text_content}")

            try:
                checkbox_xpath = ".//following::input[@type='checkbox'][1]"  # Finds the first checkbox following the span
                checkbox = span.find_element(By.XPATH, checkbox_xpath)
                
                # Check the checkbox if it's not already checked
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"Checked the checkbox related to: {text_content}")
                else:
                    print(f"Checkbox already checked for: {text_content}")
            
            except Exception as e:
                print(f"Could not find or check the checkbox for: {text_content} - {e}")
    def check_question_type(self):
        print('lol')

    def go_question_iframe(self):
        try:
            iframe_xpath = "//iframe[contains(@title, 'Question Viewer')]"
            iframe_id = "contentFrame"
            iframe_tag = "iframe"
            self.driver.wait_for_all(By.TAG_NAME, iframe_tag)
            question_iframe = self.driver.find_element(By.TAG_NAME, iframe_tag)
            self.driver.switch_to.frame(question_iframe)
            self.driver.implicitly_wait(2)
            log.info("Sucessfully moved into iframe")
        except Exception as e:
            log.error(e)
    
    def get_questions(self):
        #containers
        self.go_question_iframe()
        top_question_container_xpath = "//div[contains(@id, 'top') and contains(@class, 'dijitContentPane')]"
        mc_questions_xpath = "//span[@class='step'][.//div[@data-dojo-type='xl.player.controls.MultipleChoiceAnswer']]" # gets only questions and the mc choieces
        try:
            self.top_question = self.driver.find_element(By.XPATH, top_question_container_xpath)
            self.mc_questions = self.driver.find_elements(By.XPATH, mc_questions_xpath)
            log.info(f"""Top Level Question:
{self.top_question.text.strip()}                
Mc Questions:
{'\n'.join([question.text.strip() for question in self.mc_questions])}
""")
# NEXT TO DO, MAKE SURE THIS WORKS X SEE IF I CAN MAKE SSO NOT REDIRECT OR HOW I CAN SSO WITH SELENIUM
        except AttributeError:
            log.info("No questions found (supported: mc)")
        except Exception as e:
            log.error(f"An error has occured {e}")
        
    def create_driver(self, url=''):
        if self.driver is None:
            self.driver = Site("test")  # Assuming Site is a class that initializes the driver
            # self.login()  # Login after initializing the driver
        if url:
            self.driver.set_url(url)  # Assuming set_url is a method of the Site class


if __name__ == "__main__":
    root = Tk()
    app = HomeworkApp(root)
    root.mainloop()

# this js grabs the data
#     var xpath = "//span[contains(@class, 'rvTxt') and normalize-space(text()) != '']"; // XPath to find span elements with class rvTxt and non-empty text
# var result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

# // Loop through the results, starting from the second item
# for (var i = 0; i < result.snapshotLength; i++) {
#     var textContent = result.snapshotItem(i).textContent; // Get the text content
#     console.log(textContent.trim()); // Print the text content without leading/trailing whitespace
# }


