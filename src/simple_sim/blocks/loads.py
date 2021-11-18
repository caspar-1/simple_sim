import logging
import numpy as np
import json
from . import exceptions as excpt
from .block import Block
from .data import DATA_TYPES

logger=logging.getLogger(__name__)



class end_point(Block):
    
    def __init__(self,**kwargs):
        name=kwargs.get("name",end_point.__name__)
        super().__init__(n_max=1,block_class=end_point.__name__,name=name)

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass


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
        name=kwargs.get("name",File_out.__name__)
        super().__init__(n_max=1,block_class=File_out.__name__,name=name)
        self.filename=filename
        self.buff=[]
        self.max_buff_records=kwargs.get("max_records",10)
        self.max_buff_records_count=self.max_buff_records

    def initialise(self):
        logger.debug("initialise {}".format(self.name))
        pass

    def flush(self):
        with open (self.filename,"w+") as fh:
            for l in self.buff:
                js=json.dumps(l,cls=File_out.NumpyEncoder)
                fh.write(js)
    
    
    def run(self,ts):
        if self.data_availible():
            _data=self.block_sources[0].out_data_obj.data
            self.buff.append(_data)
            self.max_buff_records_count-=1
            if(self.max_buff_records_count==0):
                self.max_buff_records_count=self.max_buff_records
                self.flush()
        return False

    def end_simulation_clean_up(self):
        self.flush()