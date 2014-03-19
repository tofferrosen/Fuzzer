"""
file: discover.py
description: Contains functions for performing discovery of a web page
"""
from logger import * # logging output
import requests	# for getting web pages
import sys
from BeautifulSoup import BeautifulSoup, SoupStrainer	# for parsing web pages
from urlparse import urljoin # for resolving a relative url path to absolute path
from urlparse import urlparse # for parsing the domain of a url
from custom_auth import * # Read in all hardcoded authentication


def page_discovery(page, session, common_words_file, auth):
	"""
	crawls and guesses pages, including link discovery and page 
	guessing
	"""
	logger.info("Crawling for pages")
	discovered_urls = link_discovery(page, session, auth)
	page_guessing(page, session, discovered_urls, common_words_file, auth)

	return discovered_urls, session

def dvwa_relogin(session, url):
	"""
	Login back to the dvwa application, and return the
	page attempted (passed in) whose url was redirected to
	the login screen and the new session
	"""

	username = custom_auth["dvwa"]["username"]
	password = custom_auth["dvwa"]["password"]

	# Details to be posted to the login form
	payload = {
		"username": username,
		"password": password,
		"Login": "Login"
	}

	session = requests.Session()
	session.post(custom_auth["dvwa"]["login_url"], data=payload)
	page = session.get(url + "/" + "dvwa")

	# set the security cookie to low!
	cookies = session.cookies
	session_id = cookies["PHPSESSID"]
	session.cookies.clear() # clear the cookies in the cookie

	session.cookies["PHPSESSID"] = session_id
	session.cookies["security"] = "low"

	return session.get(url), session
	
def recursive_link_search(url, domain, urls, session, max_depth, depth, auth):
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

	# check if we are dvwa, if we have been redirected to login page
	if "http://127.0.0.1/dvwa/login.php" in page.url and "logout.php" not in url \
		and "dvwa/login" not in url and auth == "dvwa":
		logger.info("relogging back to dvwa")
		page, session = dvwa_relogin(session, url)

	soup = BeautifulSoup(page.content)
	links = soup.findAll('a', href=True)

	for link in links:
		href_absolute = urljoin(page.url, link.get('href'))

		# Only include links in our domain and not seen b4
		if href_absolute.startswith(domain) and href_absolute not in urls:
			recursive_link_search(href_absolute, domain, urls, session, max_depth, depth+1, auth)

	return urls

def link_discovery(page,session, auth):
	"""
	discovers all accessible links in the same domain
	given a page. Returns a list of urls found
	"""
	max_depth = 100 # huge sites -> horrific performance w/ recursion

	parsed_uri = urlparse(page.url)
	domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
	urls = recursive_link_search(page.url, domain, [], session, max_depth, 0, auth)

	return urls


def page_guessing(page, session, discovered_urls, common_words_file, auth):
	"""
	discovers potentially unlinked pages using common extentions
	"""

	common_ext = open("Resources/urlExtentions.txt", "r").read().splitlines()

	try:
		common_pgs = open(common_words_file, "r").read().splitlines()
	except:
		logger.error("list of common words file not found: " + common_words_file)
		return


	# We're up all night to get lucky
	for pg in common_pgs:
		for ext in common_ext:
			possible_pg = session.get(page.url + pg + "." + ext)

			# check if we are dvwa, if we have been redirected to login page
			if "http://127.0.0.1/dvwa/login.php" in possible_pg.url and "logout.php" not in page.url and auth == "dvwa":
				possible_pg, session = dvwa_relogin(session, possible_pg.url)

			# is this possible page not been seen before?
			if possible_pg.status_code < 300 and possible_pg.url not in discovered_urls:
				logger.info("New page found: " + possible_pg.url)

				discovered_urls.append(possible_pg.url)

def input_discovery(url, session, auth):
	"""
	crawls a page to discover all possible ways to input data into the system
	"""
	
	logger.info("Discovering inputs for %s" % (url))
	forms, session = form_discovery(url, session, auth)
	cookies, session = cookie_discovery(url, session, auth)
	
	return { 'cookies': cookies, 'forms': forms }, session
	
def form_discovery(url, session, auth):

	page = session.get(url)

	# check if we are dvwa, if we have been redirected to login page
	if "http://127.0.0.1/dvwa/login.php" in page.url and "logout.php" not in url and auth == "dvwa":
		page, session = dvwa_relogin(session, url)

	soup = BeautifulSoup(page.content)
	forms = list()
	
	for form_element in soup.findAll('form'):
		
		form = {'action': '', 'name': '', 'method': '', 'inputs': list()}

		if form_element.has_key('name'):
			form['name'] = form_element['name']
			
		if form_element.has_key('action') and form_element.has_key('method'):
			form['action'] = form_element['action']
			form['method'] = form_element['method']
			
			forms.append(form)
			
			logger.info("--form '%s' found" % (form_element['action']))

			for input_field in form_element.findAll('input'):
				if input_field.has_key('name'):
					form['inputs'].append(input_field['name'])
					logger.info("--input field '%s' found" % (input_field['name']))

	return forms, session

def cookie_discovery(url, session, auth):
	page = session.get(url);

	# check if we are dvwa, if we have been redirected to login page
	if "http://127.0.0.1/dvwa/login.php" in page.url and "logout.php" not in url and auth == "dvwa":
		page, session = dvwa_relogin(session, url)

	page_cookies = session.cookies

	logger.info("Discovering cookies")
	cookies = list()

	for cookie_found in page_cookies:
		cookie = {"name": cookie_found.name, "value": cookie_found.value}
		cookies.append(cookie)
		logger.info("--cookie found: %(name)s=%(value)s" % cookie)

	return cookies, session


