import sys
from simplesimulator import runtime, blocks, custom_exceptions
import logging


logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    model = runtime.Model()
    model.create_plot(2, 2, title="test 1")
    sine_1 = blocks.sources.sine_generator(freq=10, amplitude=1.0)
    sine_2 = blocks.sources.sine_generator(freq=20, amplitude=1.0)
    sine_3 = blocks.sources.sine_generator(freq=120, amplitude=1.0)
    sine_4 = blocks.sources.sine_generator(freq=130, amplitude=1.0)
    sine_5 = blocks.sources.sine_generator(freq=140, amplitude=1.0)
    sine_6 = blocks.sources.sine_generator(freq=150, amplitude=1.0)
    noise = blocks.sources.Noise_generator(amplitude=0.01)
    sum = blocks.functions.Sum()
    mul = blocks.functions.Multiplier()
    absolute = blocks.functions.ABS(name="TEST_ABS")
    buff = blocks.functions.Buffer(sz=2048)
    ep = blocks.loads.end_point()
    fft = blocks.dsp.FFT()
    fft_d = blocks.dsp.FFT_DISPLAY()
    ifft = blocks.dsp.IFFT()
    p1 = blocks.display.Plot_Wndw(ax=model.axes[0, 0],title="RAW",ylim=(-5,5))
    p2 = blocks.display.Plot_Wndw(ax=model.axes[0, 1],title="WINDOWED",ylim=(-10,10))
    p3 = blocks.display.Plot_Wndw(ax=model.axes[1, 0],title="FFT",ylim=(-80,10))
    p4 = blocks.display.Plot_Wndw(ax=model.axes[1, 1],title="IFFT",ylim=(-10,10))
    window=blocks.dsp.WINDOW()
    real = blocks.functions.REAL(name="REAL")

    l1 = p1.get_line_plot(fmt="r--")
    l2 = p2.get_line_plot(fmt="g")
    l3 = p3.get_line_plot(fmt="b")
    l4 = p4.get_line_plot(fmt="b")

    f = blocks.loads.File_out("test.json")

    model.add_block(sine_1)
    model.add_block(sine_2)
    model.add_block(sine_3)
    model.add_block(sine_4)
    model.add_block(sine_5)
    model.add_block(sine_6)
    model.add_block(noise)
    model.add_block(sum)
    model.add_block(buff)
    model.add_block(fft)
    model.add_block(ifft)
    model.add_block(window)
    model.add_block(absolute)
    model.add_block(real)

    model.add_block(l1)
    model.add_block(l2)
    model.add_block(l3)
    model.add_block(l4)

    model.add_block(f)
    model.add_block(fft_d)

    model.link_block(sine_1, sum)
    model.link_block(sine_2, sum)
    model.link_block(sine_3, sum)
    model.link_block(sine_5, sum)
    model.link_block(sine_6, sum)
    model.link_block(sine_4, sum)
    model.link_block(noise, sum)
    model.link_block(sum, buff)
    model.link_block(buff,window)
    model.link_block(window, fft)
    model.link_block(fft, fft_d)
    model.link_block(fft, ifft)
    model.link_block(ifft, real)

    
    #model.link_block(fft_d, f)

    model.link_block(buff, l1)
    model.link_block(window, l2)
    model.link_block(fft_d, l3)
    model.link_block(real, l4)
    #model.link_block(fft_d, l2)
    #model.link_block(ifft, l3)

    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
