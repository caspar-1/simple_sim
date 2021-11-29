import sys
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
    ts=0.00001
    display_sz=1000
    model=runtime.Model(time_step=ts)
    model.create_plot(3,1,title="test 1")
    times=np.array([0,5,7,15,20])*0.0001
    amplitudes=[1,0,1,-1,1]
    freq=100
    bits=12

    scale=2**(bits-1)

    #gui controls
    slider_freq=blocks.gui_blocks.Gui_slider(min=100,max=12500,name="Frequency",label="freq",steps=1000)
    rg=blocks.gui_blocks.Gui_RadioGroup(label="source selection",initial=1)
    rg.add_button("sine")
    rg.add_button("square")
    rg.add_button("triangle")
    rg.add_button("list")



    
    source_sin=blocks.sources.sine_generator(freq=freq,offset=0.0,amplitude=1.0)
    source_square=blocks.sources.square_generator(freq=freq,offset=0.0,amplitude=1.0)
    source_triangle=blocks.sources.triangle_generator(freq=freq,offset=0.0,amplitude=1.0,symetry=0.5)
    source_list=blocks.sources.List_Gen(name="list gen",times=times,amplitudes=amplitudes)

    buff_1=blocks.buffers.ROLL(sz=display_sz)
    buff_2=blocks.buffers.Buffer(sz=2048)
   
    p1=blocks.display.Plot_Wndw(model.axes[0],fmt="g",ylim=(-scale,scale),xlim=(0,display_sz*ts))
    p2=blocks.display.Plot_Wndw(model.axes[1],fmt="g",ylim=(-scale,scale),xlim=(0,display_sz*ts))
    p3=blocks.display.Plot_Wndw(model.axes[2],fmt="g",ylim=(-80,20),)
    switch=blocks.functions.Switch()

    l1 = p1.get_line_plot(fmt="r")
    l2 = p2.get_line_plot(fmt="b")
    l3 = p3.get_line_plot(fmt="g")

    window=blocks.dsp.WINDOW(window="blackman")
    fft=blocks.dsp.FFT()
    fft_format=blocks.dsp.FFT_DISPLAY()
    quantize=blocks.functions.Quantize(bits=bits,vref=1)



    
    model.add_block(source_sin)
    model.add_block(source_square)
    model.add_block(source_triangle)
    model.add_block(source_list)
    model.add_block(switch)
    model.add_block(quantize)
    model.add_block(buff_1)
    model.add_block(buff_2)
    model.add_block(window)
    model.add_block(fft)
    model.add_block(fft_format)
    model.add_block(l1)
    model.add_block(l2)
    model.add_block(l3)

    model.add_block(slider_freq)
    model.add_block(rg)
   
    source_sin.freq_input.connect(slider_freq)
    source_square.freq_input.connect(slider_freq)
    source_triangle.freq_input.connect(slider_freq)
    switch.select_input.connect(rg)

    model.link_block(source_sin,switch)
    model.link_block(source_square,switch)
    model.link_block(source_triangle,switch)
    model.link_block(source_list,switch)
    model.link_block(switch,quantize)
    model.link_block(quantize,buff_1)

    model.link_block(quantize,buff_2)
    model.link_block(buff_2,window)
    model.link_block(window,fft)
    
    
    
    model.link_block(buff_1,l1)
    model.link_block(window,l2)
    
    model.link_block(fft,fft_format)
    model.link_block(fft_format,l3)



    try:
        model.init()
        model.run(2000000)
    except custom_exceptions.Model_runtime_exception:
        pass
