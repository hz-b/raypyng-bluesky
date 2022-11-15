from ophyd.device import Device
from ophyd import Component as Cpt
from ophyd.sim import NullStatus


from raypyng_signal import RayPySignalRO, RayPySignal
from positioners import PVPositionerDone


class RaypyngAxis(PVPositionerDone):

    raypyng   = True
    setpoint  = Cpt(RayPySignal, kind='normal' )
    readback  = Cpt(RayPySignalRO, kind='normal')
            
    atol = 0.0001  # tolerance before we set done to be 1 (in um) we should check what this should be!

    
    def done_comparator(self, readback, setpoint):
        return setpoint-self.atol < readback < setpoint+self.atol
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readback.name = self.name

    def _axes_dict(self):
        axes_dict={}
        return axes_dict

    def set_axis(self, obj, axis):
        self.obj  = obj
        axes_dict = self._axes_dict()

        self.setpoint.set_axis(axes_dict[axis])  
        self.readback.set_axis(axes_dict[axis])

    def get(self):
        return float(self.readback.get())

    def set(self, value):
        self.setpoint.set(value)
        return NullStatus()

    @property
    def position(self):
        """The current position of the motor in its engineering units
        Returns
        -------
        position : any
        """
        return float(self.readback.get())


class SimulatedAxisSource(RaypyngAxis):

    raypyng   = True    
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _axes_dict(self):
        axes_dict={"photonEnergy":self.obj.photonEnergy,
                    "numberRays": self.obj.numberRays,
                    }
        return axes_dict
    


    

class SimulatedAxisMisalign(RaypyngAxis):

    raypyng   = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _axes_dict(self):
        axes_dict={"translationXerror": self.obj.translationXerror,
                    "translationYerror": self.obj.translationYerror,
                    "translationZerror": self.obj.translationZerror,
                    "rotationXerror": self.obj.rotationXerror,
                    "rotationYerror": self.obj.rotationYerror,
                    "rotationZerror": self.obj.rotationZerror,
                    }
        return axes_dict

    

class SimulatedAxisAperture(RaypyngAxis):

    raypyng   = True
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _axes_dict(self):
        axes_dict={"totalWidth": self.obj.totalWidth,
                    "totalHeight": self.obj.totalHeight,
                    }
        return axes_dict

    

class SimulatedAxisGrating(RaypyngAxis):

    raypyng   = True
    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _axes_dict(self):
        axes_dict={"lineDensity": self.obj.lineDensity,
                    "orderDiffraction": self.obj.orderDiffraction,
                    "cFactor": self.obj.cFactor,
                    "lineProfile": self.obj.lineProfile,
                    "blazeAngle": self.obj.blazeAngle,
                    "aspectAngle": self.obj.aspectAngle,
                    "grooveDepth": self.obj.grooveDepth,
                    "grooveRatio": self.obj.grooveRatio,
                    }
        return axes_dict

    