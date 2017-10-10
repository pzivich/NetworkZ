####################################################################
# Calculates whether there is presence of homophily in a graph 
####################################################################

import networkx as nx 
import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy.stats as sci


######################################################
#Proportion of edges with same node attribute
def edge_counter(G,var,print_result=True):
    '''Calculates the proportion of edges between two nodes with variable
    of interest relative  to the total number of edges in a network. 
    
    G
        -NetworkX graph object
        
    var 
        -variable of interest to calculate proportion for. Currently only
         implemented for a binary node attritube
    
    print_result
        -Whether to print the results of the calculation. Default is True. 
         This prevents printing in further functions that build on this.
    '''
    edge_var = 0
    ndegree = len(G.edges())
    for i,j in G.edges():
        if ((G.node[i][var]==1)&(G.node[j][var]==1)):
            edge_var += 1
        else:
            pass
    ratio = edge_var/ndegree
    if (print_result==True):
        print('total edges sum:',ndegree)
        print('var=1 edges sum:',edge_var)
        print('ratio of edges',ratio)
    else:
        pass
    return ratio


##########################################################
#Generate df of randomized rewirings
def rand_perm(G,var,permutation=10):
    '''Randomly reconnect a network then calculate the proportion of edges
    between the nodes of interest using the edge_counter function.
    NOTE: not implemented for directed or weighted networks currently
    
    G
        -NetworkX graph object 
    
    var 
        -variable of interest to calculate proportion for. Currently only
         implemented for a binary node attritube
    
    permutations
        -Number of graph rewirings to complete. Default is set to 10
    '''
    true_value = edge_counter(G,var,print_result=False)
    numb = len(G.edges())
    simulist = []
    G_copy = G.copy()
    for i in range(permutation):
        nx.double_edge_swap(G_copy,nswap=(numb/2),max_tries=numb*100)
        sim_value = edge_counter(G_copy,var,print_result=False)
        simulist.append(sim_value)
    df = pd.DataFrame()
    df['simu'] = simulist
    return df


###############################################################
#Homophily assessment
def homophily_full(G,var,permutation_number=10000,twosided=True,dist_image=True,bins=22):
    '''Assess whether homophily is present in a specific network by a 
    specified binary variable. Builds on edge_counter and rand_perm functions.
    Generates a matplotlib image of the distribution is requested.
    
    G
        -NetworkX graph object
    
    var 
        -variable of interest to calculate proportion for. Currently only
         implemented for a binary node attritube
    
    permutation_number
        -Number of permutations to conduct. A higher number will produce a
         more normalized distribution. Between 1000 to 10000 permuttions 
         is recommended to achieve good convergence. Default is set to 10000
    
    twosided
        -Whether to calculated the two-sided p-value. Default is True
    
    dist_image
        -Whether to display the distribution of the proportion of edges between
         nodes with the variable of interest. A red line designates the observed
         proportion of edges between nodes of interests observed in the actual network
    
    bins
        -Number of bins to use in the histogram
    '''
    true = edge_counter(G,var,print_result=False)
    df = rand_perm(G,var,permutation=permutation_number)
    p1 = sci.percentileofscore(df['simu'],true)
    p2 = 100 - p1
    low = min([p1,p2])
    if (twosided==True):
        pv = (low*2)/100
    else:
        pv = low / 100
    print('--------------------------------------') #printing results
    print('Homophily %:',true) #percent of homophilous edges with certain node characteristic
    print('--------------------------------------')
    print('Number of rewirings:',permutation_number) #number of rewirings
    print('P-value',pv) #p-value, calculated from percentile of value from rewirings
    print('--------------------------------------')
    if (dist_image==True): #prints results via matplotlib if requested (default is requested)
        plt.hist(df['simu'],color='blue',bins=bins,normed=True) #plot simulated data
        plt.axvline(x=true, color='red',linewidth=5) #draw a red line at actual value
        plt.show() #print output
    else:
        pass
