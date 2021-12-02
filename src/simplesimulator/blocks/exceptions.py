class Block_exception(Exception):
    message="Base Exception"
    def __init__(self,mess):            
        super().__init__(mess)
    pass


class Block_object_exists_allready(Block_exception):
    def __init__(self,obj=None):
        super().__init__("A block with this name allready exists <{}>".format(obj))


class Block_exception_invalid_class(Block_exception):
    message=""


class Block_exception_add_input_fail(Block_exception):
    message="failed to add an input to the block"

class Block_exception_invalid_data_type(Block_exception):
    pass

class Block_exception_invalid_input_data(Block_exception):
    pass

class Block_exception_unnamed_output(Block_exception):
    pass

class Block_exception_named_input_not_found(Block_exception):
    pass