
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






def get_jobs(search_term, num_jobs, verbose):
    
    #'''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    
    #Initializing the webdriver
	options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
	driver = webdriver.Chrome(executable_path="D:\\Users\\H-2\\Documents\\GitHub\\Glassdoor_Scraping\\chromedriver", options=options)
	driver.set_window_size(1120, 1000)

   # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + search_term + '"&locT=C&locId=1146821&locKeyword=Los%20Angeles,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=0&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'


#see if you can automate
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + search_term + '"&locT=C&locId=1146821&locKeyword="' + city_name + '",%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=0&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'

   #california url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data+scientist&sc.keyword=data+scientist&locT=S&locId=2280&jobType='

    # bay area:
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + search_term + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    
    # los angeles region:
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=data%20scientist&locT=C&locId=1146821&locKeyword=Los%20Angeles,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    
    #san diego
	url = 'https://www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP0.htm'
	user = "joemanjoe696@gmail.com" #user email
	passwd = "n368#m89" #user password



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


	page_count = driver.find_element_by_xpath('.//div[@class="cell middle hideMob padVertSm"]').text


	#print(total_pages)

	#page_count = 'Page 1 of 12049'
	text_to_remove = 'Page 1 of '
	page_count = page_count.replace(text_to_remove, "")
	page_count = int(page_count)
	#page_groups = page_count//5 #create subsets

	other_pages = [4 +(d-1)*5 for d in range(1,page_count)]


	for page in other_pages:
		url = "www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP" + str(page) + ".htm"
		print(url)


df = get_jobs("data scientist",10000, True)


#<div class="cell middle hideMob padVertSm"> Page 1 of 12049</div>
#page_count = driver.find_element_by_xpath('.//div[@class="cell middle hideMob padVertSm"]').text
#page_count = page_count - 'Page 1 of '


# page_count = 'Page 1 of 12049'
# text_to_remove = 'Page 1 of '
# page_count = page_count.replace(text_to_remove, "")
# page_count = int(page_count)

# page_groups = page_count//5 #create subsets



# first_page = [1]
# other_pages = [d*5-d for d in range(1,page_count)]
# page_start = first_page + other_pages
# #print(page_start)


#print(str(page_start))
#https://www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP2.htm

#for page in page_start:
#	url = "www.glassdoor.com/Job/california-jobs-SRCH_IL.0,10_IS2280_IP" + str(page) + ".htm"
#	print(url)







#--------------------------------------------------------------------------------#

#the code below works

# page_count = 'Page 1 of 12049'
# text_to_remove = 'Page 1 of '
# page_count = page_count.replace(text_to_remove, "")
# page_count = int(page_count)

# page_groups = page_count/5 #create subsets


# page_counter = 1
# for x in range (0, page_count):
# 	page_list = [1]
# 	new_addition = page_counter + [i]*page_counter
# 	page_list = page_list + page_counter






#make a for loop that starts at 1 and then add the 240 each time
#save this as a list
#create a function to take the list and plug into the IP part


#page_groupings = for page in range (0:page_count, 5)

# print(page_count)
