from graph import Graph
from util import Queue

def earliest_ancestor(ancestors, starting_node):
    # create graph and terminus path list
    ancestor_graph = Graph()
    terminus = []
    # add parent and child relationships to graph
    for parent, child in ancestors:
        if child not in ancestor_graph.vertices:
            ancestor_graph.add_vertex(child)
        if parent not in ancestor_graph.vertices:
            ancestor_graph.add_vertex(parent)
        ancestor_graph.add_edge(child, parent)
    # create queue and add starting node
    q = Queue()
    q.enqueue([starting_node])
    # create visited set and traverse entire graph
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if ancestor_graph.get_neighbors(v)==set():
            terminus.append(path)
        if v not in visited:
            visited.add(v)
            for neighbor in ancestor_graph.get_neighbors(v):
                p = path.copy()
                p.append(neighbor)
                q.enqueue(p)
    # get max length of ancestry 
    m_len = max(len(p) for p in terminus)
    longest = [p for p in terminus if len(p) == m_len]
    if m_len == 1:
        return -1
    if len(longest) == 1:
        return longest[0][-1]
    if len(longest) > 1:
        possible = [p[-1] for p in longest]
        return min(possible)