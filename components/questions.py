import re
import sys
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from huggingface_hub import InferenceClient

class Question():
    def __init__(self, top_question_container:WebElement, question, answer_elements: List[WebElement]):
        self.top_question_container = top_question_container
        self.question = question
        self.answer_elements = answer_elements 
        with open('token.bin', 'r') as token_file:
            self.TOKEN = token_file.readline()

    def is_valid_mc(self):
        """ This will allow me to not grab items that have Select all that apply (maybe)"""
    
    def format_ai_query(self, top_question, question, answer_items):
        query = f"""
{top_question}
{question}
{answer_items}
Give me ONLY the letter of the correct answer (no explanation) """
        return query

    def query_ai(self, query): 
        if not self.TOKEN:
            print("Sorry no token was found please add one withen token.bin")
            print("Now exiting")
            sys.exit()
        client = InferenceClient(token=self.TOKEN, model="mistralai/Mistral-Nemo-Instruct-2407")
        result = client.text_generation(query)
        return result
    
    def sanitize_text(self, text) -> str:
        return re.sub(r'[\n\u200B\u00A0]', '', text) # newline, wierd white spaces, non-breaking spaces
        # text_array = text.split('\n')
        # also for i, j while <len(text)
        # trying to remove duplicates \nlol\nlol 
        # ai currently not working too well, changed something with the ai (might work now) 
    
    def get_top_question(self):
        full_text = []
        question_xpath = ".//*[contains(@class, 'rvTxt') or contains(@class, 'equation')]"
        question_elements = self.top_question_container.find_elements(By.XPATH, question_xpath)
        for element in question_elements:
            text = element.get_attribute('aria-label')
            if text:
                full_text.append(text)
            else: 
                full_text.append(element.text.strip())
        top_question = ' '.join(full_text).replace(' ,', ',').strip()
        return top_question

    def get_question(self):
        try:
            print("QUESTION -------------------------------")
            # question = self.question_element.text.strip()
            question = self.question
            return question
        except Exception as e:
            print(e)
            
    def get_question_type(self): # why does this always return radio
        print(f"Current question = {self.question}")
        input_types = ['radio', 'alternative'] # can add more
        # answer = self.answer_elements[0] # checks the 1st index FOR ALL of the questons on the page
        print(f"Length of answer elements = {len(self.answer_elements)}")
        for answer in self.answer_elements:
            print("answer that I am checking", answer.text)
            for input_type in input_types:
                try:
                    input_element = answer.find_element(By.XPATH, f".//input[@type='{input_type}']")
                    return input_type
                except Exception as e:
                    print(f"not a {input_type}")
                    continue # allows it to try the next input type
        return None
    
    def get_mc(self): 
        for answer in self.answer_elements:
            try:
                url = answer.find_element(By.XPATH, ".//input[@type='radio']")
                text = url.get_attribute("aria-label") #hehe radio label had text
                sanitized_text = self.sanitize_text(text)
                letter = sanitized_text[0]
                if letter.lower() not in self.letters:
                    return
                print(f"letter = {letter.lower()}")
                self.answers[letter.lower()] = url # pretty sure works
                self.answer_query += sanitized_text + "\n"
            except Exception as e:
                print("Error retrieving text from answer")
                print(e)

        return self.answers, self.answer_query

    def get_answers(self, question_type):
        self.answers = {}
        self.answer_query = ""
        self.letters = "abcdef"
        if question_type == "radio":
            answers, answer_query = self.get_mc()
            return answers, answer_query
        else:
            return {}, ""
    
    def click_answer(self, url: WebElement):
        """Clicks the correct answer based on the text provided"""
        url.click()

