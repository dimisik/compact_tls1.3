import numpy as np
import cert_human
import requests
import urllib3
import socket
import ssl

# a = np.arange(10)
# print(a)

# store = cert_human.CertStore.from_socket(host="adobe.com") 
# chain_store = cert_human.CertChainStore.from_socket(host="adobe.com")
# print(chain_store.pem)  




cert_human.enable_urllib3_patch()
response = cert_human.requests.get("https://adobe.com", verify=False)
cert_chain = cert_human.CertChainStore.from_response(response)
print(cert_chain)




# with cert_human.ssl_socket(host="www.zillow.com") as sock:
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














