import numpy as np
import scipy.stats as stats
from tranco import Tranco
import surfing_behavior_model
from certificate_chain_extractor import get_interm_cert_chains
import cert_human
import time
import requests
import sys


#Number of webpages visited by the user during one behavior simulation
browsing_session_length=100


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

# Load list of non-responsive domains
# with open('non_responsive_domains', 'rb') as f: 
#     non_responsive_domains=pickle.load(f)
non_responsive_domains =['https://rus.ec', 'https://beone.ne', 'https://jddb.cn', 'https://nhk.or.jp', 'https://googlevideo.com', 'https://marketwatch.com', 'https://team-8.net', 'https://nflxso.net', 'https://by.me', 'https://home.nl', 'https://chinastock.com.cn']    

# List with recently visited websites
recently_visited=[]
session_connections_per_pege=[]
IC_chains=[]

#Browsing session simulation
print('_____________________________________________________________________________________')
print(' ')
print('Simulation Starting - Current session length = ' + str(browsing_session_length))
print('_____________________________________________________________________________________')


current_url='https://www.zillow.com'
recently_visited.insert(0,current_url)
print('...')
print('User browsing '+ current_url)
connections, certs = get_interm_cert_chains(current_url)
session_connections_per_pege.append(connections)
IC_chains.append(certs)

print('Intermediate Certificates Extracted')
print('---------------OK------------------------------------')

RTT=[]

# Keep Intermediate certificates in pem form
IC_dictionary = {}

for i in range(browsing_session_length-1):
    
    # nextWebAdress = surfing_behavior_model.getNextWebAdress(recently_visited, popular_websites, bounded_zipf_N)
    sample = bounded_zipf_N.rvs()
    nextWebAdress = 'https://'+popular_websites[sample]

    initial_time = time.time() #Store the time when request is sent
    try: 
        request = requests.get(nextWebAdress)
        ending_time = time.time() #Time when acknowledged the request
        elapsed_time = ending_time - initial_time
        RTT.append(elapsed_time)
    except: pass
    while nextWebAdress in non_responsive_domains:
        nextWebAdress = surfing_behavior_model.getNextWebAdress(recently_visited, popular_websites, bounded_zipf_N)
    while nextWebAdress in recently_visited:
        nextWebAdress = surfing_behavior_model.getNextWebAdress(recently_visited, popular_websites, bounded_zipf_N)    
    recently_visited.insert(0,nextWebAdress)
    current_url = nextWebAdress
    print('...')
    print('User browsing '+ current_url)
    connections, certs = get_interm_cert_chains(current_url)
    session_connections_per_pege.append(connections)
    IC_chains.append(certs)
    data = np.array(RTT)
    np.savez("RTT", data)
    for hostname in certs:
        pem_list=[]
        for cert in hostname[1]:
            pem_list.append(cert_human.x509_to_pem(cert))
        IC_dictionary[hostname[0]]=pem_list[:-1]
    d = np.array(IC_dictionary)
    np.savez("IC_dictionaty", d)
    print('Intermediate Certificates Extracted')
    print('---------------OK------------------------------------')




for entry in IC_chains:
    for hostname in entry:
        pem_list=[]
        for cert in hostname[1]:
            pem_list.append(cert_human.x509_to_pem(cert))
        IC_dictionary[hostname[0]]=pem_list[:-1]
    


d = np.array(IC_dictionary)
np.savez("IC_dictionaty", d)







