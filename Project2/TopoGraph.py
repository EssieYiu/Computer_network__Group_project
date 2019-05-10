import random
IP1 = ""
IP2 = ""
IP3 = ""
IP4 = ""
IP5 = ""
class TopoGraph:
    def __init__(self,e,n):
        self.N = n
        self.E=e
        #名字和ip的对应关系
        self.name_ip={}
        #边和cost的对应关系
        self.link_cost={}

    #获取某个节点的所有邻居以及与邻居的linkcost
    def get_allLink(self,name):
        my_ip=self.name_ip[name]
        allLink={}  #节点->cost
        for link,cost in self.link_cost.items():
            if my_ip in link:
                neigh_ip=(link[0] if link[0]!=ip else link[1]) #邻居的ip
                allLink[neigh_ip]=cost
        return allLink

    def initialize_graph(self):
        self.link_cost[(IP1,IP3)] = 34
        self.link_cost[(IP1,IP5)] = 34
        self.link_cost[(IP2,IP5)] = 34
        self.link_cost[(IP2,IP4)] = 34
        self.link_cost[(IP3,IP4)] = 34

    def change_linkCost(self):
        self.link_cost[(IP1,IP3)] = random.randint(0,50)
        self.link_cost[(IP1,IP5)] = random.randint(0,50)
        self.link_cost[(IP2,IP5)] = random.randint(0,50)
        self.link_cost[(IP2,IP4)] = random.randint(0,50)
        self.link_cost[(IP3,IP4)] = random.randint(0,50)






