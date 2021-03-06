import random
from My_node import IP
A = IP[0]
B = IP[1]
C = IP[2]
D = IP[3]
E = IP[4]
class TopoGraph(object):
    def __init__(self):
        #名字和ip的对应关系
        self.name_ip={'A':A,'B':B,'C':C,'D':D,'E':E}
        #边和cost的对应关系
        self.link_cost={}
        self.ip_changeable_route = {} #ip->list[nei1,nei2...],IP地址到list的映射关系，其中list存储邻居ip，表示它能修改到此邻居的路径权重
        self.link_cost[(A,C)] = 15
        self.link_cost[(A,D)] = 21
        self.link_cost[(A,E)] = 16
        self.link_cost[(B,E)] = 12
        self.link_cost[(B,D)] = 12
        self.link_cost[(C,D)] = 12
        self.ip_changeable_route[A] = [D,E]
        self.ip_changeable_route[B] = []
        self.ip_changeable_route[C] = [A,D]
        self.ip_changeable_route[D] = [B]
        self.ip_changeable_route[E] = [B]

        print(self.link_cost)
    #获取某个节点的所有邻居以及与邻居的linkcost
    def get_allNeighbour(self,name):
        my_ip=self.name_ip[name]
        allLink={}  #节点->cost
        for link,cost in self.link_cost.items():
            if my_ip in link:
                neigh_ip=(link[0] if link[0]!=my_ip else link[1]) #邻居的ip
                allLink[neigh_ip]=cost

        return allLink

    def get_changeable_route(self,node_ip):
        return self.ip_changeable_route[node_ip]

