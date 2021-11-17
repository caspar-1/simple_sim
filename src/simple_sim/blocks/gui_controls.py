import logging
import numpy as np
from . import exceptions as excpt
from .block import Block

from . import data as data

logger=logging.getLogger(__name__)


from tkinter import *
import time
import threading

class GUI_CNTRL():
    def __init__(self):
        self._value =None

    @property
    def value(self):
        return self._value.get()

    def callback(self):
        pass




class CheckBox(GUI_CNTRL):
    def __init__(self,**kwargs):
        super().__init__()
        self.label=kwargs.get("label","checkbox")

    def callback(self):
        print(self.value.get())
    
    def add_cntrl(self,root):
        self._value=IntVar()
        lf=LabelFrame(root,text=self.label,relief=RIDGE)
        lf.pack(anchor=W)
        _cntrl= Checkbutton(lf, text=self.label,variable=self.value, command=self.callback)
        _cntrl.pack(anchor=W)


class RadioGroup(GUI_CNTRL):

    class RadioButton():
        def __init__(self,label):
            super().__init__()
            self.label=label

        def add_cntrl(self,root,group,v):
            _cntrl= Radiobutton(root, text=self.label,variable=group._value,value=v, command=group.callback)
            _cntrl.pack(anchor=W)

    def __init__(self,**kwargs):
        self.label=kwargs.get("label","radio group")
        self.cntrls=[]
        self.idx=1

    def add(self,label):
        self.cntrls.append(RadioGroup.RadioButton(label=label))


    def add_cntrl(self,root):
        lf=LabelFrame(root,text=self.label,relief=RIDGE)
        lf.pack(anchor=W)
        self._value=IntVar()
        for r in self.cntrls:
            r.add_cntrl(lf,self,self.idx)
            self.idx+=1


class Slider(GUI_CNTRL):
    def __init__(self,**kwargs):
        super().__init__()
        self.min=kwargs.get("min",0.0)
        self.max=kwargs.get("max",1.0)
        self.steps=kwargs.get("steps",100)
        self.ticks=kwargs.get("ticks",(self.max-self.min)/2)
        self.label=kwargs.get("label",None)
        self.resolution=abs((self.max-self.min)/self.steps)

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

    def run(self,ts):
        self.data_obj.set_data(self.gui_obj.value)
        self.out_data_valid=True
        return False

