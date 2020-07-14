# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:46:32 2020

@author: dsikerid
"""

import socket
from OpenSSL import SSL
import certifi

hostname = 'zillow.com'
port = 443


context = SSL.Context(method=SSL.TLSv1_METHOD)
context.load_verify_locations(cafile=certifi.where())

conn = SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
conn.settimeout(5)
conn.connect((hostname, port))
conn.setblocking(1)
try:
    conn.do_handshake()
except:
    print("error")
conn.set_tlsext_host_name(hostname.encode())
for (idx, cert) in enumerate(conn.get_peer_cert_chain()):
    print(f'{idx} subject: {cert.get_subject()}')
    print(f'  issuer: {cert.get_issuer()})')
    print(f'  fingerprint: {cert.digest("sha1")}')

conn.close()

