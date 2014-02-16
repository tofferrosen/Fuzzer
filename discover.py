"""
file: discover.py
description: Contains functions for performing discovery of a web page
"""
from logger import * 
from BeautifulSoup import BeautifulSoup

def page_discovery(page):
	"""
	craws and guesses pages, including link discovery and page 
	guessing
	"""
	logger.info("Crawling for pages")
	urls = link_discovery(page)

	#for url in urls:
		#print url
	

def link_discovery(page):
	"""
	discovers all accessible links in the same domain
	given a page. Returns a list of urls found
	"""
	urls = []
	soup = BeautifulSoup(page.content)

	for link in soup.findAll('a'):
		href = link.get('href')

		# Only include those in our domain and not seen yet
		if "http://" not in href and href not in urls: 
			urls.append(link.get('href'))

	return urls



	
