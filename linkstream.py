import networkx as nx
import random
from collections import Counter

class linkstream:
    def __init__(self, N):
        """
        N: Number of intervals to divide link stream into
        """
        self.G = nx.MultiGraph()      # Original link stream
        self.DG = nx.MultiGraph()     # Discrete link stream
        self.N = N
        self.delta = 0
        

    def add_link(self, u, v, s, e):
        """
        u: start node
        v: end node
        s: start time
        e: end time
        """
        self.G.add_edge(u, v, start_time=s, end_time=e)
        

    def links(self):
        return self.G.edges(data=True)


    def links_at_time_t(self, t):
        """
        t: time instant
        """
        for u, v, attr in self.G.edges_iter(data=True):
            if attr['start_time'] <= t <= attr['end_time']:
                yield (u, v, attr)
                

    def discrete_time_set(self):
        start = []
        end = []
        for u, v, attr in self.G.edges_iter(data=True):
            start.append(attr['start_time'])
            end.append(attr['end_time'])
        t = [(i*(max(end) - min(start))/float(self.N) + min(start)) for i in range(0, self.N + 1)]
        self.delta = (max(end) - min(start))/float(self.N)
        return t
    

    def nodes(self):
        return self.G.nodes()


    def break_link_stream(self):
        time = self.discrete_time_set()
        for u in self.nodes():
            for t in time:
                self.DG.add_node((u, t))


    def break_links(self):
        time_set = self.discrete_time_set()
        for u, v, attr in sorted(self.G.edges_iter(data=True)):
            for k in range(len(time_set)):
                if attr['start_time'] <= time_set[k] <= attr['end_time']:
                    self.DG.add_edge((u, time_set[k]), (v, time_set[k]))
    
    def discrete_neighbors(self):
        d = {}
        for node in self.DG.nodes_iter():
            d[node] = self.DG.neighbors(node)
        return d
    
    def reachable_node_set(self, node, node_set, temp):
        nodes = node_set
        if node not in nodes:
            return []
        reach = set()
        for i in nodes:
            if i in temp:
                continue
            if i[1] == node[1]:
                reach.add(i)
        if node in reach:
            reach.remove(node)
        t = self.discrete_time_set()
        t_n = t.index(node[1])
        if t_n > 0:
            add_node = (node[0], t[t_n - 1])
            if add_node in temp:
                pass
            else:
                reach.add(add_node)
        if t_n < len(t) - 1:
            add_node = (node[0], t[t_n + 1])
            if add_node in temp:
                pass
            else:
                reach.add(add_node)
        return reach
    
    def reachable_neighbors(self, node):
        n = L.DG.neighbors(node)
        u = node[0]
        t = node[1]
        nodes = []
        for i in n:
            if i[0] == node[0] :
                continue
            yield i[0]


def modules(L):
    list_of_modules = []
    temp = L.DG.nodes()
    node_set = temp[:]
    while node_set:
        current_node = random.choice(node_set)
        module = [current_node]
        count = 0
        temp = set()
        while True:
            S = set()
            current_node_neighbors = list(L.reachable_neighbors(current_node))
            for node in L.reachable_node_set(current_node, node_set, temp):
                if list(L.reachable_neighbors(node)) == current_node_neighbors and not node in temp and node not in module:
                    S.add(node)
                if node[0] == current_node[0]:
                    x = [u for u in L.reachable_neighbors(node)]
                    y = [u for u in current_node_neighbors]
                    if Counter(x) == Counter(y) and node not in temp and node not in module:
                        S.add(node)
            node_set.remove(current_node)
            if len(S) == 0 and len(temp) == 0:
                break
            if len(S) != 0:
                current_node = random.sample(S, 1)[0]
                module.append(current_node)
                S.remove(current_node)
                temp.update(S)
            else:
                current_node = random.sample(temp, 1)[0]
                temp.remove(current_node)
                module.append(current_node)
            count +=1
        print module
        list_of_modules.append(module)
    return list_of_modules



## Example
L = linkstream(4)
L.add_link(1, 2, 4, 5)
L.add_link(1, 3, 4, 5)
L.add_link(4, 2, 4, 5)
L.add_link(4, 3, 4, 5)
L.add_link(1, 2, 1, 2)
L.add_link(1, 3, 1, 2)
print L.links()
print L.discrete_time_set()
print L.G.edges()

L.break_link_stream()
L.break_links()
Ne = L.discrete_neighbors()

print modules(L)


