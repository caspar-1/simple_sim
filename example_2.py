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
    sine_1=blocks.sources.sine_generator(freq=10.0,amplitude=1)
    rate_down=blocks.functions.RATE_CHANGE(rate=0.05)
    rate_up=blocks.functions.RATE_CHANGE()
    p1=blocks.display.Plot(ax=model.axes[0])
    p2=blocks.display.Plot(ax=model.axes[1])
    buff_1=blocks.functions.Buffer(sz=500)
    buff_2=blocks.functions.Buffer(sz=500)


    model.add_block(sine_1)
    model.add_block(rate_down)
    model.add_block(rate_up)
    model.add_block(p1)
    model.add_block(p2)
    model.add_block(buff_1)
    model.add_block(buff_2)

    model.link_block(sine_1,rate_down)
    model.link_block(rate_down,rate_up)

    model.link_block(sine_1,buff_1)
    model.link_block(rate_up,buff_2)

    model.link_block(buff_1,p1)
    model.link_block(buff_2,p2)

    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
