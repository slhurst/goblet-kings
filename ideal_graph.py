from pygraph.classes.graph import graph
from xs_and_os_validator import validate

def g():
    return g

g = graph()
g.add_node("1")
g.add_node("2")
g.add_node("3")
g.add_node("4")
g.add_node("5")
g.add_node("6")
g.add_node("7")
g.add_node("8")
g.add_node("9")

g.add_edge(("1","2"))
g.add_edge(("1","4"))
g.add_edge(("1","5"))
g.add_edge(("2","3"))
g.add_edge(("2","4"))
g.add_edge(("2","5"))
g.add_edge(("2","6"))
g.add_edge(("3","5"))
g.add_edge(("3","6"))
g.add_edge(("4","5"))
g.add_edge(("4","7"))
g.add_edge(("4","8"))
g.add_edge(("5","6"))
g.add_edge(("5","7"))
g.add_edge(("5","8"))
g.add_edge(("5","9"))
g.add_edge(("6","8"))
g.add_edge(("6","9"))
g.add_edge(("7","8"))
g.add_edge(("8","9"))

print validate(g)





