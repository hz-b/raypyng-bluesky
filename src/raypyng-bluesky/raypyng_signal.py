from ophyd.signal import Signal
from ophyd.sim import NullStatus

# based on Sirepo Signal https://github.com/NSLS-II/sirepo-bluesky/blob/master/sirepo_bluesky/sirepo_ophyd.py

class RayPySignal(Signal):
    def __init__(self, obj, axis, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj
        if axis == 'x':
            self.obj=self.obj.translationXerror
        elif axis == 'y':
            self.obj=self.obj.translationYerror
        elif axis == 'z':
            self.obj=self.obj.translationZerror
        elif axis == 'energy':
            self.obj = self.obj.photonEnergy
        elif axis == 'nrays':
            self.obj = self.obj.numberRays
        
    def set(self, value):
        self.obj.cdata = str(value)
        return NullStatus()

    def put(self, *args, **kwargs):
        self.set(*args, **kwargs).wait() 
    
    def get(self): 
        return float(self.obj.cdata)

 
class RayPySignalRO(Signal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def put(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))

    def set(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))
