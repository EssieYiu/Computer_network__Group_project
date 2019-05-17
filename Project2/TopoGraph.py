import random
#IP=["172.26.5.44","172.26.81.151","3","4","5"]
<<<<<<< HEAD
A= "192.168.199.131""
=======
A= "192.168.199.131"
>>>>>>> b97f1b4210f2f2782c6401e366c89efaa408a127
B= "127.0.0.1"
C = "127.0.0.1"
D= "192.168.199.205"
E = "192.168.199.102"
class TopoGraph(object):
    def __init__(self):
        #self.N = n
        #self.E=e
        #名字和ip的对应关系
        #x=input("Enter ip:")
        self.name_ip={'A':A,'B':B,'C':C,'D':D,'E':E}
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
        self.link_cost[(A,C)] = 34
        self.link_cost[(A,D)] = 34
        self.link_cost[(A,E)] = 34
        self.link_cost[(B,E)] = 34
        self.link_cost[(B,D)] = 34
        self.link_cost[(C,D)] = 34
        self.ip_changeable_route[A] = [D,E]
        self.ip_changeable_route[B] = []
        self.ip_changeable_route[C] = [A,D]
        self.ip_changeable_route[D] = [B]
        self.ip_changeable_route[E] = [B]

        
        print(self.link_cost)

    def node_changeable_route(self,node_ip):
        return self.ip_changeable_route[node_ip]

    def get_down(self,name):
        if name=='A':
            return True
        else:
            return False
