
##################################################################################################
                           #Web scrapping using selenium 
##################################################################################################

######################################################
#importing the libraries for Web Scrapping
######################################################

import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json


######################################################
#importing the libraries for MongoDB
######################################################
import pymongo

#################################################################################
#This is the class for Web Scrapping
###################################################################################

class webScrap:

	def __init__(self):

		self.help=" This is wrapper class is for web scrapping"

	#############################################################################
	#installClick function install the driver and select the options using selenium
	############################################################################


	def installClick(self,driver):

		try:
		

			#selecting the causeList from the webpage
			driver.get('https://dsscic.nic.in/cause-list-report-web/registry_cause_list/1')

			#selecting the cause list from the data
			driver.find_element_by_css_selector("input[type='radio'][value='appCom']").click()

			#select the option Yashvardhan kumar sinha 
		
			element_comm=driver.find_element_by_id('commissionname')
			for option in element_comm.find_elements_by_tag_name('option'):
				if(option.text=='Yashvardhan Kumar Sinha'):
					option.click()
					break


			#select the public authority 

			element_seach=driver.find_element_by_id('seach_type')
			for options in element_seach.find_elements_by_tag_name('option'):
				if(options.text=='Public Authority'):
					options.click()
					break


			#sending the start and end date keys 
			driver.find_element_by_xpath('//*[@id="fromdate"]').send_keys('01/05/2019')
			driver.find_element_by_xpath('//*[@id="todate"]').send_keys('23/10/2020')


			#clicking on the search button 
			driver.find_element_by_xpath('//*[@id="search_button"]').click()

		except Exception as error:

			print("error occured while installing : - "+str(error))


	#########################################################################################################
	#fetchingTables function scrap the table data from the webpage and return the data in the form of dictionary
	###########################################################################################################

	def fetchingTables(self,driver):

		try:

			res=driver.find_elements_by_tag_name('th')

			headers_append=[data.text for data in res]


			headers_length=len(headers_append[2:])

			list1=[]

			pagecount=0

			while pagecount<10:

				rdata=driver.find_elements_by_tag_name('td')

				rows_data=[data.text for data in rdata]

				for i in range(0,len(rows_data),headers_length):

					list1.append(rows_data[i:i+headers_length])

				try:
					driver.find_element_by_xpath('//*[@id="wrapperContent"]/div/div[2]/div[3]/div[2]/nav/div[2]/ul/li[11]/a').click()
		
					pagecount=pagecount+1

				except Exception as error:
		
					print("error occured while fetchingTables : "+str(error))

			df=pd.DataFrame(list1,columns=headers_append[2:])

			df=df.rename(columns={df.columns[0]:'SL NO',df.columns[1]:'FILE NO'},inplace=False)

			data_dict=df.to_json(orient="records")

			data_dict_result=json.loads(data_dict)

			return data_dict_result

		except Exception as error:

			print("error occured:- "+str(error))

		



##################################################################################
#This is the class for Mongo DB operation
##################################################################################


class opsDB:

	def __init__(self):

		self.help="This weapper class is for creating the database and inserting the data into database"

	def createInsert(self,data):
		
		try:
			
			myclient=pymongo.MongoClient("mongodb://localhost:27017/")

			mydb=myclient["mydatabase"]

			mycol=mydb["webcollection"]


			#inserting the data

			data_inserted=mycol.insert_many(data)


			results=data_inserted.inserted_ids

			result=[data for data in mycol.find()]


			return result

			#return results

		except Exception as error:

			print("error occured while inserting the data :"+str(error))




if __name__=='__main__':

	#initailzing the driver

	driver=webdriver.Chrome(ChromeDriverManager().install())

	#creating object for class webScrap

	web_obj=webScrap()

	#calling the function installClick

	web_obj.installClick(driver)

	#calling the function fetchingTables

	data=web_obj.fetchingTables(driver)

	#creating the object for the DB
	#print(data)

	#print(data)

	db_obj=opsDB()

	#creating and inserting the data to the database

	res=db_obj.createInsert(data)

	print(res)
