import logging
import numpy as np
from scipy import signal
from . import exceptions as excpt
from .block import Block,Input,NamedInput

from . import data as data

logger = logging.getLogger(__name__)


class source(Block):
    def __init__(self, n_max, name):
        super().__init__(n_max, self.__class__.__name__, name)

    def get_out_data_type(self):
        return self.data_obj.data_type


class sine_generator(source):

    def __init__(self, name:str=None,freq:float=1.0,amplitude:float=1.0,phase:float=0.0,offset:float=0.0):
        name = name if name else self.__class__.__name__
        super().__init__(n_max=0,name=name)
        _freq = freq
        _amplitude = amplitude
        _phase_rads = phase
        _offset = offset


        self.freq_input = NamedInput("frequency", _freq)
        self.amplitude_input = NamedInput("amplitude", _amplitude)
        self.phase_input = NamedInput("phase", _phase_rads)
        self.offset_input = NamedInput("offset", _offset)

        self.data_obj = data.STREAM_DATA()
        self.input_frequency = None

    def run(self, ts):
        _freq = self.freq_input.get()
        _amp = self.amplitude_input.get()
        _phase = self.phase_input.get()
        _offset = self.offset_input.get()

        s=_offset+(_amp*np.sin(2*np.pi*_freq*ts+_phase))
        self.data_obj.set_data(s)
        self.out_data_valid = True
        return False



class square_generator(source):

    def __init__(self, name:str=None,freq:float=1.0,amplitude:float=1.0,phase:float=0.0,offset:float=0.0):
        name = name if name else self.__class__.__name__
        super().__init__(n_max=0,name=name)
        _freq = freq
        _amplitude = amplitude
        _phase_rads = phase
        _offset = offset

        self.freq_input = NamedInput("frequency", _freq)
        self.amplitude_input = NamedInput("amplitude", _amplitude)
        self.phase_input = NamedInput("phase", _phase_rads)
        self.offset_input = NamedInput("offset", _offset)

        self.data_obj = data.STREAM_DATA()
        self.input_frequency = None

    def run(self, ts):
        _freq = self.freq_input.get()
        _amp = self.amplitude_input.get()
        _phase = self.phase_input.get()
        _offset = self.offset_input.get()

        _period=1.0/_freq
        
        
        d=(ts%_period)/_period
        data=-1 if d<0.5 else 1.0
        s=_offset+(_amp*data)


        self.data_obj.set_data(s)
        self.out_data_valid = True
        return False




class triangle_generator(source):

    def __init__(self, name:str=None,freq:float=1.0,amplitude:float=1.0,symetry:float=0.5,offset:float=0.0):
        name = name if name else self.__class__.__name__
        super().__init__(n_max=0,name=name)
        _freq = freq
        _amplitude = amplitude
        _symetry = symetry
        _offset = offset

        self.freq_input = NamedInput("frequency", _freq)
        self.amplitude_input = NamedInput("amplitude", _amplitude)
        self.symetry_input = NamedInput("symetry", _symetry)
        self.offset_input = NamedInput("offset", _offset)

        self.data_obj = data.STREAM_DATA()
        self.sig=0.0

    def run(self, ts):
        _freq = self.freq_input.get()
        _amp = self.amplitude_input.get()*2.0
        _symetry = self.symetry_input.get()
        _offset = self.offset_input.get()-1.0

        

        _period=1.0/_freq
        
        
        d=(ts%_period)/_period
        sym=_symetry
        if d<sym:
            slope=(1/sym)
            s=(d*slope)
        else:
            slope=1/(1.0-sym)
            s=1.0-((d-sym)*slope)

        
        self.data_obj.set_data((s*_amp)+_offset)
        self.out_data_valid = True
        return False



class Noise_generator(source):
    def __init__(self, name:str=None,amplitude:float=1.0):
        name = name if name else self.__class__.__name__
        super().__init__(n_max=0,name=name)
        _amplitude = amplitude
        self.amplitude_input = NamedInput("amplitude", _amplitude)
        self.data_obj = data.STREAM_DATA()


    def run(self, ts):
        _amp = self.amplitude_input.get()
        self.data_obj.set_data(_amp*np.random.randn())
        self.out_data_valid = True
        return False


class Random_Digital_generator(source):
    def __init__(self, name:str=None,nbits:int=8):
        name = name if name else self.__class__.__name__
        super().__init__(n_max=0, name=name)
        self.buff_size = nbits
        self.data_obj = data.ARRAY_DATA(self.buff_size, data_type=data.DATA_TYPES.BOOL)


    def run(self, ts):
        self.data_obj.set_data(np.random.binomial(n=1, p=0.5, size=(self.buff_size)))
        self.out_data_valid = True
        return False






class List_Gen(source):
    def __init__(self, name:str=None,times=None,amplitudes=None):
        name = name if name else self.__class__.__name__
        super().__init__(n_max=0, name=name)
        self.data_obj = data.STREAM_DATA()
        self.list_idx=0
        self.t_offset=0.0
        self.pulse_list_time=np.array(times)
        self.pulse_list_amp=np.array(amplitudes)
        self.n=len(times)
        if ((times is None)or(amplitudes is None)):
            raise excpt.Block_exception_invalid_input_data()

    def initialise(self,model_obj):
        super().initialise(model_obj)
        pass
    
    
    def run(self, ts):
        
        last_idx=self.list_idx
        next_idx=self.list_idx+1

        if next_idx==self.n:
            next_idx=0
      
        t_last=self.pulse_list_time[last_idx]+self.t_offset
        t_next=self.pulse_list_time[next_idx]+self.t_offset
        a_last=self.pulse_list_amp[last_idx]
        a_next=self.pulse_list_amp[next_idx]

        if next_idx==0:
            t_next_adj=t_next+self.pulse_list_time[last_idx]
        else:
            t_next_adj=t_next


        #interpolate data
        if t_next_adj!=t_last:
            delta=(ts-t_last)/abs(t_next_adj-t_last)
            amplitude=((delta*(a_next-a_last))+a_last)
            if amplitude is np.nan:
                pass
            else:
                self.data_obj.set_data(amplitude)


        if(ts>=t_next_adj):
            self.list_idx+=1
            if (self.list_idx==self.n):
                self.list_idx=0
                self.t_offset=ts

           


        self.out_data_valid = True
        return False