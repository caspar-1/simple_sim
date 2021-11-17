import sys
DEVEL = True

if DEVEL:
    local_path = "./src/"
    if local_path not in sys.path:
        sys.path.append(local_path)
        
from simple_sim import runtime, blocks, custom_exceptions
import logging
import simple_sim





logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    model = runtime.Model()
    model.create_plot(2, 2, title="test 1")
    sine_1 = blocks.sources.sine_generator(freq=100, amplitude=1)
    sine_2 = blocks.sources.sine_generator(freq=110, amplitude=0.9)
    sine_3 = blocks.sources.sine_generator(freq=120, amplitude=0.8)
    sine_4 = blocks.sources.sine_generator(freq=130, amplitude=0.7)
    noise = blocks.sources.Noise_generator(amplitude=0.1)
    sum = blocks.functions.Sum()
    mul = blocks.functions.Multiplier()
    absolute = blocks.functions.ABS(name="TEST_ABS")
    buff = blocks.functions.Buffer(sz=500)
    ep = blocks.loads.end_point()
    fft = blocks.dsp.FFT(normalise=True)
    fft_d = blocks.dsp.FFT_DISPLAY()
    ifft = blocks.dsp.FFT()
    p1 = blocks.display.Plot_Wndw(ax=model.axes[0, 0],title="sss")
    p2 = blocks.display.Plot_Wndw(ax=model.axes[0, 1])
    p4 = blocks.display.Plot_Wndw(ax=model.axes[1, 1])

    l1 = p1.get_line_plot(fmt="r--")
    l2 = p2.get_line_plot(fmt="g")
    l3 = p4.get_line_plot(fmt="b")

    f = blocks.loads.File_out("test.json")

    model.add_block(sine_1)
    model.add_block(sine_2)
    model.add_block(sine_3)
    model.add_block(sine_4)
    model.add_block(noise)
    model.add_block(sum)
    model.add_block(buff)
    model.add_block(fft)
    model.add_block(ifft)


    model.add_block(l1)
    model.add_block(l2)
    model.add_block(l3)

    model.add_block(f)
    model.add_block(fft_d)

    model.link_block(sine_1, sum)
    model.link_block(sine_2, sum)
    model.link_block(sine_3, sum)
    model.link_block(sine_4, sum)
    model.link_block(noise, sum)
    model.link_block(sum, buff)
    model.link_block(buff, fft)
    model.link_block(fft, fft_d)
    model.link_block(fft, ifft)
    model.link_block(fft_d, l2)
    model.link_block(buff, l1)
    model.link_block(fft_d, f)
    model.link_block(ifft, l3)

    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
