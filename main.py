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

#Number of webpages visited bu user during one behavior simulation
user_browsing_length=500


# Define zipf-like distribution for Web-page popularity
N = 1000000 #Number of popular websites in this simulation
x = np.arange(1, N+1)
a = 1.01
weights = x ** (-a)
weights /= weights.sum()
bounded_zipf_1M = stats.rv_discrete(name='bounded_zipf', values=(x, weights))


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
current_url='www.google.com'
recently_visited.insert(0,current_url)
for i in range(user_browsing_length):
    next_page_indicator = surfing_behavior_model.getNextWebAdress(recently_visited, bounded_zipf_1M)
    if next_page_indicator == -1:
        nextWebAdress=surfing_behavior_model.choose_inside_link(current_url)
   else:
       nextWebAdress = 'www.'+popular_websites(next_page_indicator)
    
    
    



# with cert_human.ssl_socket(host="www.google.com") as sock:
#         cert = sock.get_peer_certificate()
#         cert_chain = sock.get_peer_cert_chain()    
# c1 = cert_human.x509_to_pem(cert)
# cc = cert_human.x509_to_pem(cert_chain[1])       
# print(c1)
# print(cc)
# print(cert.get_subject().get_components())
# pem = cert_human.x509_to_pem(cert)


# cert_human.enable_urllib3_patch()
# response = requests.get("https://www.zillow.com")
# print(response.raw.peer_cert.get_subject().get_components())
# cert_human.disable_urllib3_patch()




# dst = ("www."+"zillow.com", 443)
# ctx = SSL.Context(SSL.SSLv23_METHOD)
# s = socket.create_connection(dst)
# s = SSL.Connection(ctx, s)
# s.set_connect_state()
# s.set_tlsext_host_name(dst[0].encode())
# s.sendall('HEAD / HTTP/1.0\n\n')
# s.recv(16)
# certs = s.get_peer_cert_chain()









