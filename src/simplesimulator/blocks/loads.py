import logging
import numpy as np
import json
from . import exceptions as excpt
from .block import Block
from .data import DATA_TYPES
from .data import ModelState ,RunResult

logger=logging.getLogger(__name__)



class end_point(Block):
    
    def __init__(self,name=None):
        class_name = self.__class__.__name__
        name=name if name else class_name
        super().__init__(n_max=1,block_class=class_name,name=name)

    def run(self,ms:ModelState)->RunResult:
        data=self.block_sources[0].out_data
        did_run=False
        if data is not None:
            did_run=True
            print("{}:{}:{}".format(self.name,ms.time,data))
        return RunResult(False,did_run)




class File_out(Block):
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    def __init__(self,filename,name=None,max_records=10):
        class_name = self.__class__.__name__
        name=name if name else class_name
        super().__init__(n_max=1,block_class=class_name,name=name)
        self.filename=filename
        self.buff=[]
        self.max_buff_records=max_records
        self.max_buff_records_count=self.max_buff_records

    def flush(self):
        with open (self.filename,"w+") as fh:
            for l in self.buff:
                js=json.dumps(l,cls=File_out.NumpyEncoder)
                fh.write(js)
    
    def run(self,ms:ModelState)->RunResult:
        did_run=False
        if self.data_availible():
            did_run=True
            _data=self.block_sources[0].out_data_obj.data
            self.buff.append(_data)
            self.max_buff_records_count-=1
            if(self.max_buff_records_count==0):
                self.max_buff_records_count=self.max_buff_records
                self.flush()
        return RunResult(False,did_run)

    def end_simulation_clean_up(self):
        self.flush()