from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.by import By
import time
from time import sleep
from helper import search_jobs
from helper import read_listings
import pandas as pd


#from selenium.webdriver.common.action_chains import ActionChains #(https://stackoverflow.com/questions/55571838/error-message-element-not-interactable-selenium-webdriver)



    
'''Gathers jobs as a dataframe, scraped from Glassdoor'''
num_jobs = 160

#Initializing the webdriver
options = webdriver.ChromeOptions()

#Uncomment the line below if you'd like to scrape without a new Chrome window every time
#options.add_argument('headless')

#Change the path to where chromedriver is in your home folder
driver = webdriver.Chrome(executable_path="D:\\Users\\H-2\\Documents\\GitHub\\Glassdoor_Scraping\\chromedriver", options=options)
driver.set_window_size(1120, 1000)


url = 'https://www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP0.htm'
user = #insert user email in quotation marks
passwd = #insert password in quotation marks



driver.get(url)
jobs = []

time.sleep(5)

#Signing In
driver.find_element_by_xpath("//a[@href='/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK']").click()

username = driver.find_element_by_id("userEmail")
username.clear()
username.send_keys(user)


password = driver.find_element_by_id("userPassword")
password.clear()
password.send_keys(passwd)


#Click the sign-in button

driver.find_element_by_xpath("//button[@class='gd-ui-button minWidthBtn css-1sdotxz']").click()



while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

    #Let the page load. Change this number based on your internet speed.
    #Or, wait until the webpage is loaded, instead of hardcoding it.
    time.sleep(6)

    ##line below is not always necessary. use when popup appears
    #driver.find_element_by_xpath("//path[@id='prefix__icon-close-1']").click()

    
    #Going through each job in this page
    #job_buttons = driver.find_elements_by_xpath("//li[@class='jl']").click()

    job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
    for job_button in job_buttons:  

        print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
        if len(jobs) >= num_jobs:
            break

        try:
            job_button.click()

        except (ElementClickInterceptedException):
            try: 
                job_button.click()
            except (ElementClickInterceptedException):
                job_button.click()


        time.sleep(3)
        collected_successfully = False
        
        while not collected_successfully:
            try:
                company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                location = driver.find_element_by_xpath('.//div[@class="location"]').text
                job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                collected_successfully = True
            except:
                time.sleep(2)

        try:
            salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
        except NoSuchElementException:
            salary_estimate = -1 #You need to set a "not found value. It's important."
        
        try:
            rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
        except NoSuchElementException:
            rating = -1 #You need to set a "not found value. It's important."

        #Printing for debugging
        print("Job Title: {}".format(job_title))
        print("Salary Estimate: {}".format(salary_estimate))
        print("Job Description: {}".format(job_description[:500]))
        print("Rating: {}".format(rating))
        print("Company Name: {}".format(company_name))
        print("Location: {}".format(location))

        #Going to the Company tab...
        #clicking on this:
        try:
            driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

            try:
                headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
            except NoSuchElementException:
                headquarters = -1

            try:
                size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
            except NoSuchElementException:
                revenue = -1

            try:
                competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            except NoSuchElementException:
                competitors = -1

        except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
            headquarters = -1
            size = -1
            founded = -1
            type_of_ownership = -1
            industry = -1
            sector = -1
            revenue = -1
            competitors = -1

            
        print("Headquarters: {}".format(headquarters))
        print("Size: {}".format(size))
        print("Founded: {}".format(founded))
        print("Type of Ownership: {}".format(type_of_ownership))
        print("Industry: {}".format(industry))
        print("Sector: {}".format(sector))
        print("Revenue: {}".format(revenue))
        print("Competitors: {}".format(competitors))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        jobs.append({"Job Title" : job_title,
        "Salary Estimate" : salary_estimate,
        "Job Description" : job_description,
        "Rating" : rating,
        "Company Name" : company_name,
        "Location" : location,
        "Headquarters" : headquarters,
        "Size" : size,
        "Founded" : founded,
        "Type of ownership" : type_of_ownership,
        "Industry" : industry,
        "Sector" : sector,
        "Revenue" : revenue,
        "Competitors" : competitors})
        #add job to jobs
    #except NoSuchElementException:
     #   print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
      #  break
df = pd.DataFrame(jobs)

