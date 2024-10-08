import sys
import requests
from typing import List
from selenium.webdriver.remote.webelement import WebElement

class Question():
    def __init__(self, question_elements: WebElement, answer_elements: List[WebElement]):
        self.question_element = question_elements
        self.answer_elements = answer_elements 

    def is_valid_mc(self):
        """ This will allow me to not grab items that have Select all that apply (maybe)"""
    
    
    def hugging_face(self, payload): ## right now just a simple question, will eventually make
        with open('token.bin', 'r') as token_file:
            TOKEN = token_file.readline()
        try:
            API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
            headers = {"Authorization": f"Bearer {TOKEN}"}
        except Exception as e:
            print(e)
            return
        json_payload = {"inputs":payload}
        response = requests.post(API_URL, headers=headers, json=json_payload)
        return response.json()

        # need to refactor text
    
    def get_answers(self) -> List[str]:
        # try inner--outer html
        # need to make a dictionary item
        answers = []
        for answer in self.answer_elements:
            try:
                # answer_letter = 
                answers.append(answer.text.strip())
                print('answer radio url = ', answer.find_element(By.XPATH, ".//input[contains(@type, 'radio')]"))
            except Exception as e:
                print("Error retrieving text from answer")
        return answers
    
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

