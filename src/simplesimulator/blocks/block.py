import logging
from simplesimulator.blocks import exceptions as excpt
from simplesimulator.blocks.data import ModelState, RunResult

logger=logging.getLogger(__name__)

"""
Blocks may have:
0..n inputs
0..n ouputs

where a block has more than one output it needs to have a unique id
block inputs can be unnamed in which case they are all treated identically, or they may be name and used 'uniquely'

if a block has inputs they should be connected
block outputs do not have to be used

              -----------------                              -----------------                              -----------------
             |                 |                            |                 |OUTPUT|---------------|INPUT|                 | 
             |    BLOCK        |                            |    BLOCK        |                            |   BLOCK         | 
             |                 |OUTPUT|---------------|INPUT|                 |                            |                 |
             |                 |                            |                 |                            |                 |
             |                 |OUTPUT|---------------|INPUT|                 |                            |                 |
             |                 |                            |                 |                            |                 |
              -----------------                              -----------------                              -----------------
"""


class IO():
    def __init__(self,owner,name):
        self.owner = owner
        self.name=name

    def is_connected(self):
        raise NotImplementedError

    def __repr__(self):
        s="{}:{}:{}".format(self.name,self.__class__.__name__,self.owner)
        return s

class Output(IO):
    def __init__(self,owner,name):
        super().__init__(owner,name)
        self.data_valid=False
        self.working_data=None
        self.out_data_obj=None
        self.loads=[]


    def data(self):
        self.out_data_obj


    def data(self,v,valid=False):
        self.working_data=v
        self.data_valid=valid

    def update(self):
        self.out_data_obj=self.working_data

    def is_connected(self):
        return len(self.loads)!=0

class Input(IO):
    def __init__(self,owner:'Block' ,name=None, default=None):
        super().__init__(owner,name)
        self.value = default
        self.input_source = None

    def connect(self,source:Output):
        if not isinstance(source,Output):
            raise excpt.Block_exception_invalid_class
        if self.input_source is None:
            self.input_source=source
        else:
            raise excpt.Block_exception_add_input_fail

    def get(self):
        if self.input_source is not None:
            if self.input_source.out_data_obj:
                self.value = self.input_source.out_data_obj.data

        return self.value

    def is_connected(self):
        return isinstance(self.input_source,Output)



class Abstract_Block():
    ID=0
    def __init__(self,n_max:int,block_class,name:str):
        self.n_inputs=0
        self.max_inputs=n_max
        self.block_class=block_class
        self.name="{}_{}".format(name,Abstract_Block.ID) 
        Abstract_Block.ID+=1
        logger.debug("Creating Block - {}:{}".format(self.name,self.block_class))
        self.model_obj=None
        self.output_data_connectors:list[Output]=[]
        self.input_data_connectors:list[Input]=[]
        self.named_input_data_connectors:list[Input]=[]
        self.last_run_time=None


    def __del__(self):
        pass

    def add_input(self):
        if self.n_inputs==self.max_inputs:
            raise excpt.Block_exception_add_input_fail
        i=Input("unnamed_{}".format(self.n_inputs))
        self.input_data_connectors.append(i)
        self.n_inputs+=1
        return i

    def add_named_input(self,name,default_value=None):
        i=Input(name)
        self.named_input_data_connectors.append(i)
        return i

    def connect_input(self,blk:Output):
        i=self.add_input()
        i.connect(blk)
        blk.loads.append(i)
       

    def connect_named_input(self,name,blk:Output):
        _connector=self.get_input_connector_by_name(name)
        if _connector:
            _connector.connect(blk)
            blk.loads.append(_connector)
        else:
            raise excpt.Block_exception_named_input_not_found()
        
    def add_output(self,name):
        _o= self.get_output_connector_by_name(name)
        if _o:
            raise excpt.Block_object_exists_allready(_o)
        o=Output(self,name)
        self.output_data_connectors.append(o)
        return o
    
    
    
    
    
    def check_is_ok(self)->bool:
        """
        check all inputs are connected

        returns:
        False : not OK
        True :  OK
        """
        ok=True
        for i in self.input_data_connectors:
            ok &= i.is_connected()

        return ok
    
    def data_availible(self)->bool:
        data_ready=True
        for b in self.input_data_connectors:
            data_ready&=b.out_data_valid
        return data_ready
    
    def initialise(self,model_obj):
        logger.debug("initialise {}".format(self.name))
        self.model_obj=model_obj
        pass

    def pre_run(self,ms:ModelState)->None:
        #we need to copy the object since we want evething to have fixed out data when the model runs
        if self.data_obj:
            self.out_data_obj=self.data_obj.obj_copy()
        else:
            self.out_data_obj=None
        pass

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

    def get_input_connector_by_name(self,name:str):
        """### Returns the input data connector.
      
        ### params:
         - name : name of the connector, optional
        """
       
        if name==None:
            raise excpt.Block_exception_unnamed_output()
        else:
            for idc in self.named_input_data_connectors:
                if idc.name==name:
                    data_connector=idc
                    break
        return data_connector


    def get_output_connector_by_name(self,name:str=None):
        data_connector=None
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
            data_connector=self.get_output_connector_by_name(name)
        return data_connector


    def __repr__(self):
        s="{}:{}".format(self.name,self.block_class)
        return s






if __name__=="__main__":

    class Test_named(Abstract_Block):

        def __init__(self, name:str=None):
            name = name if name else self.__class__.__name__
            super().__init__(n_max=0,block_class=self.__class__.__name__,name=name)

            self.A_input = self.add_named_input("A", 11)
            self.B_input = self.add_named_input("B", 22)
            self.C_input = self.add_named_input("C", 33)

            self.add_output("OUT_A")
            self.add_output("OUT_B")




    b=Test_named("test")
    print(b)