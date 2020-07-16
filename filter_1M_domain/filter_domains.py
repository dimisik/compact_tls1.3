# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 18:58:43 2020

@author: dsikerid
"""

import csv
import cert_human
from OpenSSL import SSL
import socket

filtered_hostnames = open("filtered_alexa.csv", "w+", newline='')
csvwriter = csv.writer(filtered_hostnames)
with open('top-1m_alexa.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        hostname=row[1]
        try:
            chain_store = cert_human.CertChainStore.from_socket("www."+hostname)
        except:
            try:
                dst = ("www."+hostname, 443)
                ctx = SSL.Context(SSL.SSLv23_METHOD)
                s = socket.create_connection(dst)
                s = SSL.Connection(ctx, s)
                s.set_connect_state()
                s.set_tlsext_host_name(dst[0].encode())
                s.sendall('HEAD / HTTP/1.0\n\n')
                s.recv(16)
                certs = s.get_peer_cert_chain()
            except:
                print(hostname + " was filtered out")
            else:
                print(hostname + " was added")
        else:
            print(hostname + " was added")
            # csvwriter.writerow([hostname]) 
filtered_hostnames.close()




# from OpenSSL import SSL
# import socket
# import csv
# import cert_human

# filtered_hostnames = open("filtered_alexa.csv", "w+", newline='')
# csvwriter = csv.writer(filtered_hostnames)
# with open('top-1m_alexa.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         hostname=row[1]
#         try:
#             dst = ("www."+hostname, 443)
#             ctx = SSL.Context(SSL.SSLv23_METHOD)
#             s = socket.create_connection(dst)
#             s = SSL.Connection(ctx, s)
#             s.set_connect_state()
#             s.set_tlsext_host_name(dst[0].encode())
#             s.sendall('HEAD / HTTP/1.0\n\n')
#             s.recv(16)
#             certs = s.get_peer_cert_chain()
#         except:
#             print(hostname + " was filtered out")
#         else:
#             print(hostname + " was added")
#             csvwriter.writerow([hostname]) 
# filtered_hostnames.close()














# Check TLS version
# hostname = 'www.zillow.com'
# context = ssl.create_default_context()
# with socket.create_connection((hostname, 443)) as sock:
#     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
#         print(ssock.version())
#         print(ssock.)