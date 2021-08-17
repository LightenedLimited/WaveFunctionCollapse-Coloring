def verify_graph(coloring, connections):
    nodes = len(coloring)
    for node_index in range(nodes):
        color = coloring[node_index]
        for compare_index in range(nodes):
            if compare_index == node_index:
                continue
            if connections[node_index][compare_index] or connections[compare_index][node_index]:
                #check color
                if color == coloring[compare_index]:
                    return False
    return True