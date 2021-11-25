from . import exceptions as excpt
from .block import Block
from ..gui_controls.gui_obj import GUI_OBJ
from . import data as data
import multiprocessing
import logging
logger=logging.getLogger(__name__)







class GUI_BLOCK(Block):
    def __init__(self,n_max,block_class,name):
        super().__init__(n_max,block_class,name)
        self.multiprocessing_shared_value=multiprocessing.Value('d',0.0)
        self.multiprocessing_shared_value.value=0.0

    def get_out_data_type(self):
        return self.data_obj.data_type

    @property
    def value(self):
        raise NotImplementedError

   
class Gui_RadioGroup(GUI_BLOCK):


        def __init__(self,**kwargs):
            name=kwargs.get("name",Gui_RadioGroup.__name__)
            super().__init__(n_max=0,block_class=Gui_RadioGroup.__name__,name=name)
            self.gui_obj=GUI_OBJ(Gui_RadioGroup.__name__,self.multiprocessing_shared_value,**kwargs)
            self.data_obj=data.STREAM_DATA()

        def add_button(self,label):
            self.gui_obj.sub_controls.append(label)

        def initialise(self):
            logger.debug("initialise {}".format(self.name))
            pass

        def run(self,ts):
            self.data_obj.set_data(self.multiprocessing_shared_value.value)
            self.out_data_valid=True
            return False
        

        @property
        def value(self):
            return int(self.multiprocessing_shared_value.value)

class Gui_checkbox(GUI_BLOCK):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Gui_slider.__name__)
        super().__init__(n_max=0,block_class=Gui_slider.__name__,name=name)
        self.gui_obj=GUI_OBJ(Gui_checkbox.__name__,self.multiprocessing_shared_value,**kwargs)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self,ts):
        self.data_obj.set_data(self.multiprocessing_shared_value.value)
        self.out_data_valid=True
        return False

    @property
    def value(self):
        return bool(self.multiprocessing_shared_value.value)



class Gui_slider(GUI_BLOCK):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Gui_slider.__name__)
        super().__init__(n_max=0,block_class=Gui_slider.__name__,name=name)
        self.gui_obj=GUI_OBJ(Gui_slider.__name__,self.multiprocessing_shared_value,**kwargs)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self,ts):
        self.data_obj.set_data(self.multiprocessing_shared_value.value)
        self.out_data_valid=True
        return False

    @property
    def value(self):
        return float(self.multiprocessing_shared_value.value)