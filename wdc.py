##########################################################################
# Weighted Degree Centrality
##########################################################################

import networkx as nx

def degree_w(G,var='weight',normalized=True):
    '''Calculation for weighted degree centrality (WDC). Returns a dictionary of WDC values, where 
    the key is the node and the value is the WDC. Calculation for WDC is based on Candeloro et al. PLOSone 2016
    
    Multiedged graphs might cause issues, so recommend only calculating on single-edged graphs. This has not
    been tested.
    
    G 
        -NextworkX graph object
    var 
        -edge attritube that corresponds to the weight of each edge. Default is 'weight'
    normalized
        -whether to normalize the weighted degree centrality. Normalized by number of nodes (n - 1). Default
         is True
    '''
    dictionary = {}
    for node in G.nodes_iter():
        degree = nx.degree(G,nbunch=node)
        neighbor = G[node]
        w = []
        for nei in neighbor:
            x = G.edge[node][nei][var]
            w.append(x)
        w2 = [x / sum(w) for x in w]
        w2.sort()
        form = 0
        for j in range(degree-1):
            i = j+1
            f1 = (w2[j] / sum(w2))*i
            f2 = (sum(w2[0:i]) / sum(w2))
            f3 = i * w2[j]
            ft = f1 + f2 - f3
            form += ft
        try:
            if normalized == True:
                wdc = ((0.5 + form) / (degree/2) * degree) / ((len(G.nodes())) - 1)
            else:
                wdc = ((0.5 + form) / (degree/2) * degree)
            dictionary[node] = wdc
        except:
            dictionary[node] = np.nan
    return dictionary
