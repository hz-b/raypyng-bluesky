from ophyd.device import Device
from ophyd import Component as Cpt


from .axes import SimulatedAxisSource, SimulatedAxisMisalign 
from .axes import SimulatedAxisAperture, SimulatedAxisGrating

class MisalignComponents(Device):
    raypyng  = True
    tx       = Cpt(SimulatedAxisMisalign, name="translationXerror", kind='normal')
    ty       = Cpt(SimulatedAxisMisalign, name="translationYerror", kind='normal')
    tz       = Cpt(SimulatedAxisMisalign, name="translationZerror", kind='normal')
    rx       = Cpt(SimulatedAxisMisalign, name="rotationXerror", kind='normal')
    ry       = Cpt(SimulatedAxisMisalign, name="rotationYerror", kind='normal')
    rz       = Cpt(SimulatedAxisMisalign, name="rotationZerror", kind='normal')
        
    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args, **kwargs)
        self.tx.set_axis(obj=obj, axis="translationXerror")
        self.ty.set_axis(obj=obj, axis="translationYerror")
        self.tz.set_axis(obj=obj, axis="translationZerror")
        self.rx.set_axis(obj=obj, axis="rotationXerror")
        self.ry.set_axis(obj=obj, axis="rotationYerror")
        self.rz.set_axis(obj=obj, axis="rotationZerror")

class SimulatedPGM(MisalignComponents):
    raypyng  = True
    cff               = Cpt(SimulatedAxisGrating, name='cFactor')
    lineDensity       = Cpt(SimulatedAxisGrating, name='lineDensity')
    orderDiffraction  = Cpt(SimulatedAxisGrating, name='orderDiffraction')
    lineProfile       = Cpt(SimulatedAxisGrating, name='lineProfile')
    blazeAngle        = Cpt(SimulatedAxisGrating, name='blazeAngle')
    aspectAngle       = Cpt(SimulatedAxisGrating, name='aspectAngle')
    grooveDepth       = Cpt(SimulatedAxisGrating, name='grooveDepth')
    grooveRatio       = Cpt(SimulatedAxisGrating, name='grooveRatio')
    grating1 = {'lineDensity':None, 
                'orderDiffraction':None,
                'lineProfile':None,
                'blazeAngle':None,
                'aspectAngle':None,
                'grooveDepth':None,
                'grooveRatio':None,}
    grating2 = {'lineDensity':None, 
                'orderDiffraction':None,
                'lineProfile':None,
                'blazeAngle':None,
                'aspectAngle':None,
                'grooveDepth':None,
                'grooveRatio':None,}

        
    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args,obj=obj, **kwargs)
        self.cff.set_axis(obj=obj, axis="cFactor")
        self.lineDensity.set_axis(obj=obj, axis="lineDensity")
        self.orderDiffraction.set_axis(obj=obj, axis="orderDiffraction")
        self.lineProfile.set_axis(obj=obj, axis="lineProfile")
        self.blazeAngle.set_axis(obj=obj, axis="blazeAngle")
        self.aspectAngle.set_axis(obj=obj, axis="aspectAngle")
        self.grooveDepth.set_axis(obj=obj, axis="grooveDepth")
        self.grooveRatio.set_axis(obj=obj, axis="grooveRatio")

    def change_grating(self, lineDensity):
        if lineDensity == self.grating1['lineDensity']:
            grating = self.grating1
        elif lineDensity == self.grating2['lineDensity']:
            grating = self.grating2
        else:
            raise ValueError('This grating does not exists')
        self.lineDensity.set(grating['lineDensity'])
        self.orderDiffraction.set(grating['orderDiffraction'])
        self.lineProfile.set(grating['lineProfile'])
        self.blazeAngle.set(grating['blazeAngle'])
        self.aspectAngle.set(grating['aspectAngle'])
        self.grooveDepth.set(grating['grooveDepth'])
        self.grooveRatio.set(grating['grooveRatio'])
        
        
        
class SimulatedApertures(MisalignComponents):
    raypyng  = True
    width    = Cpt(SimulatedAxisAperture, name="totalWidth", kind='normal')
    height   = Cpt(SimulatedAxisAperture, name="totalHeight", kind='normal')
        
    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args,obj=obj, **kwargs)
        self.width.set_axis(obj=obj, axis="totalWidth")
        self.height.set_axis(obj=obj, axis="totalHeight")


class SimulatedMirror(MisalignComponents):
    raypyng  = True
    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args,obj=obj, **kwargs)

          

class SimulatedSource(Device):
    raypyng  = True
    en       = Cpt(SimulatedAxisSource, name="source_en", kind='normal')
    nrays    = Cpt(SimulatedAxisSource, name="source_nrays", kind='normal')
        
    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args, **kwargs)
        self.en.set_axis(obj=obj, axis="photonEnergy")  
        self.nrays.set_axis(obj=obj, axis="numberRays")