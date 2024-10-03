# todo
- make cookies automatic (getting)
- handle mc choice ?s
    1. get ?
    2. send to gpt using whats in prompt.txt
    3. recieve it and select that ?
    4. check if right
    5. if right move on to next
    - issues:
        - need to make sure ? is right
        - pause if not mc
- random timer (so it doen't complete questions at same interval)

# Notes
For Windows try below
chrome.exe - remote-debugging-port=9111 - no-first-run - no-default-browser-check - user-data-dir="C:\Users\gauravkhurana\AppData\Local\Google\Chrome\User Data"

MAKE SURE TO CHECK TO SEE HOW MANY QUESTIONS THERE ARE - and what question currently on 
1. check to see question type - DONE mc
2. grab the quesion and answers - DONE mc
3. send to chatgpt and wait for response
4. enter chatgpt response
5. check answer
6. if correct move on
    - if no more questions here move to next section
- coiuld grep the question and what part im on, so part 1 I get 1st part, etc etc


# links
[canvas](https://wvc.instructure.com/courses/2508998/external_tools/18367)

playit.gg
ryushe.dev@gmail.com
setup-guest
   
```js
var xpathStep = "//span[contains(@class, 'step') and .//span[contains(@class, 'rvTxt') and normalize-space(text()) != '']]";
var xpathEqText = "//span[contains(@class, 'eqText')]";

// Evaluate XPath for 'step' class
var resultStep = document.evaluate(xpathStep, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

// Evaluate XPath for 'eqText' class
var resultEqText = document.evaluate(xpathEqText, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

// Iterate over the resultStep and resultEqText to get the data
for (var i = 0; i < resultStep.snapshotLength; i++) {
    console.log(resultStep.snapshotItem(i).textContent);
}

for (var i = 0; i < resultEqText.snapshotLength; i++) {
    console.log(resultEqText.snapshotItem(i).textContent);
}
```

NOTE: below is for getting xpaths for top and bottom section, however not needed at curent time
```py
top_question_container_xpath = "//div[contains(@id, 'top')]"
bottom_question_container_xpath = "//div[contains(@id, 'bottom')]"
top_questionn_container = self.hw.find_element(By.XPATH, top_question_container_xpath)
bottom_question_container = self.hw.find_element(By.XPATH, bottom_question_container_xpath)

top_question_xpath = ".//span[contains(@class, 'rvTxt')] or .//span[contains(@class, 'eqDocument')]"
bottom_question_xpath = ".//span[contains(@class, 'rvTxt')]"
```