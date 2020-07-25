# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 23:02:42 2020

@author: dsikerid
Testing
"""
# import numpy as np
# import scipy.stats as ss
# from scipy.stats import norm
# from scipy.special import erf, erfc
# import matplotlib.pyplot as plt
# import scipy.optimize as opt
# from dpln_distrib import dpln


# def objfunc(x, p):
#     if p[2] <= 0:
#         return np.inf
#     vals = -np.sum(dpln.logpdf(x, *p))
#     return vals

# sampledata = np.exp(np.random.randn(1000) + 2)
# params = opt.minimize(
#     lambda p: objfunc(sampledata, p), [0, 0, 1], method='Powell')

# p = params['x']
# plt.hist(sampledata, normed=1, log=True)
# trialx = np.linspace(sampledata.min(), sampledata.max(), 1000)
# plt.plot(trialx, dpln.pdf(trialx, *p))


import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

N = 1000000
x = np.arange(1, N+1)
a = 1.01
weights = x ** (-a)
weights /= weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))

# sample = bounded_zipf.rvs(size=100)
# plt.hist(sample, bins=np.arange(1, N+2))
# plt.show()



# import socket
# from OpenSSL import SSL
# import certifi

# hostname = 'sohu.com'
# port = 443


# context = SSL.Context(method=SSL.TLSv1_METHOD)
# context.load_verify_locations(cafile=certifi.where())

# conn = SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
# conn.settimeout(5)
# conn.connect((hostname, port))
# conn.setblocking(1)
# conn.do_handshake()
# conn.set_tlsext_host_name(hostname.encode())
# for (idx, cert) in enumerate(conn.get_peer_cert_chain()):
#     print(f'{idx} subject: {cert.get_subject()}')
#     print(f'  issuer: {cert.get_issuer()})')
#     print(f'  fingerprint: {cert.digest("sha1")}')

# conn.close()