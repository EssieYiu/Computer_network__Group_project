from node import Node
from TopoGraph import TopoGraph
if __name__ == "__main__":
    my_ip = input('Please enter your ip address')
    my_name = input('Please enter your name')
    Graph = TopoGraph()
    Graph.initialize_graph()
    neighbour=Graph.get_allNeighbour(my_name)
    down=Graph.get_down(my_name)
    my_node = Node(my_name,my_ip,neighbour,down)

    my_node.recompute_DV()


    
