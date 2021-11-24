from datetime import datetime
import logging

logging.getLogger('matplotlib.font_manager').disabled = True
logger=logging.getLogger(__name__)

def decorator(method):
    def inner(ref,*args,**kwargs):
        start=datetime.now()
        result= method(ref,*args,**kwargs)
        stop=datetime.now()
        delta=stop-start
        logger.debug("""Function :"{}" ran in {} sec.""".format(method.__qualname__,delta.total_seconds()))
        return result
    return inner
