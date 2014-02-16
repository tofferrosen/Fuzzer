"""
file: fuzz.py
description: base script to call.
usage: python fuzz [discover | test] url OPTIONS
"""
import sys 									# For system arguments
import requests								# requests HTTP library 
from custom_auth import *					# Read in all hardcoded authentication
from options import *						# Options parser
from discover import * 						# Module containing page discovery functions


(options, args) = parser.parse_args()

if len(sys.argv) < 4:
	parser.error("incorrect number of arguments")

else:
	action = sys.argv[1]
	url = sys.argv[2]

	# authentice if applicable to site
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

			with requests.Session() as s:
				s.post(custom_auth[options.app_to_auth]["login_url"], data=payload)
				page = s.get(url + "/" + options.app_to_auth)

				# make sure that url can be reached
				if page.status_code != 200:
					parser.error("Cannot reach the URL specified")
				else:
					page_discovery(page)
					