df.to_csv('jobs0.csv') 


        # #Clicking on the "next page" button
        # try:
        #     page_count = driver.find_element_by_xpath('.//div[@class="cell middle hideMob padVertSm"]').text
        #     text_to_remove = 'Page 1 of '
        #     page_count = page_count.replace(text_to_remove, "")
        #     page_count = int(page_count)
        
        #     other_pages = [4 +(d-1)*5 for d in range(1,page_count)]


        #     for page in other_pages:
        #         url = "www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP" + str(page) + ".htm"
            
#Creating Subsequent Files
    
jobs = []

time.sleep(5)

page_count = driver.find_element_by_xpath('.//div[@class="cell middle hideMob padVertSm"]').text
text_to_remove = 'Page 1 of '
page_count = page_count.replace(text_to_remove, "")
page_count = int(page_count)
other_pages = [4 +(d-1)*5 for d in range(1,page_count)]

for page in other_pages:
    url = "https://www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP" + str(page) + ".htm"
    #new_url_str = "IP" + str(page)
    #currentURL  = driver.current_url()
    #editURL = currentURL.replace("IP0", new_url_str)
    driver.get(url)

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(6)

        ##line below is not always necessary. use when popup appears
        #driver.find_element_by_xpath("//path[@id='prefix__icon-close-1']").click()

        
        #Going through each job in this page
        #job_buttons = driver.find_elements_by_xpath("//li[@class='jl']").click()

        job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            try:
                job_button.click()

            except (ElementClickInterceptedException):
                try: 
                    job_button.click()
                except (ElementClickInterceptedException):
                    job_button.click()


            time.sleep(3)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(2)

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            print("Job Title: {}".format(job_title))
            print("Salary Estimate: {}".format(salary_estimate))
            print("Job Description: {}".format(job_description[:500]))
            print("Rating: {}".format(rating))
            print("Company Name: {}".format(company_name))
            print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            print("Headquarters: {}".format(headquarters))
            print("Size: {}".format(size))
            print("Founded: {}".format(founded))
            print("Type of Ownership: {}".format(type_of_ownership))
            print("Industry: {}".format(industry))
            print("Sector: {}".format(sector))
            print("Revenue: {}".format(revenue))
            print("Competitors: {}".format(competitors))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs


        #except NoSuchElementException:
         #   print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
          #  break

        df = pd.DataFrame(jobs)
        #try:
        value = page*2/10
        value = str(value)
        df.to_csv('jobs'+ value + '.csv')
        # d = int(d)
        # d +=1 
        # d = str(d)








       # except
        #df.to_csv('jobs'+ d + 'real' + '.csv')









# page_count = driver.find_element_by_xpath('.//div[@class="cell middle hideMob padVertSm"]').text
# text_to_remove = 'Page 1 of '
# page_count = page_count.replace(text_to_remove, "")
# page_count = int(page_count)
# other_pages = [4 +(d-1)*5 for d in range(1,page_count)]

# for page in other_pages:





































#             driver.find_element_by_xpath('.//li[@class="next"]//a').click()
#         except NoSuchElementException:
#             print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
#             break

#     return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

# df = get_jobs(160, True)
# df.to_csv('data_science_jobs_bakersfield.csv') 




# page_count = 'Page 1 of 12049'
# text_to_remove = 'Page 1 of '
# page_count = page_count.replace(text_to_remove, "")
# page_count = int(page_count)

# page_groups = page_count//5 #create subsets



# first_page = [1]
# other_pages = [d+5 for d in range(1,page_count)]
# page_start = first_page + other_pages
# print(page_start)


# for page in page_start:
    



# # page_groupings = for page in range (0:page_count, 5)
# # print(page_groupings)

# page_count = 'Page 1 of 12049'
# text_to_remove = 'Page 1 of '
# page_count = page_count.replace(text_to_remove, "")
# page_count = int(page_count)

# page_groups = page_count//5 #create subsets




# page_start = [d+5 for d in range(1,page_count)]
# print(page_start)




# <input type="hidden" id="TotalPages" value="11834">

# total_pages = driver.FindElement(By.Id("TotalPages")).GetAttribute("value")

# <li class="page ">
# <a href="/Job/california-jobs-SRCH_IL.0,10_IS2280_IP2.htm">2</a></li> #IP indicates page number



# for i in range (0,11):
#     if i < 


# each csv will have 5 pages of informations