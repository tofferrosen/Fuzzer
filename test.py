"""
file: test.py
description: Contains functions for performing testing of a web page
"""
from logger import *     # logging output
from exploit import *    # the exploit strategy

def test_pages(pages):

  # All exploits to try
  sanitization = Exploit(Sanitization)
#  sensitive_data = Exploit(SensitiveData)
#  delayed_response = Exploit(DelayedResponse)
#  http_response_code = Exploit(HttpResponseCode)

  sanitization.execute(pages)
