import logging
from . import exceptions as excpt
from simplesimulator.blocks.data import ModelState, RunResult

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



class Output():
    def __init__(self,owner):
        self.owner = owner
        self.name=None
        self.data_valid=False

    def get(self):
        pass

    def update(self,data):
        self.out_data_obj=data


class Block():
    ID=0
    def __init__(self,n_max:int,block_class,name:str):
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
        self.output_data_connectors=[Output(self)]
        self.input_data_connectors=[]
        self.last_run_time=None


    def __del__(self):
        pass



    def add_input(self,blk:'Block'):
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
    
    def data_availible(self)->bool:
        data_ready=True
        for b in self.block_sources:
            data_ready&=b.out_data_valid
        return data_ready
    
    def initialise(self,model_obj):
        logger.debug("initialise {}".format(self.name))
        self.model_obj=model_obj
        pass

    def pre_run(self,ms:ModelState)->None:
        self.out_data_obj=self.data_obj

    def run(self,ms:ModelState)->RunResult:
        return RunResult()


    def post_run(self,ms:ModelState)->None:
        pass

    

    def get_output_data(self):
        return self.out_data_obj

    def get_out_data_type(self):
        raise NotImplementedError

    def end_simulation_clean_up(self):
        pass

    def get_input_connector(self,name:str=None):
        """### Returns the output data connector.
        if the block has multiple output connectors the the name has to be passed, other wise the name is not required.

        ### params:
         - name : name of the connector, optional
        """
        data_connector=None
        if len(self.output_data_connectors)==1:
            data_connector=self.output_data_connectors[0]
        else:
            if name==None:
                raise excpt.Block_exception_unnamed_output()
            else:
                for odc in self.output_data_connectors:
                    if odc.name==name:
                        data_connector=odc
                        break
        
        return data_connector
    
    
    
    
    
    
    
    
    def get_output_connector(self,name:str=None):
        """### Returns the output data connector.
        if the block has multiple output connectors the the name has to be passed, other wise the name is not required.

        ### params:
         - name : name of the connector, optional
        """
        data_connector=None
        if len(self.output_data_connectors)==1:
            data_connector=self.output_data_connectors[0]
        else:
            if name==None:
                raise excpt.Block_exception_unnamed_output()
            else:
                for odc in self.output_data_connectors:
                    if odc.name==name:
                        data_connector=odc
                        break
        
        return data_connector


    def __repr__(self):
        s="{}:{}".format(self.name,self.block_class)
        return s

