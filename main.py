'''
Created on Jul 27, 2016

@author: henk
'''
from pycrest.eve import EVE

eve = EVE()
print(eve()['status_code'])
print(eve()['version'])
print(eve()['expires_at'])
print(eve()['expires_in'])
print(eve().time()['status_code'])
print(eve().time()['version'])
print(eve().time()['expires_at'])
print(eve().time()['expires_in'])
