import pygraphviz as pgv
# http://pygraphviz.github.io/documentation/latest/reference/agraph.html
# http://pygraphviz.github.io/documentation/pygraphviz-1.5/pygraphviz.pdf
from qr import *

def gen_dot(nodes, edges):
    A = pgv.AGraph()

    # A.graph_attr['outputorder']='edgesfirst'
    # A.graph_attr['label']="miles_dat"
    # A.graph_attr['ratio']='1.0'

    A.node_attr['shape']='box'
    # A.node_attr['style']='filled'
    # A.node_attr['fixedsize']='true'
    # A.node_attr['fontsize']='8'
    # A.node_attr['fontcolor']='#FFFFFF'

    # A.edge_attr['color']='#1100FF'
    # A.edge_attr['style']='setlinewidth(2)'

    for idx, node in enumerate(nodes):
        n = A.add_node(idx)
        n.attr['label'] = node

        # n.attr['fillcolor']="#%2x0000"%(i*16)
        # n.attr['height']="%s"%(i/16.0+0.5)
        # n.attr['width']="%s"%(i/16.0+0.5)
        # # assign positions, scale to be something reasonable in points
        # n.attr['pos']="%f,%f)"%(-(float(x)-7000)/10.0,(float(y)-2000)/10.0)
        # # assign node size, in sqrt of 1,000,000's of people 
        # d=math.sqrt(float(pop)/1000000.0)
        # n.attr['height']="%s"%(d/2)
        # n.attr['width']="%s"%(d/2)
        # # assign node color
        # n.attr['fillcolor']="#0000%2x"%(int(d*256))
    for a, b in edges:
        A.add_edge(a, b)
    return A

# assert gen_dot(['a'], [('b','c')]).string() == 'strict graph "" {\n\ta;\n\tb -- c;\n}\n'

def draw_state_graph(sg: StateGraph):
    A = gen_dot(sg.states, sg.edges)
    # return A
    A.write('graph.dot')
    A.draw('graph.svg', prog='neato', args='-n2')
    # , prog="circo"
