"""
file: test.py
description: Contains functions for performing testing of a web page
"""
from logger import *     		 			 # logging output
from exploit_strategy import *   			 # the exploit strategy
from sanitization_exploit import * 	 		 # the concrete sanitization exploit
from delayed_response_exploit import *		 # the concrete delayed response exploit
from http_response_exploit import *			 # the concrete http response code exploit
from sensitive_data_exploit import *		 # the concrete sensitive data exploit

def test_pages(pages, session):

  # set up all exploit strategies 
  sanitization = ExploitStrategy(pages, session, SanitizationExploit())
  delayed_response = ExploitStrategy(pages, session, DelayedResponseExploit())
  http_reponse = ExploitStrategy(pages, session, HttpResponseExploit())
  sensitive_data = ExploitStrategy(pages, session, SensitiveDataExploit())

  # excute all exploit strategies
  sanitization.execute()
  delayed_response.execute()
  http_response.execute()
  sensitive_data.execute()
