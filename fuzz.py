"""
file: fuzz.py
description: base script to call.
usage: python fuzz [discover | test] url OPTIONS
"""
import sys 									# For system arguments
import requests								# requests HTTP library 
from logger import *
from custom_auth import *					# Read in all hardcoded authentication
from options import *						# Options parser
from discover import * 						# Module containing page discovery functions


(options, args) = parser.parse_args()

if len(sys.argv) < 4:
	parser.error("incorrect number of arguments")

else:
	action = sys.argv[1]
	url = sys.argv[2]

	if action == "discover":
		# Ensure that required common-file option is set
		if options.common_words is None:
			parser.error("newline-delimited file of common words is required for discovery")
		else:
			
			# authentic if applicable to site
			if options.app_to_auth is not None:

				try: 
					username = custom_auth[options.app_to_auth]["username"]
					password = custom_auth[options.app_to_auth]["password"]
				except:
					parser.error("application specified in --custom-auth does not exist!")

				if options.app_to_auth == "dvwa":

					# Details to be posted to the login form
					payload = {
						"username": username,
						"password": password,
						"Login": "Login"
					}

					session = requests.Session()
					session.post(custom_auth[options.app_to_auth]["login_url"], data=payload)
					page = session.get(url + "/" + options.app_to_auth)

					# make sure that url can be reached
					if page.status_code != 200:
						parser.error("Cannot reach the URL specified")
					else:
						logger.info("Authenticated to DVWA")
						discovered_urls = page_discovery(page, session, options.common_words)
						for url in discovered_urls:
							input_discovery(url,session)
						

			# End custom-auth option
	# End discover
	elif action == "test":
		logger.error("not implemented yet")
	else:
		parser.error("invalid action")
					




