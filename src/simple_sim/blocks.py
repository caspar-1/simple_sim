import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
from simple_sim.custom_exceptions import * 
import simple_sim.function_timer as function_timer
import logging
import json

logging.getLogger('matplotlib.font_manager').disabled = True
logger=logging.getLogger(__name__)


class DATA_TYPES(Enum):
    STREAM_DATA=1
    ARRAY_DATA=2
        
class DATA():
    def __init__(self,sz,data_type):
        self.sz=sz
        self.data_type=data_type

    def check_type(self,expected):
        return (self.data_type==expected)

class VALUE_DATA(DATA):
    def __init__(self):
        super().__init__(1,DATA_TYPES.STREAM_DATA)
        self.data=None

class ARRAY_DATA(DATA):
    def __init__(self,buffer_sz,data_type="float"):
        super().__init__(buffer_sz,DATA_TYPES.ARRAY_DATA)
        _type_dict={"float":np.single,"complex":np.csingle}
        if data_type not in _type_dict:
            raise Block_exception_invalid_data_type
        self.data=np.zeros(self.buffer_sz,dtype=_type_dict[data_type])





class Block():
    ID=0
    def __init__(self,n_max,block_class,name=None):
        self.block_sources=[]
        self.block_loads=[]
        self.block_output=None
        self.data=None
        self.out_data=None
        self.n_inputs=0
        self.max_inputs=n_max
        self.block_class=block_class
        self.name="{}_{}".format(block_class,Block.ID) if name is None else name
        Block.ID+=1
        logger.debug("Creating Block :{}".format(self))


    def __del__(self):
        pass

    def add_input(self,blk,**kwargs):
        if not isinstance(blk,Block):
            raise Block_exception_invalid_class
        if self.n_inputs==self.max_inputs:
            raise Block_exception_add_input_fail
        self.block_sources.append(blk)
        blk.block_loads.append(self)
        self.n_inputs+=1
    
    
    def initialise(self):
        pass
    
    def run(self)->bool:
        return False

    def update_out_data(self):
        self.out_data=self.data

    def get_data(self):
        return self.out_data

    def get_out_data_type(self):
        raise NotImplementedError

    def end_simulation_clean_up(self):
        pass

    def __repr__(self):
        s="{}:{}:{}".format(self.name,self.block_class,self.out_data)
        return s



class source(Block):
    def __init__(self,n_max,block_class):
        super().__init__(n_max,block_class)


class end_point(Block):
    
    def __init__(self):
        super().__init__(n_max=1,block_class=end_point.__name__)

    def run(self,ts):
        data=self.block_sources[0].out_data
        if data is not None:
            print("{}:{}:{}".format(self.name,ts,data))
        return False



class File_out(Block):
    

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)



    def __init__(self,filename,**kwargs):
        super().__init__(n_max=1,block_class=File_out.__name__)
        self.filename=filename
        self.buff=[]
        self.max_buff_records=kwargs.get("max_records",10)
        self.max_buff_records_count=self.max_buff_records

    def flush(self):
        with open (self.filename,"w+") as fh:
            for l in self.buff:
                js=json.dumps(l,cls=File_out.NumpyEncoder)
                fh.write(js)
    
    
    def run(self,ts):
        data=self.block_sources[0].out_data
        if data is not None:
            self.buff.append(data)
            self.max_buff_records_count-=1
            if(self.max_buff_records_count==0):
                self.max_buff_records_count=self.max_buff_records
                self.flush()
        return False

    def end_simulation_clean_up(self):
        self.flush()

class sine_generator(source):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=0,block_class=sine_generator.__name__)
        self.freq=kwargs.get("freq",1)
        self.apmplitude=kwargs.get("amplitude",1.0)
        self.phase_rads=kwargs.get("phase",0.0)

    def run(self,ts):
        self.data= self.apmplitude*np.sin(2*np.pi*self.freq*ts+self.phase_rads)
        return False

    def get_out_data_type(self):
        return DATA_TYPES.STREAM_DATA


class Noise_generator(source):
    def __init__(self,**kwargs):
        super().__init__(n_max=0,block_class=Noise_generator.__name__)
        self.apmplitude=kwargs.get("amplitude",1.0)

    def run(self,ts):
        self.data= self.apmplitude*np.random.randn()
        return False

    def get_out_data_type(self):
        return DATA_TYPES.STREAM_DATA




class Sum(Block):

    def __init__(self,**kwargs):
        super().__init__(n_max=-1,block_class=Sum.__name__)
        

    def run(self,ts):
        r=0.0
        for i in self.block_sources:
            if i.out_data is None:
                r=None
                break
            r=r+i.out_data

        self.data= r
        return False

class Sub(Block):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=2,block_class=Sub.__name__)

    def run(self,ts):
        r=0.0
        a=self.block_sources[0]
        b=self.block_sources[1]
        if a and b:
            r=a.out_data-b.out_data
        else:
            r=None
        self.data= r
        return False

class Multiplier(Block):
 
    def __init__(self,**kwargs):
        super().__init__(n_max=-1,block_class=Multiplier.__name__)

    def run(self,ts):
        r=1.0
        for i in self.block_sources:
            if i.out_data is None:
                r=None
                break
            r=r*i.out_data

        self.data= r
        return False

    def get_out_data_type(self):
        pass

class ABS(Block):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=1,block_class=ABS.__name__)

    def run(self,ts):
        _data=self.block_sources[0].out_data
        if _data is not None:
            r=np.abs(_data)                      
        else:
            r=None
        self.data= r
        return False




class Buffer(Block):
    
    def __init__(self,**kwargs):
        self.buffer_sz=kwargs.get("sz",1)
        super().__init__(n_max=1,block_class=Buffer.__name__)
        self.data=np.zeros(self.buffer_sz)
        self.data_count=0
        self.data_ready=False

    def run(self,ts):
        data=self.block_sources[0].out_data
        if data:
            self.data[self.data_count]=data
            self.data_count+=1
        return False


    def update_out_data(self):
        if self.data_count==self.buffer_sz:
            self.out_data=self.data
            self.data_count=0
        else:
            self.out_data=None


class FFT(Block):
    
    def __init__(self,**kwargs):
        super().__init__(n_max=1,block_class=Buffer.__name__)

    
    def run(self,ts):    
        
        @function_timer.decorator
        def __run(data):
            return np.fft.rfft(data)

        data=self.block_sources[0].out_data
        if data is None:
            self.data=None
        else:
            self.data=__run(data)
            pass
        
        return False




    def update_out_data(self):
        self.out_data=self.data



class Display(Block):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)



class Plot(Display):

    def __init__(self,**kwargs):
        super().__init__(n_max=1,block_class=Plot.__name__)
        self.ax=kwargs.get("ax",None)
        self.kwargs=kwargs
        self.line=None
        
        
    def initialise(self):
        if self.ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
        else:
            self.fig = self.ax.figure
        self.ax.set_title(self.kwargs.get("title","Title"))


    def run(self,ts):
        @function_timer.decorator
        def __run(data):
            try:
                if self.line is None:
                    x=np.linspace(0,0.5,data.shape[0])
                    self.line, = self.ax.plot(x,data, 'r-')
                else:
                    self.line.set_ydata(data)
            except:
                raise Model_runtime_exception

        data=self.block_sources[0].out_data
        if data is not None:
            __run(data)
            return True
        return False