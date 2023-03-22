import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import undetected_chromedriver as uc
import time
import datetime
now = datetime.datetime.now()

def track_fedex(track_id):
	options = Options()
	#options.add_argument('--headless')
	driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
	driver.get(f'https://www.fedex.com/fedextrack/?trknbr={track_id}')
	html = driver.page_source
	soup = BeautifulSoup(html,'html5lib')

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, 'tr.travel-history-table__scan-event-details-row:nth-child(3) > td:nth-child(1)'))
	first_option = WebDriverWait(driver, 15).until(condition)
	time_v = first_option.text

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, 'tr.travel-history-table__scan-event-details-row:nth-child(3) > td:nth-child(2)'))
	first_option = WebDriverWait(driver, 15).until(condition)
	location = first_option.text

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, 'tr.travel-history-table__scan-event-details-row:nth-child(3) > td:nth-child(3)'))
	first_option = WebDriverWait(driver, 15).until(condition)
	status = first_option.text
	driver.quit()

	txt = f'Date and time : {time_v}\nLocation : {location}\nStatus : {status}'
	return txt


def track_usps(track_id):
	options = Options()
	#options.add_argument('--headless')
	driver = uc.Chrome(options=options)
	driver.get(f'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={track_id}')

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '.delivery_status > h2:nth-child(2) > strong:nth-child(1)'))
	first_option = WebDriverWait(driver, 15).until(condition)
	status = first_option.text

	try:
		condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '.status_feed > p:nth-child(2)'))
		first_option = WebDriverWait(driver, 5).until(condition)
		location = first_option.text
	except:
		location = ''

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '.status_feed > p:nth-child(1)'))
	first_option = WebDriverWait(driver, 5).until(condition)
	time_v = first_option.text
	driver.quit()
	
	txt = f'Date and time : {time_v}\nLocation : {location}\nStatus : {status}'
	return txt
	

def track_ups(track_id):

	options = Options()
	#options.add_argument('--headless')
	driver = uc.Chrome(options=options)
	driver.get('https://www.ups.com/track?loc=en_US&requester=ST/')

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '#stApp_trackingNumber'))
	first_option = WebDriverWait(driver, 15).until(condition)
	first_option.send_keys(track_id)

	driver.find_element_by_css_selector('#stApp_btnTrack').click()

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '#st_App_View_Details'))
	first_option = WebDriverWait(driver, 15).until(condition)
	first_option.click()

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.tab-header:nth-child(2) > span:nth-child(1)'))
	first_option = WebDriverWait(driver, 15).until(condition)
	first_option.click()

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '#stApp_milestoneActivityLocation0'))
	first_option = WebDriverWait(driver, 15).until(condition)
	status = first_option.text

	condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '#stApp_activitiesdateTime0'))
	first_option = WebDriverWait(driver, 15).until(condition)
	time_v = first_option.text
	driver.quit()

	txt = f'Date and time : {time_v}\nStatus : {status}'
	return txt

def discord_part():
	import os
	import discord
	TOKEN = 'MTA4NzkxMDMzNDg0NjczMDM1MA.G7d5Xw.hcOzTNIx08xj7C3nQ29ICYOHuMq6vmVA5TxFJY'
	guild = '1077964523312517160'

	client = discord.Client()
	log = []
	@client.event
	async def on_message(message):
		if '-track' in message.content:
			line = message.content.split(' ')
			if line[1].lower() == 'fedex':
				try:
					response = track_fedex(line[-1].strip())
					log.append(['fedex',line[-1].strip()])
				except Exception as e:
					print(e)
					response = 'Invalid ID'
			elif line[1].lower() == 'usps':
				try:
					response = track_usps(line[-1].strip())
					log.append(['usps',line[-1].strip()])
				except Exception as e:
					print(e)
					response = 'Invalid ID'
			elif line[1].lower() == 'ups':
				try:
					response = track_ups(line[-1].strip())
					log.append(['ups',line[-1].strip()])
				except Exception as e:
					print(e)
					response = 'Invalid ID'
			else:
				response = 'Invalid Command!'

			final_response = f'@{message.author}'+'\n'+response
			await message.channel.send(final_response)


	current = datetime.datetime.now()
	if current.hour == now.hour+12:
		for h in log:
			if h[0].lower() == 'fedex':
				try:
					response = track_fedex(line[-1].strip())
				except Exception as e:
					print(e)
					response = str(e)

			elif h[0].lower() == 'usps':
				try:
					response = track_usps(line[-1].strip())
				except Exception as e:
					print(e)
					response = str(e)

			elif h[0].lower() == 'ups':
				try:
					response = track_ups(line[-1].strip())
				except Exception as e:
					print(e)
					response = str(e)




	client.run(TOKEN)

discord_part()