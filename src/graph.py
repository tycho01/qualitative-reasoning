import pygraphviz as pgv
# http://pygraphviz.github.io/documentation/latest/reference/agraph.html
# http://pygraphviz.github.io/documentation/pygraphviz-1.5/pygraphviz.pdf
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
        if A.has_node(node):
            A.get_node(node).attr['label'] = label
        # else:
        #     A.add_node(node, label=label)

    A.node_attr['shape']='circle'
    return A

# assert gen_dot(['a'], [('b','c')]).string() == 'strict graph "" {\n\ta;\n\tb -- c;\n}\n'

def draw_state_graph(sg: StateGraph):
    A = gen_dot(sg.states, sg.edges)
    A.write('../graph.dot')
    A.draw('../circo.svg', prog='circo')
    return A
