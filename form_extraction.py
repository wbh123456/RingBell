import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from pyvirtualdisplay import Display
script_dir = os.path.dirname(os.path.realpath(__file__)) #<-- absolute dir the script is in
abs_path = script_dir + '/Data/'

def get_options():
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : abs_path}
    chrome_options.headless = True
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options

def extract(is_listener):
    username_xpath = "/html/body/div[1]/div[1]/div/div[3]/div[2]/input"
    pwd_xpath = "/html/body/div[1]/div[1]/div/div[4]/div/input"
    login_button_xpath = ".//a[@onclick='askformLogin()']"
    form_menu_id = "menu4603080002"
    bell_ringer_form_xpath = ".//a[@href='/Survey/DataList.aspx?AppConfigID=4603080002&FormApplicationID=10244540001&FormCategoryID=10276160001&FormID=14461000001']"
    download_button_id = "btnExport"

    # If file already exits, delete it
    if os.path.exists(abs_path + "数据列表.xls"):
        os.remove(abs_path + "数据列表.xls")

    #form_extraction
    start = time.time()
    print("Starting browser...")
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Chrome(chrome_options=get_options())

    print("Going to www.askform.cn/login ...")
    browser.get("https://www.askform.cn/login")

    print("Loggin in...")
    try:
        element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, username_xpath))
        )
        element.send_keys("contact.listener@gmail.com")

        element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, pwd_xpath))
        )
        element.send_keys("iamyourlistener")

        element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_button_xpath))
        )
        element.click()

        print("Looking for form...")
        element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, form_menu_id))
        )
        element.click()
        
        if is_listener:
            #this link in wrong!! Need to be changed in the future
            element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//a[@href='/Survey/DataList.aspx?AppConfigID=4603080002&FormApplicationID=10801670001&FormCategoryID=10833290001&FormID=16128410001']"))
            )
            element.click()
        else:
            element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, bell_ringer_form_xpath))
            )
            element.click()

        
        print("Downloading...")
        element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, download_button_id))
        )
        element.click()
        time.sleep(5)
        browser.close()

    finally:
        browser.quit()

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
