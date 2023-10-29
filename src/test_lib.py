import networkx as nx

graph = nx.Graph()


set_a = ["a", "b", "c"]
set_b = [1, 2, 3, 4]

graph.add_nodes_from(set_a)
graph.add_nodes_from(set_b)

graph.add_edges_from(
    [
        ("a", 1),
        ("a", 4),
        ("b", 2),
        ("c", 1),
    ]
)

print(nx.bipartite.maximum_matching(graph, top_nodes=set_a))


