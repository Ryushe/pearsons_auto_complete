# pearsons auto complete
A little about this app, I know some people that use Pearsons. This site does wonders for the community. However, this one teacher inparticular has pissed me off. Assigning thousands of mc a night (exageration ofc). 

Currently Supported Questions:
- multiple choice 
    - not including the wierd pull down questions

# Info
This app aims to allow students to skip boring ass multiple choice by utilizing ai to do it for them. 

Is this cheating? Ya

Should schools assign college students what is 2+2? No

# Disclaimer
I am NOT responsible for what happens to you or your account if you so chose to use this automation.

# How to use
With all of that out of the way, how do we use this app to help us with school?

1. `pip install -r requirements.txt`
2. make a file named `token.bin` in the root dir and put your ai api key into it
3. `python homeworkapp.py`

## if don't have api key for ai (free)
1. create an account at https://huggingface.co
2. go to profile -> Acess Tokens -> click on create token -> read only -> copy token into `token.bin` file

Thats it!!!!

Now, you will be presented with an interface that has the options:
- set url - entering a url into the box and hitting this will take you to the site
    - you can also just interact with the site like normal
- Go to Canvas - takes you to the canvas login
- Save Cookies - saves login
- Load Cookies - restores login
- Start - navigate to your pearson questions (At the first question you want it to start at)
    - NOTE: it will only go in chronological order
- Pause - Pause the app for whatever reason
- Quit - Exits the app properly

# Trouble shooting
Q: Canvas is stuck on can't load cookies
A:
- ensure cookies are enabled (within chrome settings)
- try resaving cookies and then reloading page
- try navigating to other parts of the site
    -  eg: click on dashboard, groups, etc
- if all else fails delete cookies within chrome settings 
  - click delete cookies button and relaunch app