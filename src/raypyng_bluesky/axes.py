from ophyd.device import Device
from ophyd import Component as Cpt
from ophyd.sim import NullStatus


from .signal import RayPySignalRO, RayPySignal
from .positioners import PVPositionerDone


class RaypyngAxis(PVPositionerDone):
    """The Axis used by all the Raypyng devices.

    At the moment it is a comparator, in the future some other positioner will be used, 
    probably a SoftPositioner.
    The class defines an empty dictionary, the ``axes_dict`` that will be then filled by each device.

    """    

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
        """Define an empty dictionary

        Returns:
            dict: empty dictionary
        """        
        axes_dict={}
        return axes_dict

    def set_axis(self, obj, axis):
        """Set what axis should be used, based on the ``axes_dict``

        Args:
            obj (_type_): _description_
            axis (_type_): _description_
        """        
        self.obj  = obj
        axes_dict = self._axes_dict()

        self.setpoint.set_axis(axes_dict[axis])  
        self.readback.set_axis(axes_dict[axis])

    def get(self):
        """return the value of a certain axis as in the RMLFile

        Returns:
            float: the value of the axis in the RML file
        """        
        return float(self.readback.get())

    def set(self, value):
        """Write a value in the RMLFile for a certain element/axis

        Args:
            value (float,int): the value to set to the axis

        """        
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
    """Define basic properties of the source, number of rays and photon energy in eV.

    """    

    raypyng   = True    
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _axes_dict(self):
        axes_dict={"photonEnergy":self.obj.photonEnergy,
                    "numberRays": self.obj.numberRays,
                    }
        return axes_dict
    


    

class SimulatedAxisMisalign(RaypyngAxis):
    '''Define basic properties of the all the optical elements after the source, 
    the misalignement along and about the axis.
    '''
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
    '''Define basic properties of the aperture, 
    the width and the height.
    '''
    raypyng   = True
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _axes_dict(self):
        axes_dict={"totalWidth": self.obj.totalWidth,
                    "totalHeight": self.obj.totalHeight,
                    }
        return axes_dict

    

class SimulatedAxisGrating(RaypyngAxis):
    '''Define basic properties of the gratings:
        - lineDensity        
        - orderDiffraction
        - cFactor
        - lineProfile
        - blazeAngle
        - aspectAngle
        - grooveDepth
        - grooveRatio
    '''
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

    