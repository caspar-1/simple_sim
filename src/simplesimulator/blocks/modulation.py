import logging
import numpy as np
from . import exceptions as excpt
from .block import Block
from . import data as data

logger=logging.getLogger(__name__)


class MODULATION(Block):
    def __init__(self,n_max,block_class,name):
        super().__init__(n_max,block_class,name)

class OFDM(MODULATION):

    def __init__(self,**kwargs):
        name=kwargs.get("name",OFDM.__name__)
        super().__init__(n_max=1,block_class=OFDM.__name__,name=name)
        self.n_sub_carriers=kwargs.get("k",64)
        self.n_pilot_carriers=kwargs.get("p",16)
        self.bits_symbol=kwargs.get("mu",4)
        self.pilotValue=3+3j
        self.data_obj=None
  
    def initialise(self,model_obj):
        super().initialise(model_obj)
        logger.debug("initialise {}".format(self.name))
        self.allCarriers=np.arange(self.n_sub_carriers)
        self.pilotCarriers=self.allCarriers[::self.n_sub_carriers//self.n_pilot_carriers]
        self.pilotCarriers=np.hstack([self.pilotCarriers,np.array([self.allCarriers[-1]])])
        self.dataCarriers=np.delete(self.allCarriers,self.pilotCarriers)
        self.payloadBits_per_OFDM = len(self.dataCarriers)*self.mu

    def run(self,ts):
        if self.data_availible():  
            data_in=self.block_sources[0].out_data_obj.data
            if self.window is None:
                self.window=self.window_fnct(len(data_in))

            data_out=np.zeros_like(data_in)
            if(self.data_obj is None):
                self.data_obj=data.ARRAY_DATA.from_data(data_out)
            else:
                self.data_obj.data=data_out

            self.out_data_valid=True
        else:
            self.out_data_valid=False
        
        return False


