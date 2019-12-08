import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# from pyvirtualdisplay import Display
script_dir = os.path.dirname(os.path.realpath(__file__)) #<-- absolute dir the script is in
abs_path = script_dir + '\\Data\\'

# test code
def test():
    options = Options()
    options.headless = True
    
    print("starting")
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Chrome(options=options)

    # put the rest of our selenium code in a try/finally
    # to make sure we always clean up at the end
    try:
        print("getting web")
        browser.get('https://www.google.com')
        print(browser.title) #this should print title

    finally:
        browser.quit()
        print("done")

# form_extraction headless
def get_headless():
    options = Options()
    options.headless = True
    prefs = {'download.default_directory' : abs_path}
    options.add_experimental_option('prefs', prefs)
    return options

def get_options():
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : abs_path}
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options

def extract():
    #form_extraction
    start = time.time()
    print("starting browser...")
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Chrome(chrome_options=get_options())

    print("going to www.askform.cn/login ...")
    browser.get("https://www.askform.cn/login")

    print("loggin in...")
    browser.find_element_by_id("un").send_keys("contact.listener@gmail.com")
    browser.find_element_by_id("pwd").send_keys("iamyourlistener")
    browser.find_element_by_xpath(".//a[@onclick='askformLogin()']").click()

    browser.find_element_by_id("menu4603080002").click()

    browser.find_element_by_xpath(".//a[@href='/Survey/DataList.aspx?AppConfigID=4603080002&FormApplicationID=10801670001&FormCategoryID=10833290001&FormID=16128410001']").click()
    print("downloading...")
    browser.find_element_by_id("btnExport").click()

    time.sleep(5)
    browser.close()

    end = time.time()
    print("time: " + str(end - start))

extract()
