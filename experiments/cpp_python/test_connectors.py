import simpleSimCore as core

class xBlock(core.pyBlock):

    def __init__(self,name):
        super().__init__(name,self.__class__.__name__,0)
        self.in_a=self.add_input_connector("A")
        self.in_b=self.add_input_connector("B")
        self.in_c=self.add_input_connector("C")
        self.in_d=self.add_input_connector("D")
        self.out_a=self.add_output_connector("A")
        self.out_b=self.add_output_connector("B")
        self.iout_c=self.add_output_connector("C")
        self.out_d=self.add_output_connector("D")
        print(self.out_d.name)
        print(self.out_d.owner.name)
        print(self.in_d.direction())
        print(self.out_d.direction())


    def pre_run(self,ms):
        pass

    def run(self,ms):
        pass

    def post_run(self,ms):
        pass

    def __repr__(self):
        return """{{"name":"{}","class_id":"{}"}} """.format(self.name,self.class_id)




def do(obj):
    obj.enable_debug()
    #a=obj.get_input_connector_byname("B")
    
  

if __name__=="__main__":
    x=xBlock("source")
    y=xBlock("load")

    y.enable_debug()
    y.in_a.connect(x.out_a)
    y.in_b.connect(x.out_b)
    y.in_c.connect(x.out_b)

    simple_a=core.BlockSimple("simple_a")
    simple_b=core.BlockSimple("simple_b")

    do(simple_a)

    print(x)

