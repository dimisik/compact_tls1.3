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
"""
import math
import numpy as np
import scipy.stats as stats



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
    if static==1: revisit_prob = 0.5
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
    experimentl_distribution_min = 0.07005739852975212
    experimentl_distribution_max = 320.98314686549594
    sample = np.random.lognormal(mu,sigma)
    if sample < experimentl_distribution_min: sample==150
    if sample > experimentl_distribution_max: sample==150
    normalized_stack_dist = (sample-experimentl_distribution_min)/(experimentl_distribution_max-experimentl_distribution_min)
    stack_dist = math.floor(normalized_stack_dist * len(recently_visited))
    next_page = recently_visited(stack_dist)
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



def choose_inside_link(current_url):


def getNextWebAdress(recently_visited, bounded_zipf_1M):
    """
    This function decides the next user surfing action and returns the next
    website to be viseted as a pointer to the website_list 
    If the next action is following a link inside the current page returns -1
    """
    if revisit_action(static=0):
        nextWebAdress = revisit_page_choice(recently_visited)
        return nextWebAdress
    elif jump_action():
        nextWebAdress = bounded_zipf_1M.rvs()
        while nextWebAdress not in recently_visited: nextWebAdress = bounded_zipf_1M.rvs() 
        return nextWebAdress
    else:     
        return -1
        
        
        
        
        
        
        
        

