import sys
from simplesimulator import runtime,blocks,custom_exceptions
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
    sine_1=blocks.sources.sine_generator(freq=10.1,amplitude=1)
    noise=blocks.sources.Noise_generator(amplitude=0.01)
    sum=blocks.functions.Sum()
    rate_down=blocks.dsp.RATE_CHANGE(rate=0.1)
    rate_up=blocks.dsp.RATE_CHANGE()
    p1=blocks.display.Plot_Wndw(ax=model.axes[0],title="sss",ylim=(-2,2))
    p2=blocks.display.Plot_Wndw(ax=model.axes[1],ylim=(-2,2))
    l1 = p1.get_line_plot(fmt="g")
    l2 = p2.get_line_plot(fmt="r")
    buff_1=blocks.functions.Buffer(sz=500)
    buff_2=blocks.functions.Buffer(sz=500)


    model.add_block(sine_1)
    model.add_block(noise)
    model.add_block(sum)
    model.add_block(rate_down)
    model.add_block(rate_up)
    model.add_block(buff_1)
    model.add_block(buff_2)
    model.add_block(l1)
    model.add_block(l2)
    


    model.link_block(sine_1,sum)
    model.link_block(noise,sum)
    model.link_block(sum,buff_1)

    model.link_block(sum,rate_down)
    model.link_block(rate_down,rate_up)

    model.link_block(rate_up,buff_2)

    model.link_block(buff_1,l1)
    model.link_block(buff_2,l2)

    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
