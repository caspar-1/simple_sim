import numpy as np
from enum import Enum
from . import exceptions as excpt

class DATA_FORMATS(Enum):
    STREAM_DATA=1
    ARRAY_DATA=2


class DATA_TYPES(Enum):
    BOOL=0
    UINT_8=1
    INT_8=2
    UINT_16=3
    INT_16=4
    UINT_32=5
    INT_32=6
    FLOAT=7
    DOUBLE=8
    COMPLEX=9


__numpy_mapping_type_dict={
    DATA_TYPES.BOOL:np.byte,
    DATA_TYPES.UINT_8:np.byte,
    DATA_TYPES.INT_8:np.ubyte,
    DATA_TYPES.UINT_16:np.uint16,
    DATA_TYPES.INT_16:np.int16,
    DATA_TYPES.UINT_32:np.uint32,
    DATA_TYPES.INT_32:np.int32,
    DATA_TYPES.FLOAT:np.float64,
    DATA_TYPES.DOUBLE:np.double,
    DATA_TYPES.COMPLEX:np.complex128}

__numpy_mapping_type_dict_reverse={v.__name__:k for k,v in __numpy_mapping_type_dict.items()}


def get_numpy_mapping_type(data_type:DATA_TYPES)->np.dtype:
    if data_type not in __numpy_mapping_type_dict:
            raise excpt.Block_exception_invalid_data_type
    return __numpy_mapping_type_dict[data_type]

def get_mapping_type(np_type:np.dtype)->DATA_TYPES:
    if str(np_type.name) not in __numpy_mapping_type_dict_reverse:
            raise excpt.Block_exception_invalid_data_type
    return __numpy_mapping_type_dict_reverse[str(np_type.name)]




        
class DATA():
    def __init__(self,sz,data_format:DATA_FORMATS,data_type:DATA_TYPES)->None:
        self.sz=sz
        self.data_type=data_type
        self.data_format=data_format
        self.data=np.zeros(self.sz,dtype=get_numpy_mapping_type(data_type))
        
    def check_type(self,expected:DATA_TYPES)->bool:
        return (self.data_type==expected)

    def is_compatible(self,other)->bool:
        return ((self.data_type==other.data_type)and(self.data.shape==other.data.shape))

    def set_data(self,data)->None:
        self.data=data

    def get_data(self):
        return self.data


 


class STREAM_DATA(DATA):
    def __init__(self,data_type:DATA_TYPES=DATA_TYPES.FLOAT)->None:
        super().__init__(1,DATA_FORMATS.STREAM_DATA,data_type)

class ARRAY_DATA(DATA):
    def __init__(self,buffer_sz:int,data_type:DATA_TYPES=DATA_TYPES.FLOAT)->None:
        super().__init__(buffer_sz,DATA_FORMATS.ARRAY_DATA,data_type)

    @staticmethod
    def from_data(data):
        _obj=None
        if isinstance(data, np.ndarray):
            _sz=data.shape[0]
            _type=get_mapping_type(data.dtype)
            _obj=ARRAY_DATA(_sz,_type)
            _obj.data=data
        return _obj
        



class ModelState:
    time:float=0.0
    delta:float=0.0

class RunResult:
    def __init__(self,update_display=False,did_run=False):
        self.update_display=update_display
        self.did_run=did_run
