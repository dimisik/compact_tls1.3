# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 18:58:43 2020

@author: dsikerid
"""

import csv
import cert_human

filtered_hostnames = open("filtered_amazon.csv", "w+", newline='')
csvwriter = csv.writer(filtered_hostnames)
with open('top-1m_alexa.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        hostname=row[1]
        try:
            chain_store = cert_human.CertChainStore.from_socket(hostname)
        except:
            print(hostname + " was filtered out")
        else:
            print(hostname + " was added")
            csvwriter.writerow([hostname]) 
            csvwriter.writerow([hostname]) 
            break
filtered_hostnames.close()



# hostname = 'www.zillow.com'
# context = ssl.create_default_context()
# with socket.create_connection((hostname, 443)) as sock:
#     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
#         print(ssock.version())
#         print(ssock.)