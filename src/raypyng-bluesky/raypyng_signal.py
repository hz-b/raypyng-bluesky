from ophyd.signal import Signal
from ophyd.sim import NullStatus

# based on Sirepo Signal https://github.com/NSLS-II/sirepo-bluesky/blob/master/sirepo_bluesky/sirepo_ophyd.py

class RayPySignal(Signal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis = None
    
    def set_axis(self, axis):
        self.axis = axis
        
    def set(self, value):
        self.axis.cdata = str(value)
        return NullStatus()

    def put(self, *args, **kwargs):
        self.set(*args, **kwargs).wait() 
    
    def get(self): 
        return float(self.axis.cdata)

 
class RayPySignalRO(RayPySignal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def put(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))

    def set(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))
