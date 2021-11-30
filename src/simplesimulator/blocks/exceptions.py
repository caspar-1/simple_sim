class Block_exception(Exception):
    message="Base Exception"
    def __init__(self):            
       
        super().__init__(self.__class__.message)
    pass

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