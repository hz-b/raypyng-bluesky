from ophyd.signal import Signal
from ophyd.sim import NullStatus
import time
import queue   
import threading
import os

import numpy as np

from ophyd.status import Status


from raypyng.runner import RayUIRunner, RayUIAPI

class RayPySignal(Signal):
    raypyng = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis = None
    
    def set_axis(self, axis):
        self.axis = axis
        
    def set(self, value):
        self.axis.cdata = str(value)
        return NullStatus()

    def put(self, *args, **kwargs):
        pass

    def get(self): 
        return float(self.axis.cdata)

 
class RayPySignalRO(RayPySignal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def put(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))

    def set(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))



# class RaypyngDetector(Signal):
#     raypyng = True
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rml=None


#     def set_rml(self, rml):
#         self.rml = rml
        
#     def put(self, value, *, timestamp=None, force=False):
#         raise ReadOnlyError("The signal {} is readonly.".format(self.name))

#     def set(self, value, *, timestamp=None, force=False):
#         raise ReadOnlyError("The signal {} is readonly.".format(self.name))
    
#     def set_simulation_temporary_folder(self, path):
#         self.path = path
#         if not os.path.exists(self.path):
#             os.makedirs(self.path)

#     def check_if_simulation_is_done(self,result_queue):
#         # make sure tmp folder exists, if not create it
#         sim_done = os.path.join(self.path,"simulation_done.txt")
#         while not os.path.exists(os.path.join(self.path, self.name+"-RawRaysOutgoing.csv")):
#             #print('stuck', time.localtime())
#             time.sleep(.1)
#         result_queue.put(('done'))
#         return 
    
#     def trigger(self):
        
#         q = queue.Queue()
#         threads = threading.Thread(target=self.check_if_simulation_is_done(q), args=())
#         threads.daemon = True
#         threads.start()

#         d = Status(self)
#         d._finished()
#         return d
        
#     def get(self): 
#         rays = np.loadtxt(os.path.join(self.path, self.name+"-RawRaysOutgoing.csv"), skiprows=2)
#         intensity = rays.shape[0]
#         return intensity


# class RaypyngTriggerDetector(Signal):
#     raypyng = True
#     raypyngTriggerDet = True
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rml=None
#         self.exports_list = []

#     def set_rml(self, rml):
#         self.rml = rml
        
#     def put(self, value, *, timestamp=None, force=False):
#         raise ReadOnlyError("The signal {} is readonly.".format(self.name))

#     def set(self, value, *, timestamp=None, force=False):
#         raise ReadOnlyError("The signal {} is readonly.".format(self.name))
    
#     def set_simulation_temporary_folder(self, path):
#         self.path = path
#         if not os.path.exists(self.path):
#             os.makedirs(self.path)

#     def remove_done_simulation_file(self):
#         sim_done = os.path.join(self.path,"simulation_done.txt")
#         if os.path.exists(sim_done):
#             os.remove(sim_done)

#     def simulate(self,result_queue):
#         self.remove_done_simulation_file()
#         # make sure tmp folder exists, if not create it
#         if not os.path.exists(self.path):
#             os.makedirs(self.path)
        
#         r = RayUIRunner(ray_path=None, hide=True)
#         a = RayUIAPI(r)
#         self.rml.write(os.path.join(self.path,'tmp.rml'))
#         r.run()
#         a.load(os.path.join(self.path,'tmp.rml'))
#         a.trace(analyze=False)
#         for exp in self.exports_list:
#             aa=a.export(exp, "RawRaysOutgoing", self.path, '')
#         a.quit()
#         result_queue.put(('done'))
#         return 
    
#     def update_exports(self, exp):
#         self.exports_list= exp

#     def trigger(self):
#         q = queue.Queue()
#         threads = threading.Thread(target=self.simulate(q), args=())
#         threads.daemon = True
#         threads.start()

#         d = Status(self)
#         d._finished()
#         sim_done = os.path.join(self.path,"simulation_done.txt")
#         os.mknod(sim_done)
#         return d
        
#     def get(self): 
#         return 1