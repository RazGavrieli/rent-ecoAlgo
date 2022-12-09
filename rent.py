import networkx as nx
from matplotlib import pyplot as plt
def players_to_graph(evaluations):
    g = nx.Graph()
    agents = []
    for roomIndex, room in enumerate(evaluations):
        g.add_node((roomIndex, 'r'), bipartite=1)
        agents.append((roomIndex, 'r'))
        
    for playerIndex, player in enumerate(evaluations[0]):
        g.add_node((playerIndex, 'p'),  bipartite=0)
    
    for roomIndex, room in enumerate(evaluations):
        for playerIndex, playerValue in enumerate(room):
            g.add_edge((playerIndex, 'p'), (roomIndex, 'r'), weight=playerValue)
    
    return g, agents

def draw_graph(g, agents):
    pos1 = nx.bipartite_layout(g, agents)
    edge_labels = nx.get_edge_attributes(g, "weight")
    nx.draw_networkx_edge_labels(g, pos=pos1,edge_labels=edge_labels, label_pos=0.2)
    nx.draw_networkx(g, pos=pos1)
    plt.show()

def powerset(iterable):
    from itertools import chain, combinations
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range((len(s)+1)))

def brute_force_max_matching(g: nx.Graph(), agents):
    # find a max weight matching and sum the weight of this max weight matching
    res = nx.max_weight_matching(g)
    sumTarget = 0
    for edge in res:
        data = g.get_edge_data(edge[0], edge[1])
        sumTarget += data['weight']
    results = []

    # brute force over all the matchings, if the sum of weight equalts to sumTarget, append the result to a list
    for i in powerset(g.edges()):
        if len(i) != len(agents) or not nx.is_matching(g, i):
            continue
        sum = 0
        for edge in i:
            data = g.get_edge_data(edge[0], edge[1])
            sum += data['weight']
        if sum == sumTarget:
            results.append(i)
    return results

v = [[35,40,25],
[35,60,40],
[25,40,20]]

g, agents = players_to_graph(v)
#draw_graph(g, agents)

results = brute_force_max_matching(g, agents)
print(results)
z = 0
maxMin = -1
for i in results:
    currMin = 999999
    for edge in i:
        currWeight = g.get_edge_data(edge[0], edge[1])['weight']
        if currWeight < currMin:
            currMin = currWeight
    if currMin > maxMin:
        maxMin = currMin
        z = i
print(z)

