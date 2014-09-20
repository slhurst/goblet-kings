from ideal_graph import create_graph


def getBoard(g, status):
    if not g:
        g = create_graph()
    occupied = status
    for k, v in status.iteritems():
        if v:
            continue
        else:
            occupied[k] = True 
            return (g, occupied)



