from raypyng_bluesky.devices import SimulatedPGM, SimulatedApertures, SimulatedMirror, SimulatedSource
from raypyng_bluesky.detector import RaypyngDetectorDevice, RaypyngTriggerDetector

from raypyng_bluesky.run_engine_stuff import SupplementalDataRaypyng

from raypyng.rml import RMLFile


import sys

class RaypyngOphydDevices():

    def __init__(self, *args, RE, rml_path, temporary_folder, name_space=None, **kwargs):
        
        self.RE = RE

        self.rml = RMLFile(rml_path)
        self.temporary_folder = temporary_folder
        self.name_space = name_space.f_globals
        

        mirrors = ['Toroid', 'PlaneMirror', 'Cylinder', 'Ellipsoid']
        mirror_dict = {k:SimulatedMirror for k in mirrors}

        sources = ['Dipole']
        source_dict = {k:SimulatedSource for k in sources}

        monos = ['PlaneGrating']
        mono_dict = {k:SimulatedPGM for k in monos}

        apertures = ['Slit']
        aperture_dict = {k:SimulatedApertures for k in apertures}

        detectors = ['ImagePlane']
        detector_dict = {k:RaypyngDetectorDevice for k in detectors}

        self.type_to_class_dict ={**mirror_dict, 
                            **source_dict, 
                            **mono_dict, 
                            **aperture_dict,
                            **detector_dict}
        self.create_raypyng_elements_from_rml()
        self.create_trigger_detector()
        self.append_preprocessor()
    
    def create_raypyng_elements_from_rml(self):
        if self.name_space is None: 
            self.name_space = sys._getframe(1).f_globals
        ret = ()
        for oe in self.rml.beamline.children():
            cls = self.type_to_class_dict[oe['type']]
            k = oe['name']
            if oe['type'] == 'ImagePlane':
                self.name_space[k] = cls(name=k, rml=self.rml, tmp=self.temporary_folder)
                ret = ret + (self.name_space[k],)
            else:
                self.name_space[k] = cls(obj=oe, name=k)
                ret = ret + (self.name_space[k],)
        return ret
    
    def create_trigger_detector(self):
        ret = ()
        k = 'TriggerDetector'
        cls = RaypyngTriggerDetector
        self.name_space[k] = cls(name='RaypyngTriggerDetector', rml=self.rml, temporary_folder=self.temporary_folder)
        ret = ret + (self.name_space[k],)

    def trigger_detector(self):
        return self.name_space['TriggerDetector']
    
    def append_preprocessor(self):
        TriggerDetector = self.trigger_detector()
        sd = SupplementalDataRaypyng(trigger_detector=TriggerDetector)
        self.RE.preprocessors.append(sd) 




