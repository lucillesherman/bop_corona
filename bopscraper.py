from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.action_chains import ActionChains
import csv


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
browser = webdriver.Chrome(executable_path = "/Users/user/Desktop/nopolitics/coronavirus_counts/chromedriver 2", chrome_options=option)
browser.get("https://www.bop.gov/coronavirus/")


element = browser.find_element_by_xpath('//*[@id="stats"]/h3')

actions = ActionChains(browser)

browser.execute_script("arguments[0].scrollIntoView();", element)
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="totals_breakdown_link"]')))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

browser.find_element_by_xpath('//*[@id="totals_breakdown_link"]').click()

results = browser.page_source
soup = BeautifulSoup(results, "html.parser")
table = soup.find("tbody")

output = [["inmates_positive", "staff_positive", "inmate_deaths", "staff_deaths", "facility", "city", "state"]]

for row in table.find_all('tr'):
    list_of_cells = []
    # print(row)
    for cell in row.find_all('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    output.append(list_of_cells)

import datetime
current_date = datetime.datetime.now()
filename = "bopcovid"+str(current_date.strftime("%Y-%m-%d %H:%M"))

outfile = open(filename + ".csv", "w")
writer = csv.writer(outfile)
writer.writerows(output)
browser.close()