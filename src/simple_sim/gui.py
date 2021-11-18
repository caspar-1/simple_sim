from tkinter import *
import time
import threading


class GUI:
    def __init__(self,cntrls):
        self.close_requested=False
        self.root=None
        self.cntrls=cntrls
        self.is_running=False

    def __close_window(self):
        self.close_requested=True

    def stop(self):
        self.close_requested=True


    def periodic_call(self):
        if not self.close_requested:
            self.root.after(500, self.periodic_call)
        else:
            print("Destroying GUI at:", time.time())
            try: 
                self.root.quit()
                
            except:
                pass

    def tkinter_loop(self):
        self.is_running=True
        self.root=Tk()
        self.root.title("Simple SIM")
        self.root.protocol("WM_DELETE_WINDOW", self.__close_window)
        for c in self.cntrls:
            c.add_cntrl(self.root)

        self.root.after_idle(self.periodic_call)
        self.root.mainloop()
        self.is_running=False
       
        print("TKinter main loop finished")

    def start(self):
        threading.Thread(target=self.tkinter_loop).start()


# g=RadioGroup()
# g.add("A")
# g.add("B")
# g.add("C")
# s1=Slider(label="GAIN 1",min=-10,max=10,steps=20)
# s2=Slider(label="GAIN 2")
# c1=CheckBox()
# cntrls = [s1,s2,c1,g]
# g=GUI(cntrls)
# g.run()

# # ROP
# while g.is_running:
#     time.sleep(0.1)
#     print(s1.value)


# time.sleep(1)