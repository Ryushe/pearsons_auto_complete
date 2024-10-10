import tkinter as Tk
import time
from typing import List
from tkinter.ttk import *
from tkinter import *
from utils import *
import logging
import json
import pickle
from components.questions import Question

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(levelname)s: %(message)s',  
    handlers=[
        logging.FileHandler('log.log'),  
        logging.StreamHandler()  
    ]
)

log = logging.getLogger(__name__) 
logging.getLogger('selenium').setLevel(logging.WARNING)

class HomeworkApp:
    def __init__(self, root, driver=''):
        self.root = root
        self.root.title("Homework Helper")
        self.frm = Frame(root)
        self.frm.grid(padx=10, pady=10)
    
        self.driver = None

        self.url_var = StringVar()
        self.cookie_file = "cookies.pkl"
        self.in_iframes = False

        self.setup_ui()
    
    def show_current_url(self):
        if self.driver is not None:
            current_url = self.driver.current_url  # No parentheses needed
            # Update the label with the current URL
            self.url_label.config(text=f"Current Url: {current_url}")  
    

    def setup_ui(self):
        main_pady=3
        main_padx=3
        #row 0
        Label(self.frm, text="Enter HW URL:").grid(column=0, row=0, sticky=W, padx=main_padx, pady=main_pady)
        Entry(self.frm, textvariable=self.url_var).grid(column=1, row=0, sticky=W, padx=main_padx, pady=main_pady)
        
        #row 1
        Button(self.frm, text="Set URL", command=self.set_url, width=15).grid(column=0, row=1, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Canvas w/ cookies", command=self.load_cookies, width=15).grid(column=1, row=1, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Save Cookies", command=self.save_cookies, width=15).grid(column=2, row=1, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Delete Cookies", command=self.delete_cookies, width=15).grid(column=3, row=1, sticky=W, padx=main_padx, pady=main_pady)
        #row 2
        Button(self.frm, text="Solve Questions", command=self.solve_questions, width=15).grid(column=0, row=2, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Pause", command=self.root.destroy, width=15).grid(column=1, row=2, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Quit", command=self.root.destroy, width=15).grid(column=2, row=2, sticky=W, padx=main_padx, pady=main_pady)
        Button(self.frm, text="Debug ", command=self.debug, width=15).grid(column=3, row=2, sticky=W, padx=main_padx, pady=main_pady)
    
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
            log.info("Saved Cookies")
            file.close()
        except Exception as e:
            log.error(e)
    
    def delete_cookies(self):
        try:
            if os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)
            self.driver.delete_all_cookies()
        except Exception as e:
            log.info("Error clearing cookies")

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
    
    def create_site(self):
        if self.driver == None:
            self.driver = Site("profile")

    def set_url(self, url=""):
        self.create_site()
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
    
    def do_multiple_choice(self):
        print("lol")
    
    def do_checkboxes(self): # Place holder code
        xpath_for_span = "//span[contains(@class, 'rvTxt') and normalize-space(text()) != '']"
        spans = self.driver.find_elements(By.XPATH, xpath_for_span)

        for span in spans:
            text_content = span.text.strip()
            log.info(f"Found span with text: {text_content}")

            try:
                checkbox_xpath = ".//following::input[@type='checkbox'][1]"  # Finds the first checkbox following the span
                checkbox = span.find_element(By.XPATH, checkbox_xpath)
                
                # Check the checkbox if it's not already checked
                if not checkbox.is_selected():
                    checkbox.click()
                    log.info(f"Checked the checkbox related to: {text_content}")
                else:
                    log.info(f"Checkbox already checked for: {text_content}")
            
            except Exception as e:
                print(f"Could not find or check the checkbox for: {text_content} - {e}")

    def debug(self):
        question = Question('path', 'answer')
        answer = question.query_ai("What is the color of the sky?") # right now will be preset what is color of sky
        print(answer)

    def enter_iframes(self):
        log.info("title: " + self.driver.title)
        # enter 1st iframe
        try:
            iframe1_xpath = "//iframe[contains(@title, 'Question Viewer')]"
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, iframe1_xpath))
            log.info("sucessfully entered 1st iframe")
        except Exception as e:
            log.info("couldnt get into the 1st iframe")
            return
        # enter 2nd iframe (questions/answers/selection for more questions)
        try:
            iframe2_xpath = "//iframe[contains(@id, 'activityFrame')]"
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, iframe2_xpath))
            log.info("sucessfully entered 2st iframe")
        except Exception as e:
            log.info("couldnt get into the 2st iframe")
            return
        self.in_iframes = True
    
    def get_mc_questions(self) -> List[Question]:
        # mc_wait_path = "//span[@class='step']/following::div[contains(@class, 'addblank')]"
        # self.driver.wait_for(By.XPATH, mc_wait_path)
        #containers
        top_question_container_xpath = "//div[contains(@id, 'top') and contains(@class, 'dijitContentPane')]"
        mc_container_xpath = "//span[@class='step']"
        mc_question_xpath = "./following::div[contains(@class, 'addblank')]"
        mc_answers_xpath = ".//div[@data-dojo-type='xl.player.controls.MultipleChoiceAnswer']" # gets only questions and the mc choieces
        # remember can use the choices to get the answer AND the radio button
        # NOTE: check if mc_choices_xpath gets questions ONLY if they have a radio button (q6 on 2ptb i believe had a select all that apply) - could filter that out and only send it if it doesn't have select all that apply
        #
        try:
            top_question_container = self.driver.find_element(By.XPATH, top_question_container_xpath)

            questions = []
            mc_containers = self.driver.find_elements(By.XPATH, mc_container_xpath)
            for container in mc_containers:
                ## Questions eg: what is the state of florida, Answers eg: * mc1 *mc2
                try:
                    mc_question_element = container.find_element(By.XPATH, mc_question_xpath)
                    mc_answer_elements = container.find_elements(By.XPATH, mc_answers_xpath)
                    question_box = Question(top_question_container, mc_question_element, mc_answer_elements)
                    questions.append(question_box)
                except:
                    log.info("question invalid, skipped")
                    log.error(e)
            return questions

        except AttributeError:
            log.info("No questions found (supported: mc)")
        except Exception as e:
            log.error(f"{e}")
    
    def get_question_query(self, question: Question):
        #get question and the main question (at the top)
        answer_query = ''
        try:
            question_query = question.get_question() 
            top_question = question.get_top_question()
            question_type = question.get_question_type()
            print(f"question_type = {question_type}")
            if question_type is None:
                return None
        except Exception as e:
            log.warning("cant get question")
            log.warning(e)
        #get answers & dict
        try:
            # could check to see if question exists before this (limiting ai calls)
            answers_dict, answer_query = question.get_answers(question_type)
        except Exception as e:
            log.warning("cant get answers")
            log.warning(e)
        
        if answer_query:
            return top_question, question_query, answer_query, answers_dict 
        else: 
            return None

    def solve_questions(self):
        if not self.in_iframes:
            self.enter_iframes()
        page_questions = self.get_mc_questions() 
        for question in page_questions: # on the page
            question_query = self.get_question_query(question)
            if question_query:
                if len(question_query) == 4:
                    top_question, question_query, answer_query, answers_dict = question_query
                else:
                    log.info("question didn't have every attribute, skipping")
                    continue 
            else:
                continue

            #query ai
            try:
                log.info("Getting answer from ai")
                time.sleep(3)
                ai_query = question.format_ai_query(top_question, question_query, answer_query)
                print("ai query = ", ai_query)
                response = question.query_ai(ai_query)
                time.sleep(3)
                print(f"response = {response}")
            except:
                log.warning("error querying the ai\n")
            
            try:
                correct_letter = response.lstrip()[0].lower() # gets abc.. (removes ' ')
                if correct_letter.isalpha(): # is response a letter
                    print(f"letter: {correct_letter} is valid")
                    print(f"url for {correct_letter} is {answers_dict[correct_letter]}")
                else: 
                    print(f"{correct_letter} not a letter")
            except Exception as e:
                print("Something happened when comparing a the letter")
                print(e)
                
            # AI works
            # ai still cooked FUCK ME (wrong answers and sometimes have a random :) - just need better ai
            # make only get mc questions (error in get_type logic): keeps the last type
            # INSTEAD of how im handling the answers, i could search for "the correct answer is"...
            # make click if response.lower() == letter
            

if __name__ == "__main__":
    root = Tk()
    app = HomeworkApp(root)
    root.mainloop()
