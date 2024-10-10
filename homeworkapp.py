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
    def check_question_type(self):
        print('lol')

    def debug(self):
        questions = self.driver.execute_script("""
let elements = document.evaluate("//span[@class='step']/following::div[contains(@class, 'addblank')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

let questions = []
for (let i = 0; i < elements.snapshotLength; i++) {
    console.log(elements.snapshotItem(i).textContent.trim());
    questions.push(elements.snapshotItem(i).textContent.trim())
    }
    return questions""")
    
        for question in questions:
            print(question)

    def js_get_questions(self):
        questions = self.driver.execute_script("""
let elements = document.evaluate("//span[@class='step']/following::div[contains(@class, 'addblank')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

let questions = []
for (let i = 0; i < elements.snapshotLength; i++) {
    console.log(elements.snapshotItem(i).textContent.trim());
    questions.push(elements.snapshotItem(i).textContent.trim())
    }
    return questions""")
    
        for question in questions:
            print(question)
        questions = [""] + questions # try to align the data with the ? 
        return questions

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

            return_questions = []
            mc_containers = self.driver.find_elements(By.XPATH, mc_container_xpath)
            questions = self.js_get_questions() # will be an array
            
            for container, question in zip(mc_containers, questions):
            # for container in mc_containers:
                ## Questions eg: what is the state of florida, Answers eg: * mc1 *mc2
                try:
                    trial_shitter = container.find_elements(By.XPATH, mc_question_xpath) # hopefully inits the rest of the ob
                    # mc_question = questions_to_be_answered[question_index]
                    mc_answer_elements = container.find_elements(By.XPATH, mc_answers_xpath)
                    question_box = Question(top_question_container, question, mc_answer_elements)
                    return_questions.append(question_box)
                except Exception as e:
                    log.error(e)
            del return_questions[0] # trying to align everything
            return return_questions

        except AttributeError:
            log.info("No questions found (supported: mc)")
        except Exception as e:
            log.error(f"{e}")
    
    def get_question_data(self, question: Question):
        #get question and the main question (at the top)
        answer_query = ''
        try: # WORKS
            question_query = question.get_question() 
            top_question = question.get_top_question()
        except Exception as e:
            log.warning("cant get question")
            log.warning(e)
        try:
            question_type = question.get_question_type()
            print(f"question_type = {question_type}")
        except Exception as e:
            print(e)
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

    
    def init_questions(self):
        """Logic behind, can't get 1st then when js with fresh page no work as well"""
        """This aims to find all elements ensuring they all have been touched/initialized"""
        self.driver.find_elements(By.XPATH, "//span[@class='step']/following::div[contains(@class, 'addblank')]")

    def solve_questions(self):
        if not self.in_iframes:
            self.enter_iframes()

        # self.driver.implicitly_wait(3)# should fix not getting 1st wuestion
        self.driver.wait_for_all(By.XPATH, "//span[@class='step']/following::div[contains(@class, 'addblank')]", self.driver)

        page_questions = self.get_mc_questions() 
        for question in page_questions:
            question_data = self.get_question_data(question)
            if question_data:
                if len(question_data) == 4:
                    top_question, question_query, answer_query, answers_dict = question_data
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
                    print(f"For question: {question.get_question()}")
                    print(f"clicking option: {correct_letter}")
                    print(f"url for {correct_letter} is {answers_dict[correct_letter]}")
                    answer = answers_dict[correct_letter]
                    question.click_answer(answer)
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

            # because checking locally, and not getting the question data for the other ? when i check to see what kind of ? it is it uses the one before if it doesn't exist
                # the indexing becomes wrong, due to the questions being longer than the aswer array
                # not sure y - ISSUE is that the data from the ? before gets put into the next ? if no data

            # due to not getting first question, indexes thrown off causing the input 1? == 2a 2? ==3a
                # this leads to the bottom question being a radio, because its given the wrong input

            # not getting 1st qweston pushes everything (getting everything else)
            # issue with this is even me waiting forever, i am not getting it
            # BIG DISCOVERY, elements aernt loaded till clicked on, meaning need to click on an element before i can read anything
                # see if you can click the top section and then if it loads sick 
                    # this would mean clicking the top activates the elements allowing us to pull the top question
                # debug will allow me to test if it works or not or use code below
                """
let elements = document.evaluate("//span[@class='step']/following::div[contains(@class, 'addblank')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

for (let i = 0; i < elements.snapshotLength; i++) {
    console.log(elements.snapshotItem(i).textContent.trim());
}
                """
                
    """
const xpath = "//span[@class='step']/following::div[contains(@class, 'addblank')]";
const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);

let node;
const questions = [];

// Iterate through all matching nodes
while (node = result.iterateNext()) {
    questions.push(node.textContent.trim());  // Push the text content to the array
}

// Print each question's text content to the console
questions.forEach(question => console.log(question));
    """
            
            

if __name__ == "__main__":
    root = Tk()
    app = HomeworkApp(root)
    root.mainloop()
