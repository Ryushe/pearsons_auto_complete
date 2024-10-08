import re
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from huggingface_hub import InferenceClient

class Question():
    def __init__(self, top_question_element:WebElement, question_elements: WebElement, answer_elements: List[WebElement]):
        self.top_question_element = top_question_element
        self.question_element = question_elements
        self.answer_elements = answer_elements 

    def is_valid_mc(self):
        """ This will allow me to not grab items that have Select all that apply (maybe)"""
    
    def format_ai_query(self, top_question, question, answers):
        print(f"{top_question}\n{question}\n{answers}")
        return f"{top_question}\n{question}\n{answers}\nthese are labled A, B, C and D in vertical order, give me your answer as the question letter (example: A) "

    def query_ai(self, payload): ## right now just a simple question, will eventually make
        with open('token.bin', 'r') as token_file:
            TOKEN = token_file.readline()
        client = InferenceClient(token=TOKEN)
        result = client.text_generation(payload, max_new_tokens=12)
        return result
    
    def sanitize_text(self, text):
        return re.sub(r'[\n\u200B]', '', text)
        # text_array = text.split('\n')
        # also for i, j while <len(text)
        # trying to remove duplicates \nlol\nlol 
        # ai currently not working too well, changed something with the ai (might work now) 
    
    def get_top_question(self):
        full_text = []
        question_elements = self.top_question_element.find_elements(By.CSS_SELECTOR, '.rvTxt, .equation')
        for element in question_elements:
            text = element.get_attribute('aria-label')
            if text:
                full_text.append(text)
            else: 
                full_text.append(element.text.strip())
        return ' '.join(full_text).replace(' ,', ',').strip()


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
                answers[letter] = {sanitized_text:url} # pretty sure works
                answer_query += sanitized_text + "\n"
                print(f"""
answer radio url =  {url}
answer text = {sanitized_text}
letter = {letter}\n""")
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

