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

def test_pages(pages):

  # set up all exploit strategies 
  sanitization = ExploitStrategy(pages, SanitizationExploit())
  delayed_response = ExploitStrategy(pages, DelayedResponseExploit())
  http_reponse = ExploitStrategy(pages, HttpResponseExploit())
  sensitive_data = ExploitStrategy(pages, SensitiveDataExploit())

  # excute all exploit strategies
  sanitization.execute()
  delayed_response.execute()
  http_response.execute()
  sensitive_data.execute()
