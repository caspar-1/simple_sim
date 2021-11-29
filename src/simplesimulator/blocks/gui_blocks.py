from . import exceptions as excpt
from .block import Block
from ..gui_controls.gui_obj import GUI_OBJ
from . import data as data
import multiprocessing
import logging
logger=logging.getLogger(__name__)





def cast_bool(v):return bool(v)
def cast_int(v):return int(v)
def cast_float(v):return float(v)

class GUI_BLOCK(Block):
    def __init__(self,n_max,block_class,defined_name,**kwargs):
        super().__init__(n_max,block_class,defined_name)
        self.multiprocessing_shared_value=None
        self.gui_obj=None
        self.data_obj=None
        self.kwargs=kwargs
        self.sub_controls=[]
        
    def get_out_data_type(self):
        return self.data_obj.data_type

    def get_shared_value(self,cast_fnct=cast_float):
        value=0
        if self.multiprocessing_shared_value is not None:
            value=cast_fnct(self.multiprocessing_shared_value.value)
        return value

    def get_gui_obj(self,v):
        self.multiprocessing_shared_value=v
        gui_obj=GUI_OBJ(self.__class__.__name__,v,self.sub_controls,**self.kwargs)
        return gui_obj



    @property
    def value(self):
        raise NotImplementedError

   
class Gui_RadioGroup(GUI_BLOCK):


        def __init__(self,**kwargs):
            name=kwargs.get("name",Gui_RadioGroup.__name__)
            super().__init__(n_max=0,block_class=Gui_RadioGroup.__name__,defined_name=name,**kwargs)
            self.data_obj=data.STREAM_DATA()

        def add_button(self,label):
            self.sub_controls.append(label)

        def run(self,ts):
            self.data_obj.set_data(self.value)
            self.out_data_valid=True
            return False
        

        @property
        def value(self):
            return self.get_shared_value(cast_int)

class Gui_checkbox(GUI_BLOCK):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Gui_slider.__name__)
        super().__init__(n_max=0,block_class=Gui_slider.__name__,defined_name=name,**kwargs)
        self.data_obj=data.STREAM_DATA()

    def run(self,ts):
        self.data_obj.set_data(self.value)
        self.out_data_valid=True
        return False

    @property
    def value(self):
        return self.get_shared_value(cast_bool)



class Gui_slider(GUI_BLOCK):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Gui_slider.__name__)
        super().__init__(n_max=0,block_class=Gui_slider.__name__,defined_name=name,**kwargs)
        self.data_obj=data.STREAM_DATA()


    def run(self,ts):
        self.data_obj.set_data(self.value)
        self.out_data_valid=True
        return False

    @property
    def value(self):
        return self.get_shared_value(cast_float)