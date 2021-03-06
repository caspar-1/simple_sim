
import multiprocessing
import time
from simplesimulator.blocks import data as data
from .gui_obj import GUI_OBJ

import logging
logger=logging.getLogger(__name__)
import os
"""

**** IMPORTANT ****
all gui controls will run in a separate process
and must not be interacted with directly

the "Gui_process_funct" is acting as a namespace to
limit the import scope of Tk 

"""

DEFAULT_SLIDER_WIDTH=350
MIN_HEIGHT=200
MIN_WIDTH=DEFAULT_SLIDER_WIDTH



def Gui_process_funct(que:multiprocessing.Queue,cntrls:list[GUI_OBJ]):
    logger.debug("Gui_process_funct [PID={}]".format(os.getpid()))
    import tkinter as tk
    logger.debug("tkinter imported")
    
    
    class GUI_CNTRL():
        def __init__(self,sdv):
            self._value =None
            self.shared_data_value_obj=sdv
            self.label="?"

        def callback(self):
            v=self._value.get()
            self.set_shared_value(v)

        def set_shared_value(self,v):
            #logger.debug("Cntrl:{} = {}".format(self.label,v))
            if self.shared_data_value_obj:
                self.shared_data_value_obj.value=v


        @staticmethod
        def factory(obj:GUI_OBJ):
            obj_inst=None
            class_dict={"Gui_slider":tk_Slider,"Gui_checkbox":tk_CheckBox,"Gui_RadioGroup":tk_RadioGroup}
            obj_class=class_dict.get(obj.id,None)
            if obj_class:
                obj_inst=obj_class(obj.shared_data_value,obj.sub_controls,**obj.obj_data_dict)
            return obj_inst


    class tk_CheckBox(GUI_CNTRL):
        def __init__(self,sdv:multiprocessing.Value,sub_controls,**kwargs):
            super().__init__(sdv)
            self.label=kwargs.get("label","checkbox")
            self.initial=kwargs.get("initial",0)
            self.set_shared_value(self.initial)

        def add_cntrl(self,root):
            self._value=tk.IntVar()
            self._value.set(self.initial)
            lf=tk.LabelFrame(root,text=self.label,relief=tk.RIDGE)
            lf.pack(anchor=tk.W)
            _cntrl= tk.Checkbutton(lf, text=self.label,variable=self._value, command=self.callback)
            _cntrl.pack(anchor=tk.W)
            



    class tk_RadioGroup(GUI_CNTRL):

        class tk_RadioButton():
            def __init__(self,label):
                super().__init__()
                self.label=label

            def add_cntrl(self,root,group,idx):
                _cntrl= tk.Radiobutton(root, text=self.label,variable=group._value,value=idx, command=group.callback)
                _cntrl.pack(anchor=tk.W)

        def __init__(self,sdv:multiprocessing.Value,sub_controls,**kwargs):
            super().__init__(sdv)
            self.label=kwargs.get("label","radio group")
            self.initial=kwargs.get("initial",1)
            self.cntrls=[]
            self.idx=1
            self.set_shared_value(self.initial)
            for s in sub_controls:
                self.cntrls.append(tk_RadioGroup.tk_RadioButton(label=s))

        def add_cntrl(self,root):
            lf=tk.LabelFrame(root,text=self.label,relief=tk.RIDGE)
            lf.pack(anchor=tk.W)
            self._value=tk.IntVar()

            for r in self.cntrls:
                r.add_cntrl(lf,self,self.idx)
                self.idx+=1
            
            self._value.set(self.initial)




    class tk_Slider(GUI_CNTRL):
        def __init__(self,sdv:multiprocessing.Value,sub_controls,**kwargs):
            super().__init__(sdv)
            self.label=kwargs.get("label","slider")
            self.min=kwargs.get("min",0.0)
            self.max=kwargs.get("max",1.0)
            self.initial=kwargs.get("initial",self.min)
            self.steps=kwargs.get("steps",100)
            self.ticks=kwargs.get("ticks",(self.max-self.min)/2)
            
            self.resolution=abs((self.max-self.min)/self.steps)
            self.set_shared_value(self.initial)
            

        def callback(self,v):
            super().callback()

        def add_cntrl(self,root):
            self._value=tk.DoubleVar()
            self._value.set(self.initial)
            lf=tk.LabelFrame(root,text=self.label,relief=tk.RIDGE)
            lf.pack(anchor=tk.W)
            _cntrl= tk.Scale(
                lf,
                from_=self.min,
                to=self.max,
                tickinterval=self.ticks,
                variable=self._value,
                length=DEFAULT_SLIDER_WIDTH,
                orient=tk.HORIZONTAL,
                resolution=self.resolution,
                command=self.callback
                )
            _cntrl.pack(anchor=tk.W)
    

    class TK_GUI_PROCESS:

        def __init__(self,que:multiprocessing.Queue):
            self.close_requested=False
            self.que=que

        def __close_window(self):
            self.close_requested=True

        def periodic_call(self):
            if self.close_requested==False:
                self.root.after(500, self.periodic_call)
            else:
                logger.debug("Destroying GUI at:", time.time())
                try:
                    self.root.quit()

                except:
                    pass

        def process_function(self,cntrl_obj_list:list[GUI_OBJ]):
            logging.debug("process_function")
            self.root = tk.Tk()
            self.root.minsize(MIN_HEIGHT, MIN_WIDTH)
            self.root.title("Simple Simulator Controls  [PID={}]".format(os.getpid()))
            self.root.protocol("WM_DELETE_WINDOW", self.__close_window)
            logging.debug("initialise controls..")
            for o in cntrl_obj_list:
                logger.debug("added:".format(o.id))
                cntrl_inst=GUI_CNTRL.factory(o)
                if cntrl_inst:
                    cntrl_inst.add_cntrl(self.root)
                

            self.root.after_idle(self.periodic_call)
            self.que.put("running")
            logging.debug("starting tk main loop...")
            self.root.mainloop()
    

            logger.debug("Simple Simulator Controls window finished [PID={}]".format(os.getpid()))


    p=TK_GUI_PROCESS(que)
    p.process_function(cntrls)


