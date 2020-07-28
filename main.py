import numpy as np
import scipy.stats as stats
from tranco import Tranco
import surfing_behavior_model
from certificate_chain_extractor import get_interm_cert_chains
import pickle

#Number of webpages visited by the user during one behavior simulation
browsing_session_length=20


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
non_responsive_domains =['https://beone.ne' , 'https://team-8.net', 'https://nflxso.net']    

# List with recently visited websites
recently_visited=[]
IC_chains=[]

#Browsing session simulation
print('_____________________________________________________________________________________')
print(' ')
print('Simulation Starting - Current session length = ' + str(browsing_session_length))
print('_____________________________________________________________________________________')



current_url='https://www.google.com'
recently_visited.insert(0,current_url)
print('...')
print('User browsing '+ current_url)
IC_chains = get_interm_cert_chains(current_url)
print('Intermediate Certificates Extracted')
print('---------------OK------------------------------------')

for i in range(browsing_session_length-1):
    
    nextWebAdress = surfing_behavior_model.getNextWebAdress(recently_visited, popular_websites, bounded_zipf_N)
    while nextWebAdress in non_responsive_domains:
        nextWebAdress = surfing_behavior_model.getNextWebAdress(recently_visited, popular_websites, bounded_zipf_N)
    if nextWebAdress not in recently_visited:
        recently_visited.insert(0,nextWebAdress)
    current_url = nextWebAdress
    print('...')
    print('User browsing '+ current_url)
    IC_chains = IC_chains + get_interm_cert_chains(nextWebAdress)
    print('Intermediate Certificates Extracted')
    print('---------------OK------------------------------------')



data = np.array(IC_chains)
np.savez("IC_chains", data)







