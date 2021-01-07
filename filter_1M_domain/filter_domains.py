# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 18:58:43 2020

@author: dsikerid

Creates black_list containing non responsive domains from a 1M domain list.
"""

import csv
import cert_human
from OpenSSL import SSL
import socket
import numpy as np
from tranco import Tranco







def get_certificate_chain(host):
    """
    Extracts the certificate chain from the provided host.
    params:
        host (str): hostname
    output:
        -list of certificates in the chain (excluding root)
        -in case of exception (eg. timeout) returns -1
    """
    try:
        with cert_human.ssl_socket(host) as sock:
#            cert = sock.get_peer_certificate()
            cert_chain = sock.get_peer_cert_chain()  
            return cert_chain
    except:
        try:
            dst = (host, 443)
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            sock = socket.create_connection(dst)
            s = SSL.Connection(ctx, sock)
            s.set_connect_state()
            s.set_tlsext_host_name(dst[0].encode())
            s.sendall('HEAD / HTTP/1.0\n\n')
            s.recv(16)
            cert_chain = s.get_peer_cert_chain()
            return cert_chain
        except: 
            return -1



# For the Tranco list
tranco_project = Tranco(cache=True, cache_dir='.tranco')
latest_list = tranco_project.list()
popular_websites = latest_list.top(1000000)
non_responsive_domains=[]



for link in popular_websites:
    check = get_certificate_chain(link)
    if check == -1:
        non_responsive_domains.append(link)
        print(link + " was added to the non-responsive list")

 
data = np.array(non_responsive_domains)
np.savez("non_responsive_domains", data)




# For CSV Files
# non_responsive_domains=[]
# csvwriter = csv.writer(filtered_hostnames)
# with open('top-1m_cisco_umbrella.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         hostname=row[1]
#         check = get_certificate_chain(hostname)
#         if check == -1:
#             non_responsive_domains.append(hostname)
#             print(hostname + " was added to non-responsive list")
# with open('non_responsive_domains', 'wb') as f:
#     pickle.dump(non_responsive_domains, f)   










