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
        ip=name_ip[name]
        allLink={}  #节点->cost
        for link,cost in self.link_cost.items():
            if ip in link:
                n=(link[0] if link[0]!=ip else link[1])
                allLink[n]=cost
        return allLink

    def change_linkCost(self,A,B,new_cost):
        ipA=name_ip[A]
        ipB=name_ip[B]
        self.link_cost






