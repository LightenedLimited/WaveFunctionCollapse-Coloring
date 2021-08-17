def run(nodes, colors, connections, available_colors, entropy, output):
    global min_index
    global affected_nodes
    global FINISHED
    global RESTART_FLAG
    
    FINISHED = False
    RESTART_FLAG = False
    affected_nodes = []
    min_index = -1

    def restart_wfc():
        global available_colors, entropy, output
        available_colors = [[True for _ in range(colors)] for _1 in range(nodes)]
        entropy = [colors for _ in range(nodes)]
        output = [-1 for _ in range(nodes)]


#returns the index of the lowest entropy
    def find_lowest_entropy():
        global colors
        global min_index
        global FINISHED 
        global RESTART_FLAG
        min_value = colors+1
        FINISHED = True
        for index, val in enumerate(entropy):
            #collapsed nodes
            if val == -1:
                continue
            if val == 0:
                RESTART_FLAG = True
                restart_wfc()
            if(min_value > val):
                min_value = val
                min_index = index
                FINISHED = False
            

    def observe():
        find_lowest_entropy()


    def collapse(index):
        global entropy, available_colors, output, affected_nodes
        if not(FINISHED):
            if(entropy[index] == 0):
                raise Exception("Impossible pattern")
            entropy[index] = -1
            affected_nodes.append(index)
            #pick lowest available color
            flag = True
            color_index = available_colors[index].index(True)
            available_colors[index] = [False] * colors
            available_colors[index][color_index] = True
            output[index] = color_index


    def propogate():
        visisted = [False for _ in range(nodes)]
        while len(affected_nodes) > 0:
            index = affected_nodes.pop()
            #find first available color
            color_index = available_colors[index].index(True)
            #calculate impact
            for node_index in range(nodes):
                #check if connected and is not collapsed
                if connections[index][node_index] and entropy[node_index] != -1:
                    if(available_colors[node_index][color_index] == True):
                        available_colors[node_index][color_index] = False
                        entropy[node_index] -= 1
                    if entropy[node_index] == 0:
                        raise Exception("Found error in propogation")
                    if entropy[node_index] == 1 and not(visisted[node_index]):
                        visisted[node_index] = True
                        #collapse 
                        affected_nodes.append(node_index)

    while not(FINISHED):
        RESTART_FLAG = False
        observe()
        if(min_index == -1):
            break
        if RESTART_FLAG:
            continue
        collapse(min_index)
        propogate()
    return output

if __name__ == "__main__":
    import timeit
    import os
    from utils import verify_graph
    import time
    for filename in os.listdir("./data"):
        if(filename.endswith("b") or filename.startswith(".")):
            continue
        connections = [[]]
        available_colors = [[]]
        nodes = -1
        colors = -1
        entropy = []
        affected_nodes = []
        output = []
        degrees = []
        max_degree = 0

        with open("./data/"+filename, "r") as file:
            for line in file.readlines():
                line = line.strip()
                if(line.split(" ")[0] == "p"):
                    #this is beginning line
                    nodes = int(line.split(" ")[2])
                    connections = [[False for _ in range(nodes)] for _1 in range(nodes)]
                    
                    output = [-1] * nodes
                    degrees = [0] * nodes
                if(line.split(" ")[0] == "e"):
                    index_1 = int(line.split(" ")[1])-1
                    index_2 = int(line.split(" ")[2])-1
                    connections[index_1][index_2] = True
                    connections[index_2][index_1] = True
                    degrees[index_1] += 1 
                    degrees[index_2] += 1
        colors = max(degrees) + 1
        available_colors = [[True for _ in range(colors)] for _1 in range(nodes)]
        entropy = [colors] * nodes
        output = run(nodes, colors, connections, available_colors, entropy, output)
        #micro seconds
        print(filename, verify_graph(output, connections), nodes, len(set(output)), timeit.timeit('run(nodes, colors, connections, available_colors, entropy, output)', number = 100, globals=globals()) / 100 * 10 ** 6, sep=",", end="\n")
        # print(verify_graph(output, connections))
        # print(nodes)
        # print(len(set(output)))
        # print(filename)
        # print(timeit.timeit('run(nodes, colors, connections, available_colors, entropy, output)', number = 100, globals=globals()) / 100)
    pass