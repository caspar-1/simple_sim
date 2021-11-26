

import multiprocessing


class GUI_OBJ():
    def __init__(self, id: str, sdv: multiprocessing.Value, sub_controls=[], **kwargs):
        self.id = id
        self.shared_data_value = sdv
        self.obj_data_dict = kwargs
        self.sub_controls = sub_controls
