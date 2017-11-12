import requests
import re
import os
import sys                                                                                                                                                                  
from urllib2 import Request, urlopen                                                                                                                                        
import urllib                                                                                                                                                               
from bs4 import BeautifulSoup   
import logging
import json
import xml.etree.ElementTree

# search by google
# return the total number of response
def google_search(sentence):                                                                                                                                                                                                                                                                                          
    url = "http://www.google.de/search?q=%s" % urllib.quote_plus(sentence)    

    reponse = Request(url)                                                                                                                                                   
    reponse.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')                               
    html_google = urlopen(reponse).read()    

    soup = BeautifulSoup(html_google, 'html.parser')                                                                                                                                           
    count = soup.find('div', id='resultStats')    

    return count

sent1 = "Lions are predators"
sent2 = "Sheep are predators"

print google_search(sent1)
print google_search(sent2)