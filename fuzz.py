"""
file: fuzz.py
description: base script to call.
usage: python fuzz [discover | test] url OPTIONS

Project Team:

CHRISTOFFER ROSEN			 <cbr4830@rit.edu>
ISIOMA NNODUM 				 <iun4534@rit.edu>
SAMANTHA SHANDROW 			 <ses6421@rit.edu>
"""
import sys 											# For system arguments
import requests									# requests HTTP library
import pprint
from logger import *
from custom_auth import *				# Read in all hardcoded authentication
from options import *						# Options parser
from discover import * 					# Module containing page discovery functions
from test import *							 # Module containing page test functions

pr = pprint.PrettyPrinter(indent=4)

(options, args) = parser.parse_args()

if len(sys.argv) < 4:
	parser.error("incorrect number of arguments")

else:
	action = sys.argv[1]
	url = sys.argv[2]

	if action == "discover" or action == "test":
		page = None
		session = None

		# Ensure that required common-file option is set
		if options.common_words is None:
			parser.error("newline-delimited file of common words is required for discovery")
		else:

			# authentic if applicable to site
			if options.app_to_auth is not None:

				try:
					username = custom_auth[options.app_to_auth.lower()]["username"]
					password = custom_auth[options.app_to_auth.lower()]["password"]
				except:
					parser.error("application specified in --custom-auth does not exist!")

				if options.app_to_auth.lower() == "dvwa":

					# Details to be posted to the login form
					payload = {
						"username": username,
						"password": password,
						"Login": "Login"
					}

					session = requests.Session()
					session.post(custom_auth[options.app_to_auth.lower()]["login_url"], data=payload)
					page = session.get(url + "/" + options.app_to_auth)

				elif options.app_to_auth.lower() == "bodgeit":

					# Just get the bodgeit page b/c there u don't need to authentication to use site.
					session = requests.Session()
					page = session.get(custom_auth[options.app_to_auth.lower()]["login_url"])

			# No custom authentication given
			else:
				session = requests.Session()
				page = session.get(url)

			# make sure that url can be reached
			if page.status_code != 200:
				parser.error("Cannot reach the URL specified")
			else:
				logger.info("Successfully reached page!")

			# time to discover
			discovered_urls = page_discovery(page, session, options.common_words)
			discovered_pages = list()
			for url in discovered_urls:
				inputs = input_discovery(url,session)
				discovered_page = { 'url': url, 'inputs': inputs }
				discovered_pages.append(discovered_page)

			pr.pprint(discovered_pages)

			if action == "test":
				test_pages(discovered_pages)
	else:
		parser.error("invalid action")
