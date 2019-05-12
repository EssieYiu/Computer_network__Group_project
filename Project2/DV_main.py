from node import Node
from TopoGraph import TopoGraph
if __name__ == "__main__":
    my_ip = input('Please enter your ip address')
    my_name = input('Please enter your name')
    Graph = TopoGraph('e','n')
    Graph.initialize_graph()
    local_node = Node(my_name,my_ip)
    
