# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 20:21:20 2020

@author: dsikerid

Functions that describe the surfing behavioral model of a user.
Action probability distributions chosen based on:
   -[1] Burklen, Susanne, Pedro Jose Marron, Serena Fritsch, and Kurt Rothermel. "User centric walk: An 
    integrated approach for modeling the browsing behavior of users on the web." In 38th Annual 
    Simulation Symposium, pp. 149-159. IEEE, 2005.
   -[2] Barford, Paul, and Mark Crovella. "Generating representative web workloads for network and 
   server performance evaluation." In Proceedings of the 1998 ACM SIGMETRICS joint international 
   conference on Measurement and modeling of computer systems, pp. 151-160. 1998.
   
Uses and modifies get_all_website_links(url) from:
https://github.com/x4nth055/pythoncode-tutorials/tree/master/web-scraping/link-extractor
"""
import math
import numpy as np
import scipy.stats as stats
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup




def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)



def get_all_website_links(url):
    """
    Returns all URLs that is found on `url`
    """
    internal_urls = []
    external_urls = []
    # all URLs of `url`
    urls = []
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    # initialize an HTTP sesion
    session = HTMLSession()
    # make HTTP request & retrieve response
    response = session.get(url)
    # execute Javascript
    try:
        response.html.render()
    except:
        pass
    soup = BeautifulSoup(response.html.html, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                external_urls.append(href)
                urls.append(href)
            continue
        urls.append(href)
        internal_urls.append(href)
    return urls



def revisit_action(static):
    """
    This function decides whether the next browsing action will be revisiting
    a previously visted website or not
    Input: If static==1 then the revisit rate is predifined.
    Output: 1 -> revisit previous website
            0 -> do not revisit
    The distribution of the revisiting pattern is log-normal with parameters
    mu and sigma defined in this function

    """
    mu = 0.5
    sigma = 0.2
    experimentl_distribution_min = 0.5489157804116644
    experimentl_distribution_max = 4.810632252219341
    sample = np.random.lognormal(mu,sigma)
    revisit_prob = (sample-experimentl_distribution_min)/(experimentl_distribution_max-experimentl_distribution_min)
    if static==1: revisit_prob = 0.15
    if np.random.random() < revisit_prob:
        return 1 
    else:
        return 0


def revisit_page_choice(recently_visited):
    """
    This function decides the page to be revisited
    Input: List of already revisited sites, recently_visited (str)
    Output: page pointer 
    (Temporal Locality)The distribution of the stack distance of the next chosen site is 
    log-normal with parameters mu and sigma defined in this function
    """
    mu = 1.5
    sigma = 0.75
    experimental_distribution_min = 0.07005739852975212
    experimental_distribution_max = 320.98314686549594
    sample = np.random.lognormal(mu,sigma)
    if sample < experimental_distribution_min: sample==150
    if sample > experimental_distribution_max: sample==150
    normalized_stack_dist = (sample-experimental_distribution_min)/(experimental_distribution_max-experimental_distribution_min)
    stack_dist = math.floor(normalized_stack_dist * len(recently_visited))
    next_page = recently_visited[stack_dist]
    return next_page
    

def jump_action():
    """
    This function decides whether the user jumps to a new webpage or
    follows a link within the current page
    Output: 1 -> jump to a new website
            0 -> follow link inside current page
    Following [1] the distribution for the probability that a user jumps to 
    another page is Zipf-like with parameter a: 1.2 < a < 1.5        
    """
    N = 100
    x = np.arange(1, N+1)
    a = 1.2
    weights = x ** (-a)
    weights /= weights.sum()
    bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
    sample = bounded_zipf.rvs()
    jump_prob=sample/100
    if np.random.random() < jump_prob:
        return 1 
    else:
        return 0



def choose_internal_link(current_url):
    """
    This function decides the next internal link to be chosen by the user.
    For more detaile refer to [1].
    If the total number of links is less than 10 the probability of choosing
    each link is nearly equally distributed
    For the case of >10 links the user is more likely to choose based on their
    position on the page
    """
    internal_links = get_all_website_links(current_url)
    for link in internal_links:
        url=urlparse(link)
        if url.scheme != 'https': 
            internal_links.remove(link)
    num_of_links=len(internal_links)
    if num_of_links == 0:
        next_page = -1        
    elif num_of_links <= 10:
        stack_dist=np.random.randint(0, num_of_links+1)
        next_page = internal_links[stack_dist]            
    else:
        N = num_of_links
        x = np.arange(1, N+1)
        a = 1.2
        weights = x ** (-a)
        weights /= weights.sum()
        bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
        sample = bounded_zipf.rvs()
        next_page = internal_links[sample]
    return next_page
    


def getNextWebAdress(recently_visited, popular_websites, bounded_zipf_1M):
    """
    This function decides the next user surfing action and returns the next
    website to be viseted 
    """
    if revisit_action(static=1):
        nextWebAdress = revisit_page_choice(recently_visited)
    elif jump_action():
        sample = bounded_zipf_1M.rvs()
        nextWebAdress = 'https://'+popular_websites[sample]
        while nextWebAdress in recently_visited: 
            sample = bounded_zipf_1M.rvs()  
            nextWebAdress = 'https://'+popular_websites[sample]
    else:     
        nextWebAdress = choose_internal_link(recently_visited[0])
        if nextWebAdress == -1: 
            sample = bounded_zipf_1M.rvs()
            nextWebAdress = 'https://'+popular_websites[sample]
            while nextWebAdress in recently_visited: 
                sample = bounded_zipf_1M.rvs()  
                nextWebAdress = 'https://'+popular_websites[sample]
    return nextWebAdress
        
        
        
        
        
        
        
        

