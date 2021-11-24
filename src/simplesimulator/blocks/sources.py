import logging
import numpy as np
from . import exceptions as excpt
from .block import Block,Input,NamedInput

from . import data as data

logger = logging.getLogger(__name__)


class source(Block):
    def __init__(self, n_max, block_class, name):
        super().__init__(n_max, block_class, name)

    def get_out_data_type(self):
        return self.data_obj.data_type





class sine_generator(source):

    def __init__(self, **kwargs):
        name = kwargs.get("name", sine_generator.__name__)
        super().__init__(n_max=0, block_class=sine_generator.__name__, name=name)
        _freq = kwargs.get("freq", 1)
        _apmplitude = kwargs.get("amplitude", 1.0)
        _phase_rads = kwargs.get("phase", 0.0)

        self.freq_input = NamedInput("frequency", _freq)
        self.amplitude_input = NamedInput("amplitude", _apmplitude)
        self.phase_input = NamedInput("phase", _phase_rads)

        self.data_obj = data.STREAM_DATA()
        self.input_frequency = None

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self, ts):
        _freq = self.freq_input.get()
        _amp = self.amplitude_input.get()
        _phase = self.phase_input.get()

        self.data_obj.set_data(_amp*np.sin(2*np.pi*_freq*ts+_phase))
        self.out_data_valid = True
        return False


class Noise_generator(source):
    def __init__(self, **kwargs):
        name = kwargs.get("name", Noise_generator.__name__)
        super().__init__(n_max=0, block_class=Noise_generator.__name__, name=name)
        _apmplitude = kwargs.get("amplitude", 1.0)
        self.amplitude_input = NamedInput("amplitude", _apmplitude)
        self.data_obj = data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self, ts):
        _amp = self.amplitude_input.get()
        self.data_obj.set_data(_amp*np.random.randn())
        self.out_data_valid = True
        return False


class Random_Digital_generator(source):
    def __init__(self, **kwargs):
        name = kwargs.get("name", Random_Digital_generator.__name__)
        super().__init__(n_max=0, block_class=Random_Digital_generator.__name__, name=name)
        self.buff_size = kwargs.get("nbits", 8)
        self.data_obj = data.ARRAY_DATA(self.buff_size, data_type=data.DATA_TYPES.BOOL)

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self, ts):
        self.data_obj.set_data(np.random.binomial(n=1, p=0.5, size=(self.buff_size)))
        self.out_data_valid = True
        return False
