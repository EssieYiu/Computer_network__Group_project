import random
class TopoGraph:
    def __init__(self,n,e):
        self.N=n
        self.E=e
        #名字和ip的对应关系
        self.name_ip={}
        #边和cost的对应关系
        self.link_cost={}

    #获取某个节点的所有邻居以及与邻居的linkcost
    def get_allLink(self,name):
        my_ip=name_ip[name]
        allLink={}  #节点->cost
        for link,cost in self.link_cost.items():
            if my_ip in link:
                neigh_ip=(link[0] if link[0]!=ip else link[1]) #邻居的ip
                allLink[neigh_ip]=cost
        return allLink

    def change_linkCost(self):
        for link in self.link_cost.keys():
            new_cost=random.randint(1,50)
            self.link_cost[link]=new_cost
        print("* Link cost has changed!")
