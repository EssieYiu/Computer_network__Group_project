NAMELIST = ['A','B','C','D','E']
INF = 10000000
class LSGraph:
    def __init__(self):
        self.name_ip = {'A':"192.168.199.131",'B':"","C":"",'D':"192.168.199.205",'E':"192.168.199.102"}
        self.topo = [[0,1,INF,3,INF],[6,0,5,INF,4],[INF,1,0,INF,INF],[2,INF,INF,0,3],[INF,2,INF,5,0]]

    def get_name_ip(self):
        return self.name_ip

    def get_neighbour(self,name):
        neighbour = {}
        index = ord(name)-ord('A')
        for i in range(5):
            if self.topo[index][i] != 0  and self.topo[index][i] < INF:
                neighbour[chr(i+ord('A'))] = self.topo[index][i]
        return neighbour
        
    def get_init_topo(self):
        return self.topo