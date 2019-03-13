import pygraphviz as pgv

def gen_dot(nodes, edges):
    G = pgv.AGraph()
    for node in nodes:
        G.add_node(node)
    for a, b in edges:
        G.add_edge(a, b)
    return G.string()

assert gen_dot(['a'], [('b','c')]) == 'strict graph "" {\n\ta;\n\tb -- c;\n}\n'
