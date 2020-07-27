import numpy as np
import cert_human
import requests
import urllib3
import ssl
from OpenSSL import SSL
import socket
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from tranco import Tranco
import surfing_behavior_model
from certificate_chain_extractor import get_interm_cert_chains

#Number of webpages visited by the user during one behavior simulation
browsing_session_length=500


# Define zipf-like distribution for Web-page popularity
N = 1000000 #Number of popular websites in this simulation
x = np.arange(1, N+1)
a = 1.01
weights = x ** (-a)
weights /= weights.sum()
bounded_zipf_N = stats.rv_discrete(name='bounded_zipf', values=(x, weights))


# Read popular websites from Cisco Umbrella
#https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip

# ALTERNATIVE: Read popular websites from the Tranco project
#https://tranco-list.eu
tranco_project = Tranco(cache=True, cache_dir='.tranco')
latest_list = tranco_project.list()
popular_websites = latest_list.top(N)

# List with recently visited websites
recently_visited=[]


#Browsing session simulation
current_url='https://www.google.com'
recently_visited.insert(0,current_url)
for i in range(browsing_session_length):
    next_page_indicator = surfing_behavior_model.getNextWebAdress(recently_visited, bounded_zipf_N)
    if next_page_indicator == -1:
        nextWebAdress=surfing_behavior_model.choose_internal_link(current_url)
        get_interm_cert_chains(nextWebAdress)
    else:
        nextWebAdress = 'https://'+popular_websites(next_page_indicator)
        get_interm_cert_chains(nextWebAdress)
    
    










