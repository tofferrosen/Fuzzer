"""
file: discover.py
description: Contains functions for performing discovery of a web page
"""
from logger import * 
import requests
from BeautifulSoup import BeautifulSoup

def page_discovery(page, session):
	"""
	craws and guesses pages, including link discovery and page 
	guessing
	"""
	logger.info("Crawling for pages")
	discovered_urls = link_discovery(page)
	page_guessing(page, session, discovered_urls)

	#print discovered_urls
	

def link_discovery(page):
	"""
	discovers all accessible links in the same domain
	given a page. Returns a list of urls found
	"""
	urls = ['http://127.0.0.1/dvwa/.'] # Root automatically added
	soup = BeautifulSoup(page.content)

	for link in soup.findAll('a'):
		href = page.url + link.get('href')

		# Only include those in our domain and not seen yet
		if "http://" not in link.get('href') and href not in urls: 
			logger.info("New page found: " + href)
			urls.append(href)

	return urls

def page_guessing(page, session, discovered_urls):
	"""
	discovers potentially unlinked pages using common extentions
	"""

	common_ext = open("Guessing/urlExtentions.txt", "r").read().splitlines()
	common_pgs = open("Guessing/pageNames.txt", "r").read().splitlines()

	# We're up all night to get lucky
	for pg in common_pgs:
		for ext in common_ext:
			possible_pg = session.get(page.url + pg + "." + ext)
			if possible_pg.status_code < 300 and possible_pg.url not in discovered_urls:
				logger.info("New page found: " + possible_pg.url)
				discovered_urls.append(possible_pg.url)




	
