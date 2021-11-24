
import numpy as np
from . import exceptions as excpt
from .block import Block
import multiprocessing
from . import data as data

import logging
logger=logging.getLogger(__name__)


from tkinter import *


class GUI_CNTRL():
    def __init__(self):
        self._value =None
        self.multiprocessing_shared_value=multiprocessing.Value('d',0.0)

    def add_cntrl(self,n):
        self.shared=n

    @property
    def value(self):
        return self.multiprocessing_shared_value.value

    def callback(self):
        v=self._value.get()
        self.shared.value=v


class CheckBox(GUI_CNTRL):
    def __init__(self,**kwargs):
        super().__init__()
        self.label=kwargs.get("label","checkbox")
        self.multiprocessing_shared_value.value=0

    def add_cntrl(self,root):
        self._value=IntVar()
        lf=LabelFrame(root,text=self.label,relief=RIDGE)
        lf.pack(anchor=W)
        _cntrl= Checkbutton(lf, text=self.label,variable=self._value, command=self.callback)
        _cntrl.pack(anchor=W)
        super().add_cntrl(self.multiprocessing_shared_value)

    @property
    def value(self):
        return int(self.multiprocessing_shared_value.value)


class RadioGroup(GUI_CNTRL):

    class RadioButton():
        def __init__(self,label):
            super().__init__()
            self.label=label

        def add_cntrl(self,root,group,v):
            _cntrl= Radiobutton(root, text=self.label,variable=group._value,value=v, command=group.callback)
            _cntrl.pack(anchor=W)

    def __init__(self,**kwargs):
        super().__init__()
        self.label=kwargs.get("label","radio group")
        self.cntrls=[]
        self.idx=1
        self.multiprocessing_shared_value.value=0

    def add(self,label):
        self.cntrls.append(RadioGroup.RadioButton(label=label))


    def add_cntrl(self,root):
        lf=LabelFrame(root,text=self.label,relief=RIDGE)
        lf.pack(anchor=W)
        self._value=IntVar()
        for r in self.cntrls:
            r.add_cntrl(lf,self,self.idx)
            self.idx+=1
        super().add_cntrl(self.multiprocessing_shared_value)

    @property
    def value(self):
        return int(self.multiprocessing_shared_value.value)


class Slider(GUI_CNTRL):
    def __init__(self,**kwargs):
        super().__init__()
        self.min=kwargs.get("min",0.0)
        self.max=kwargs.get("max",1.0)
        self.steps=kwargs.get("steps",100)
        self.ticks=kwargs.get("ticks",(self.max-self.min)/2)
        self.label=kwargs.get("label",None)
        self.resolution=abs((self.max-self.min)/self.steps)
        self.multiprocessing_shared_value.value=self.min

    def callback(self,v):
        super().callback()

    def add_cntrl(self,root):
        self._value=DoubleVar()
        lf=LabelFrame(root,text=self.label,relief=RIDGE)
        lf.pack(anchor=W)
        _cntrl= Scale(
            lf,
            from_=self.min,
            to=self.max,
            tickinterval=self.ticks,
            variable=self._value,
            length=300,
            orient=HORIZONTAL,
            resolution=self.resolution,
            command=self.callback
            )
        _cntrl.pack(anchor=W)
        super().add_cntrl(self.multiprocessing_shared_value)



class GUI_BLOCK(Block):
    def __init__(self,n_max,block_class,name):
        super().__init__(n_max,block_class,name)

    def get_out_data_type(self):
        return self.data_obj.data_type


class Gui_slider(GUI_BLOCK):
    def __init__(self,**kwargs):
        name=kwargs.get("name",Gui_slider.__name__)
        super().__init__(n_max=0,block_class=Gui_slider.__name__,name=name)
        self.min=kwargs.get("min",1)
        self.max=kwargs.get("max",1.0)
        self.steps=kwargs.get("steps",100)
        self.ticks=kwargs.get("ticks",(self.max-self.min)/2)
        self.gui_obj=Slider(label=name,min=self.min,max=self.max,steps=self.steps,tick=self.ticks)
        self.data_obj=data.STREAM_DATA()

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def run(self,ts):
        self.data_obj.set_data(self.gui_obj.value)
        self.out_data_valid=True
        return False

