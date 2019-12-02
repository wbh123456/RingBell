import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

#pyanywhere test code
def test():
    with Display():
        # we can now start Firefox and it will run inside the virtual display
        browser = webdriver.Firefox()

        # put the rest of our selenium code in a try/finally
        # to make sure we always clean up at the end
        try:
            browser.get('https://www.google.com')
            print(browser.title) #this should print title

        finally:
            browser.quit()


#form_extraction
c = 0
while (0):

    start = time.time()

	driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.get("https://www.askform.cn/login")

    driver.find_element_by_id("un").send_keys("contact.listener@gmail.com")
    driver.find_element_by_id("pwd").send_keys("iamyourlistener")
    driver.find_element_by_xpath(".//a[@onclick='askformLogin()']").click()

    driver.find_element_by_id("menu4603080002").click()

    driver.find_element_by_xpath(".//a[@href='/Survey/DataList.aspx?AppConfigID=4603080002&FormApplicationID=10801670001&FormCategoryID=10833290001&FormID=16128410001']").click()

    driver.find_element_by_id("btnExport").click()

    time.sleep(5)
    driver.close()

    end = time.time()
    c += 1
    print("time: " + str(end - start))
    print("count: " + str(c))
