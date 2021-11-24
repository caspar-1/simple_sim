import sys

DEVEL=True

if DEVEL:
    local_path="./src/"
    if local_path not in sys.path:
        sys.path.append(local_path)


import simplesimulator
from simplesimulator import runtime,blocks,custom_exceptions
import logging
import numpy as np


logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger=logging.getLogger(__name__)


if __name__=="__main__":

    model=runtime.Model(time_step=1e-3)
    model.create_plot(1,2,title="Simple Mixer")
    sine_1=blocks.sources.sine_generator(freq=300,amplitude=1,phase=0.5)
    sine_2=blocks.sources.sine_generator(freq=300,amplitude=1)
    noise_1=blocks.sources.Noise_generator(amplitude=0.01)
    slider_freq=blocks.gui_controls.Gui_slider(min=250,max=350,name="Frequency",steps=1000)
    slider_phase=blocks.gui_controls.Gui_slider(min=0,max=np.pi*2,name="Phase")
    slider_noise=blocks.gui_controls.Gui_slider(min=0,max=2,name="Noise")
    buff_1 = blocks.functions.Buffer(sz=600)
    buff_2 = blocks.functions.Buffer(sz=600)
    buff_3 = blocks.functions.Buffer(sz=600)
    sum = blocks.functions.Sum()
    mul = blocks.functions.Multiplier()
    fft=blocks.dsp.FFT()
    fft_d = blocks.dsp.FFT_DISPLAY()
    window=blocks.dsp.WINDOW()
    filter=blocks.dsp.FILTER_CHEB_LP(wn=0.15)
   
    p1=blocks.display.Plot_Wndw(ax=model.axes[0],ylim=(-2,2))
    p2=blocks.display.Plot_Wndw(ax=model.axes[1],ylim=(-100,0),xlim=(0,600))
    l1 = p1.get_line_plot(fmt="b")
    l2 = p2.get_line_plot(fmt="b")


    model.add_block(sine_1)
    model.add_block(sine_2)
    model.add_block(noise_1)

    model.add_block(buff_1)
    model.add_block(buff_2)
    model.add_block(buff_3)

    model.add_block(mul)
    model.add_block(sum)

    model.add_block(slider_freq)
    model.add_block(slider_phase)
    model.add_block(slider_noise)

    model.add_block(window)
    model.add_block(filter)
    model.add_block(fft)
    model.add_block(fft_d)
    model.add_block(l1)
    model.add_block(l2)

    sine_1.freq_input.connect(slider_freq)
    sine_1.phase_input.connect(slider_phase)
    noise_1.amplitude_input.connect(slider_noise)

    model.link_block(sine_1,buff_1)
    model.link_block(sine_2,buff_2)
    model.link_block(noise_1,buff_3)
    
    model.link_block(buff_1,mul)
    model.link_block(buff_2,mul)
    model.link_block(mul,sum)
    model.link_block(buff_3,sum)

    model.link_block(sum,filter)
    model.link_block(filter,l1)
    model.link_block(filter,window)
    model.link_block(window,fft)
    model.link_block(fft,fft_d)
    model.link_block(fft_d,l2)



    try:
        model.init()
        model.run(100000000)
    except custom_exceptions.Model_runtime_exception:
        pass
