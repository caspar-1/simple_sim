import simpleSimCore as core


class xBlock(core.Block):

    def __init__(self,name):
        super().__init__(name,self.__class__.__name__,0)

    def pre_run(self,ms):
        rr=core.RunResult()
        rr.message="Pre_run"
        print("Pre run:{} {} {}".format(self.name,ms.time,ms.d_time))
        return rr

    def run(self,ms):
        rr=core.RunResult()
        rr.message="run"
        print("Run:{} {} {}".format(self.name,ms.time,ms.d_time))
        return rr


    def post_run(self,ms):
        rr=core.RunResult()
        rr.message="post_run"
        print("Post run:{} {} {}".format(self.name,ms.time,ms.d_time))
        return rr


print(core.version())
print(core.build_date())
px=xBlock("px")
py=xBlock("py")
cx=core.SimpleBlock("cx")
cy=core.SimpleBlock("cy")

print(py.class_id)
print(cy.class_id)

engine=core.Engine()
if True:
    engine.register_block(px)
    engine.register_block(px)
else:
    engine.register_block(cx)
    engine.register_block(cy)

engine.run(100,False)


pass