import random
IP1 = ""
IP2 = ""
IP3 = ""
IP4 = ""
IP5 = ""
class TopoGraph(object):
    def __init__(self):
        #self.N = n
        #self.E=e
        #名字和ip的对应关系
        self.name_ip={'A':IP1,'B':IP2,'C':IP3,'D':IP4,'E':IP5}
        #边和cost的对应关系
        self.link_cost={}
        self.ip_changeable_route = {} #ip->list[nei1,nei2...],IP地址到list的映射关系，其中list存储邻居ip，表示它能修改到此邻居的路径权重

    #获取某个节点的所有邻居以及与邻居的linkcost
    def get_allNeighbour(self,name):
        my_ip=self.name_ip[name]
        allLink={}  #节点->cost
        for link,cost in self.link_cost.items():
            if my_ip in link:
                neigh_ip=(link[0] if link[0]!=my_ip else link[1]) #邻居的ip
                allLink[neigh_ip]=cost
        return allLink

    def initialize_graph(self):
        self.link_cost[(IP1,IP3)] = 34
        self.link_cost[(IP1,IP4)] = 34
        self.link_cost[(IP1,IP5)] = 34
        self.link_cost[(IP2,IP5)] = 34
        self.link_cost[(IP2,IP4)] = 34
        self.link_cost[(IP3,IP4)] = 34
        self.ip_changeable_route[IP1] = [IP4,IP5]
        self.ip_changeable_route[IP2] = []
        self.ip_changeable_route[IP3] = [IP1,IP4]
        self.ip_changeable_route[IP4] = [IP2]
        self.ip_changeable_route[IP5] = [IP2]

    def node_changeable_route(self,node_ip):
        return self.ip_changeable_route[node_ip]

    def get_down(self,name):
        if name=='A':
            return True
        else:
            return False
