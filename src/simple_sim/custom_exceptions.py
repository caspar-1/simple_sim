class Model_runtime_exception(Exception):
    def __init__(self,msg=None):
        self.message = msg
        

    def __str__(self):
        if self.message:
            return f'{self.message}'
        else:
            return "Model runtime exception raised"
