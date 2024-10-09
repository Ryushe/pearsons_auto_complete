import re
import sys
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from huggingface_hub import InferenceClient

class Question():
    def __init__(self, top_question_container:WebElement, question_elements: WebElement, answer_elements: List[WebElement]):
        self.top_question_container = top_question_container
        self.question_element = question_elements
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
        if self.TOKEN:
            client = InferenceClient(token=self.TOKEN)
            result = client.text_generation(query)
            return result
        else:
            print("Sorry no token was found please add one withen token.bin")
            print("Now exiting")
            sys.exit()
    
    def sanitize_text(self, text):
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

    def get_mc_answers(self):
        answers = {}
        answer_query = ""
        letters = "abcdef"
        for answer in self.answer_elements:
            try:
                url = answer.find_element(By.XPATH, ".//input[contains(@type, 'radio')]")
                text = url.get_attribute("aria-label") #hehe radio label had text
                sanitized_text = self.sanitize_text(text)
                letter = sanitized_text[0][0]
                if not any(letter in letter.lower() for letter in letters):
                    return
                answers[letter.lower()] = url # pretty sure works
                answer_query += sanitized_text + "\n"
            except Exception as e:
                print("Error retrieving text from answer")

        return answers, answer_query

    def get_question(self):
        try:
            print("QUESTION -------------------------------")
            return self.question_element.text.strip()
        except Exception as e:
            print(e)
            
    
    def click_answer(self, driver, answer_text):
        """Clicks the correct answer based on the text provided"""
        if answer_text in self.answers:
            index = self.answers.index(answer_text)
            answer_id = self.answer_ids[index]
            
            # Find the answer element by its ID and click it
            element = driver.find_element_by_id(answer_id)
            element.click()
        else:
            print(f"Answer '{answer_text}' not found for question '{self.question_text}'.")

