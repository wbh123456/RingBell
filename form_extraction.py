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
def get_headless_options():
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

def extract(is_listener):
    #form_extraction
    start = time.time()
    print("starting browser...")
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Chrome(chrome_options=get_options())

    print("going to www.askform.cn/login ...")
    browser.get("https://www.askform.cn/login")

    print("loggin in...")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[3]/div[2]/input").send_keys("contact.listener@gmail.com")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[4]/div/input").send_keys("iamyourlistener")
    # on old website
    # browser.find_element_by_id("emailOrTel").send_keys("contact.listener@gmail.com")
    # browser.find_element_by_id("password").send_keys("iamyourlistener")

    browser.find_element_by_xpath(".//a[@onclick='askformLogin()']").click()

    browser.find_element_by_id("menu4603080002").click()
    if is_listener:
        #this link in wrong!! Need to be changed in the future
        browser.find_element_by_xpath(".//a[@href='/Survey/DataList.aspx?AppConfigID=4603080002&FormApplicationID=10801670001&FormCategoryID=10833290001&FormID=16128410001']").click()
    else:
        browser.find_element_by_xpath(".//a[@href='/Survey/DataList.aspx?AppConfigID=4603080002&FormApplicationID=10244540001&FormCategoryID=10276160001&FormID=14461000001']").click()
    print("downloading...")
    browser.find_element_by_id("btnExport").click()

    time.sleep(5)
    browser.close()

    end = time.time()
    print("time: " + str(end - start))

def organize_form():
    #delete downloaded file
    os.remove(abs_path + "oldForm.xls")
    os.rename(abs_path + "newForm.xls", abs_path + "oldForm.xls")
    os.rename(abs_path + "数据列表.xls", abs_path + "newForm.xls")
    print("Successfully organizes the forms!")

if __name__ == '__main__':
    extract(is_listener = False)
