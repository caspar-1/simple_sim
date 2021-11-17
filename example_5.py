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
    model.create_plot(1,1,title="test 1")
    sine_1=blocks.sources.sine_generator(freq=50,amplitude=1)
    slider=blocks.gui_controls.Gui_slider(min=-1,max=1)
    buff = blocks.functions.Buffer(sz=500)
    sum = blocks.functions.Sum()
   
    p1=blocks.display.Plot_Wndw(ax=model.axes)
    l1 = p1.get_line_plot(fmt="b")


    model.add_block(sine_1)
    model.add_block(l1)
    model.add_block(buff)
    model.add_block(slider)
    model.add_block(sum)

    model.link_block(sine_1,sum)
    model.link_block(slider,sum)
    model.link_block(sum,buff)
    model.link_block(buff,l1)


    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
