from collections import Counter

def is_square(x):
    x = x**0.5
    return int(x) == x

def expected_counter(size):
    x = int(size**0.5)
    return Counter({3:4, 5:4*(x-2), 8:(x-2)**2})

def validate_board(graph):
    nodes = graph.nodes()
    size = len(nodes)
    if not is_square(size):
        return False
    c = Counter(graph.node_order(n) for n in nodes)

    return c == expected_counter(size)
    
