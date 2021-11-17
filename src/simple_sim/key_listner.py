# pip3 install pynput

from pynput.keyboard import Key, Listener
import threading, queue
import time
import logging
logging.getLogger('matplotlib.font_manager').disabled = True
logger=logging.getLogger(__name__)





class key_listner(threading.Thread):
    def __init__(self,**kwargs):
        super().__init__()
        self.que=kwargs.get("que",None)
        self.callback=kwargs.get("callback",None)
        self.quit_key=kwargs.get("quit_key",Key.esc)
        self.callback_dict=kwargs.get("callback_dict",None)
        self.listener=None
        self.running=False

    def run(self):
        logger.debug("start key listner")
        def show(key):
           
            pressed_key = str(key).replace("'", "")
            if self.que:
                self.que.put(pressed_key)
            if self.callback:

                self.callback(key=pressed_key)
            if self.callback_dict:
                callback_fn=self.callback_dict.get(pressed_key,None)
                if callback_fn:
                    callback_fn()
            if key == self.quit_key:
                # Stop listener
                return False
            

        self.listener=Listener(on_press=show)
        self.listener.start()
        self.listener.join()


        

    def get_key(self):
        key=self.que.get(False)
        return key

    def stop(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener.join()
            logger.debug("key listner stopped")






if __name__=="__main__":

    stop=False


    def callback_general(**kwargs):
        k=kwargs.get("key","")
        print(k)



    def callback_A(**kwargs):
        print(callback_A.__name__)

    def callback_B(**kwargs):
        print(callback_B.__name__)   
        




    # Listener
    q=queue.Queue()
    k=key_listner(callback=callback_general,callback_dict={"A":callback_A,"B":callback_B})
    k.start()

    for _ in range(10000000):
        time.sleep(0.1)
        if not k.is_alive():
            break

    k.join()



