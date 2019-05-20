NAMELIST = ['A','B','C','D','E']
INF = 10000000
class LSGraph:
    def __init__(self):
        self.name_ip = {'A':"192.168.199.131",'B':"192.168.39.128","C":"",'D':"192.168.199.205",'E':"192.168.199.102"}
        #self.topo = [[0,1,INF,3,INF],[6,0,5,INF,4],[INF,1,0,INF,INF],[2,INF,INF,0,3],[INF,2,INF,5,0]]
        #self.topo = [[INF,INF,INF,INF,INF],[INF,INF,INF,INF,INF],[INF,INF,INF,INF,INF],[INF,INF,INF,INF,5],[INF,INF,INF,4,INF]] #only D and E exist
        self.topo = [[INF,INF,INF,INF,INF],[INF,INF,INF,4,100],[INF,INF,INF,INF,INF],[INF,5,INF,INF,3],[INF,1,INF,2,INF]] #B D E exist
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

    def get_down_status(self,router_name):
        if router_name == 'A':
            return True
        return False 