import logging
from . import exceptions as excpt


logger=logging.getLogger(__name__)



class Input():
    def __init__(self, name, default):
        self.source = None

    def connect(self,source):
        if self.source is None:
            self.source=source
        else:
            raise excpt.Block_exception_add_input_fail

    def get(self):
        if self.source is not None:
            if self.source.out_data_obj:
                self.value = self.source.out_data_obj.data

        return self.value





class NamedInput():
    def __init__(self, name, default):
        self.name = name
        self.value = default
        self.source = None

    def connect(self,source):
        if self.source is None:
            self.source=source
        else:
            raise excpt.Block_exception_add_input_fail

    def get(self):

        if self.source is not None:
            if self.source.out_data_obj:
                self.value = self.source.out_data_obj.data

        return self.value










class Block():
    ID=0
    def __init__(self,n_max,block_class,name):
        self.block_sources=[]
        self.block_loads=[]
        self.block_output=None
        self.data_obj=None
        self.out_data_obj=None
        self.out_data_valid=False
        self.n_inputs=0
        self.max_inputs=n_max
        self.block_class=block_class
        self.name="{}_{}".format(name,Block.ID) 
        Block.ID+=1
        logger.debug("Creating Block - {}:{}".format(self.name,self.block_class))
        self.model_obj=None


    def __del__(self):
        pass

    def add_input(self,blk,**kwargs):
        if not isinstance(blk,Block):
            raise excpt.Block_exception_invalid_class
        if self.n_inputs==self.max_inputs:
            raise excpt.Block_exception_add_input_fail
        self.block_sources.append(blk)
        blk.block_loads.append(self)
        self.n_inputs+=1
    
    def check_is_ok(self)->bool:
        """
        returns:
        False : not OK
        True :  OK
        """
        error=False
        error|=(self.n_inputs==0 and self.max_inputs!=0)

        return not error
    
    def data_availible(self):
        data_ready=True
        for b in self.block_sources:
            data_ready&=b.out_data_valid
        return data_ready
    
    def initialise(self,model_obj):
        logger.debug("initialise {}".format(self.name))
        self.model_obj=model_obj
        pass
    
    def run(self)->bool:
        return False

    def update_out_data(self):
        self.out_data_obj=self.data_obj

    def get_data(self):
        return self.out_data_obj

    def get_out_data_type(self):
        raise NotImplementedError

    def end_simulation_clean_up(self):
        pass

    def __repr__(self):
        s="{}:{}".format(self.name,self.block_class)
        return s

