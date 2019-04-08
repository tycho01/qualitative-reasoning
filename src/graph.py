import pygraphviz as pgv
from qr import *

def gen_dot(states, edges):
    A = pgv.AGraph(
        directed=True,
        overlap=False,
        splines=True,
        sep=+1.2,
        normalize=True,
        smoothing='avg_dist'
    )

    A.add_edges_from(edges)

    for node, entity_state in states.items():
        label = pretty_print(entity_state)
        tooltip = intra_state_trace(entity_state)
        if A.has_node(node):
            A.get_node(node).attr['label'] = label
            A.get_node(node).attr['tooltip'] = tooltip
        else:
            A.add_node(node, label=label, tooltip=tooltip)

    for a, b in edges:
        e = A.get_edge(a, b)
        tooltip = inter_state_trace(states[a], states[b])
        e.attr['tooltip'] = tooltip

    A.node_attr['shape']='circle'
    return A

# assert gen_dot(['a'], [('b','c')]).string() == 'strict graph "" {\n\ta;\n\tb -- c;\n}\n'

def draw_state_graph(sg: StateGraph):
    A = gen_dot(sg.states, sg.edges)
    A.write('../graph.dot')
    A.draw('../graph.svg', prog='circo')
    return A
