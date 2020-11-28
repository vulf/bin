#!/usr/bin/python3
# Whatsapp bulk send
# Author: Pranav Sivvam
# Date: 9-11-20
#
# Note:
#   MEMBERS_FILE must contain phone numbers including the country code, e.g, +91xxxxxxxxxx, +97xxxxxxxxxx
#   phone numbers which successfully received the message(s) will be appended to 'sent.out' in the current directory.
#   if 'sent.out' does not exist, it will be created automatically.
#
# Bugs:
#   fix handling of non whatsapp numbers

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import time
import sys

if len(sys.argv) < 3:
    print("Usage: ./wamsg.py MEMBERS_FILE MSG_FILE")
    sys.exit(0)

# get files
MEM_FILE = sys.argv[1]
MSG_FILE = sys.argv[2]

TARGET = list()
with open(MEM_FILE, 'r') as f:
    for line in f:
        TARGET.append(line)

# path to chromedriver
DRV_PATH = 'chromedriver'

driver = webdriver.Chrome(DRV_PATH)

def nextLine():
    return str(ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform())

MSG = ''

with open(MSG_FILE, 'r') as f:
    for line in f:
        MSG += line

# enter numbers with country code, e.g +917283928372
for i in range(len(TARGET)):
        if TARGET[i].startswith('+91'):
            TARGET[i] = TARGET[i][3:]
        TARGET[i] = TARGET[i].replace(' ','')

with open('sent.out', 'a') as f:
    for num in TARGET:
        num = '+91' + num
        print(num)
        driver.get('https://web.whatsapp.com/send?phone='+ num)
        try:
           WebDriverWait(driver, 10).until (EC.alert_is_present())
           alert = driver.switch_to.alert
           alert.accept()
           print("alert is present")
        except TimeoutException:
           print("alert is not present")
        time.sleep(6)
        inp = driver.find_element_by_xpath('//div[@spellcheck="true"][@contenteditable="true"][@dir="ltr"]')
        ActionChains(driver).move_to_element(inp).click(inp).perform()
        for i in range( len(MSG) ):
            if MSG[i] == '\n':
                nextLine()    
            else:
                inp.send_keys(MSG[i])

        inp.send_keys('\n')
        f.write(num)

print('Completed execution. Press enter to exit script')
input()
driver.quit()
