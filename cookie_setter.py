import json
#1. document.cookie
#2. paste into cookie string

def main(cookie_string):
# cookie_string = input("Give me document.cookie output: \n")
    cookies = cookie_string.split('; ')
    formatted_cookies = []
    # Iterate through each cookie and format it into a dictionary
    for cookie in cookies:
        name, value = cookie.split('=', 1)  # Split only on the first '='
        formatted_cookies.append({'name': name, 'value': value})

    # Output the formatted cookies
    try:
        with open('cookies.json', "w") as cookie_file:
            json.dump(formatted_cookies, cookie_file, indent=4)
            # for cookie in formatted_cookies:
            #     cookie_file.write(f"{str(cookie)}\n")
        print("Successfuly wrote to cookies.json")
    except:
        print("Failed to write to cookies.json")
        
    cookie_file.close()
