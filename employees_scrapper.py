from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


#LinkedIn Login
browser = webdriver.Chrome("d:/bannu_anna/drivers/chromedriver")
browser.get('https://www.linkedin.com/uas/login')

#Give Username and Password
username = ""
password = ""


#Giving Username as input
elementID = browser.find_element_by_id("username")
elementID.send_keys(username)


#Giving Password as input
elementID = browser.find_element_by_id("password")
elementID.send_keys(password)
elementID.submit()


#delay for verifying captcha
time.sleep(40)

#Opening given company LinkedIn 
browser.get('https://www.linkedin.com/company/hubspot')


#scrapping a all employees's url from company LinkedIn Page
src_1 = browser.page_source
soup_1 = BeautifulSoup(src_1, 'lxml')
company_employees =  soup_1.find('div', {'class': 'display-flex mt2 mb1'})
links = []
for link in company_employees.findAll('a'):
    links.append(link.get('href'))

company_employees_link = "https://www.linkedin.com/" + links[0] + "&page="


#scrapping employee's LinkedIn url's 
employees_linkedin = []
num = 1
number_of_employees_to_scrap = 100
while len(employees_linkedin)<=number_of_employees_to_scrap:

    browser.get(company_employees_link + str(num))
    src_2 = browser.page_source
    soup_2 = BeautifulSoup(src_2, 'lxml')

    temp = soup_2.find_all('div', {'class': 'display-flex'})
    for i in temp:
        for tag in i.findAll('a', {'aria-hidden':'false'}):
            employees_linkedin.append(tag.get('href'))
    num += 1


#Scrapping employee details
employees_data = []
for employee in employees_linkedin:
    a = []
    browser.get(employee)
    src_3 = browser.page_source
    soup_3 = BeautifulSoup(src_3, 'lxml') 

    employee = soup_3.find_all('div', {'class': 'mt2 relative'})
    name = employee[0].find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().split()    
    first_name = name[0]
    a.append(first_name)
    last_name = name[1]
    a.append(last_name)
    label = employee[0].find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
    a.append(label)
    location = employee[0].find('span', {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
    a.append(location)
    temp_1 = soup_3.findAll('img', {'class': 'pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show ghost-person ember-view'})
    temp_2 = soup_3.findAll('img', {'class': 'pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show ember-view'})
    if temp_1 == []:
        profile_picture = temp_2[0].get('src')
    if temp_2 == []:
        profile_picture = temp_1[0].get('src')
    a.append(profile_picture)
    browser.get(profile_picture)
    employees_data.append(a)


#saving employee details as a pandas dataframe
df = pd.DataFrame(employees_data, columns=['first name', 'last name', 'label', 'location', 'profile picture'])


#converting the pandas dataframe to csv and saving it as "employees_data"
df.to_csv('employees_data.csv', index=False)
