import sys

DEVEL=True

if DEVEL:
    local_path="./src/"
    if local_path not in sys.path:
        sys.path.append(local_path)


import simple_sim
from simple_sim import runtime,blocks,custom_exceptions
import logging



logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger=logging.getLogger(__name__)


if __name__=="__main__":

    model=runtime.Model()
    model.create_plot(1,2,title="test 1")
    source_1=blocks.sources.Random_Digital_generator(nbits=128)
    
    p1=blocks.display.Plot_Wndw(model.axes[0],fmt="g",drawstyle="steps",title="BitStream")
    p2=blocks.display.Plot_Wndw(model.axes[1])
    l1 = p1.get_line_plot(fmt="b")
    l2 = p2.get_line_plot(fmt="b")


    model.add_block(source_1)
    
    model.add_block(l1)
    model.add_block(l2)
   
    model.link_block(source_1,l1)
    model.link_block(source_1,l2)

    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
