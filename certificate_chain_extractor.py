# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:40:21 2020

@author: dsikerid
"""

import cert_human
from OpenSSL import SSL
import socket
from urllib.parse import urlparse
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import os
import urllib3
import ssl




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




def explore_web_address(WebAddress):
    """
    Uses selenium-wire:https://pypi.org/project/selenium-wire/#openssl
    Extracts the underlying requests made by the browser for a specific url.
    params:
        WebAddress (str): url
    output:
        -requested_urls: urls of the requested content
        -unique_hostnames: unique hostnames of the requested_urls
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    
    # Create a new instance of the Chrome driver
    path_to_chromedriver=os.getcwd()+'\\chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=path_to_chromedriver)
    # driver = webdriver.Chrome(options=options, executable_path=r"C:/Users/dsikerid/Desktop/chromedriver.exe")
    
    # Go to the page
    driver.get(WebAddress)
    
    requested_urls=[]
    requested_hostnames=[]
    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            requested_urls.append(request.url)
            url=urlparse(request.url)
            if url.scheme=='https':
                requested_hostnames.append(url.hostname)
    unique_hostnames=set(requested_hostnames)        
    return requested_urls, unique_hostnames
        


def get_interm_cert_chains(WebAddress):
    """
    Extracts certificate chains from all contents requests made when loading a page.
    params:
        WebAddress (str): url
    output:
        -number of requested_urls: number of total connections initiated by the browser
        -chains: list of certificate chains per unique content request address
    """
    main_host=urlparse(WebAddress)
    requested_urls, unique_hostnames=explore_web_address(WebAddress)
    if main_host.hostname not in unique_hostnames: unique_hostnames.insert(0,main_host.hostname)
    chains = []
    for host in unique_hostnames:
        cert_chain=get_certificate_chain(host)
        temp = (host, cert_chain)   
        chains.append(temp)
    return len(requested_urls), chains





































