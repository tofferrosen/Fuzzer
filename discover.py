"""
file: discover.py
description: Contains functions for performing discovery of a web page
"""
from logger import * # logging output
import requests	# for gettign web pages
import sys
from BeautifulSoup import BeautifulSoup, SoupStrainer	# for parsing web pages
from urlparse import urljoin # for resolving a relative url path to absolute path
from urlparse import urlparse # for parsing the domain of a url


def page_discovery(page, session, common_words_file):
	"""
	craws and guesses pages, including link discovery and page 
	guessing
	"""
	logger.info("Crawling for pages")
	discovered_urls = link_discovery(page.url, session)
	page_guessing(page, session, discovered_urls, common_words_file)

	return discovered_urls
	
def recursive_link_search(url, domain, urls, session, max_depth, depth):
	"""
	helper function for link_discovery
	max_depth + depth is just only so that we can control how
	far we want to recurse, as this is quite a performance dump
	"""
	
	if depth == max_depth:
		return

	# Add page if not seen b4
	if url not in urls:
		logger.info("New page found: " + url)
		urls.append(url)

	page = session.get(url)
	soup = BeautifulSoup(page.content)
	links = soup.findAll('a', href=True)

	for link in links:
		href_absolute = urljoin(page.url, link.get('href'))

		# Only include links in our domain and not seen b4
		if href_absolute.startswith(domain) and href_absolute not in urls:
			recursive_link_search(href_absolute, domain, urls, session, max_depth, depth+1)

	return urls

def link_discovery(url,session):
	"""
	discovers all accessible links in the same domain
	given a page. Returns a list of urls found
	"""
	max_depth = 100 # huge sites -> horrific performance w/ recursion

	parsed_uri = urlparse(url)
	domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
	urls = recursive_link_search(url, domain, [], session, max_depth, 0)
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
	page = session.get(url);
	cookies = session.cookies;

	logger.info("Discovering cookies")

	for cookie in cookies:
		logger.info("--cookie found: %(name)s=%(value)s" % {"name": cookie.name, "value": cookie.value})

	return cookies


	
