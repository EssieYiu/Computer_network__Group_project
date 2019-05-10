class TopoGraph:
    def __init__(self,n,e):
        self.N=n
        self.E=e
        #名字和ip的对应关系
        self.name_ip={}
        #边和cost的对应关系
        self.link_cost={}
        #node和其所有邻居的对应关系
        self.edge={}
    #获取某个节点的所有邻居以及与邻居的linkcost
    def get_allLink(self,name):




