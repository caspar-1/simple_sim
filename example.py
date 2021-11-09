from simple_sim import runtime,blocks
import logging



logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger=logging.getLogger(__name__)


if __name__=="__main__":

    model=runtime.Model()
    model.create_plot(2,2,title="test 1")
    sine_1=blocks.sine_generator(freq=100,amplitude=1)
    sine_2=blocks.sine_generator(freq=110,amplitude=0.9)
    sine_3=blocks.sine_generator(freq=120,amplitude=0.8)
    sine_4=blocks.sine_generator(freq=130,amplitude=0.7)
    noise=blocks.Noise_generator(amplitude=0.5)
    sum=blocks.Sum()
    mul=blocks.Multiplier()
    absolute=blocks.ABS()
    buff=blocks.Buffer(sz=500)
    ep=blocks.end_point()
    fft=blocks.FFT()
    p1=blocks.Plot(ax=model.axes[0,0])
    p2=blocks.Plot(ax=model.axes[0,1])
    p3=blocks.Plot(ax=model.axes[1,0])
    f=blocks.File_out("test.json")


    model.add_block(sine_1)
    model.add_block(sine_2)
    model.add_block(sine_3)
    model.add_block(sine_4)
    model.add_block(noise)
    model.add_block(sum)
    model.add_block(buff)
    model.add_block(absolute)
    model.add_block(fft)
    model.add_block(p1)
    model.add_block(p2)
    model.add_block(f)


    model.link_block(sine_1,sum)
    model.link_block(sine_2,sum)
    model.link_block(sine_3,sum)
    model.link_block(sine_4,sum)
    model.link_block(noise,sum)
    model.link_block(sum,buff)
    model.link_block(buff,fft)
    model.link_block(fft,absolute)
    model.link_block(absolute,p1)
    model.link_block(buff,p2)
    model.link_block(absolute,f)

    model.init()
    model.run(100000)