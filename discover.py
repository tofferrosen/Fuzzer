"""
file: discover.py
description: Contains functions for performing discovery of a web page
"""
from logger import * 
import requests
import sys
from BeautifulSoup import BeautifulSoup, SoupStrainer

def page_discovery(page, session, common_words_file):
	"""
	craws and guesses pages, including link discovery and page 
	guessing
	"""
	logger.info("Crawling for pages")
	discovered_urls = link_discovery(page)
	page_guessing(page, session, discovered_urls, common_words_file)

	return discovered_urls
	

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

def page_guessing(page, session, discovered_urls, common_words_file):
	"""
	discovers potentially unlinked pages using common extentions
	"""

	common_ext = open("Guessing/urlExtentions.txt", "r").read().splitlines()

	try:
		common_pgs = open(common_words_file, "r").read().splitlines()
	except:
		logger.error("list of common words file not found: " + common_words_file)
		return


	# We're up all night to get lucky
	for pg in common_pgs:
		for ext in common_ext:
			possible_pg = session.get(page.url + pg + "." + ext)
			if possible_pg.status_code < 300 and possible_pg.url not in discovered_urls:
				logger.info("New page found: " + possible_pg.url)
				discovered_urls.append(possible_pg.url)

def input_discovery(url, session):
	"""
	crawls a page to discover all possible ways to input data into the system
	"""
	
	logger.info("Discovering inputs for %s" % (url))
	
	form_parameter_discovery(url, session)
	cookie_discovery(url, session)
	
	return
	
def form_parameter_discovery(url, session):
	page = session.get(url)
	soup = BeautifulSoup(page.content)
	
	for input_field in soup.findAll('input'):
		if input_field.has_key('name'):
			logger.info("--input field '%s' found" % (input_field['name']))
	
	'''for field in BeautifulSoup(content, parseOnlyThese=SoupStrainer('input')):
		if field.has_key('name'):
			logger.info("  input field '%s' found" % (field['name']))

	return'''
	
def cookie_discovery(url, session):
	return


	
