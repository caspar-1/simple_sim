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
    model.create_plot(2,1,title="test 1")
    sine_1=blocks.sources.sine_generator(freq=100,amplitude=1)
    noise=blocks.sources.Noise_generator(amplitude=0.1)
    sum=blocks.functions.Sum()
   
    absolute=blocks.functions.ABS(name="TEST_ABS")
    buff_1=blocks.functions.Buffer(sz=2048)
    buff_2=blocks.functions.Buffer(sz=512)
    ep=blocks.loads.end_point()
    fft=blocks.dsp.FFT(normalise=False)
    fft_d=blocks.dsp.FFT_DISPLAY()
    ifft=blocks.dsp.FFT()
    p1=blocks.display.Plot_Wndw(ax=model.axes[0],ylim=(-2,2))
    p2=blocks.display.Plot_Wndw(ax=model.axes[1],ylim=(-60,10))
    l1 = p1.get_line_plot(fmt="b")
    l2 = p2.get_line_plot(fmt="b")


    model.add_block(sine_1)
    model.add_block(noise)
    model.add_block(sum)
    model.add_block(buff_1)
    model.add_block(buff_2)
    model.add_block(fft)
    model.add_block(l1)
    model.add_block(l2)
    model.add_block(fft_d)


    model.link_block(sine_1,sum)
    model.link_block(noise,sum)
    model.link_block(sum,buff_1)
    model.link_block(sum,buff_2)
    model.link_block(buff_1,fft)
    model.link_block(fft,fft_d)
    model.link_block(fft_d,l2)
    model.link_block(buff_2,l1)


    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
