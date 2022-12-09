from ophyd.signal import Signal
import time
import queue   
import threading
import os
import shutil

import numpy as np

from ophyd.status import Status
from ophyd import Component as Cpt
from ophyd.device import Device


from raypyng.runner import RayUIRunner, RayUIAPI
from raypyng.postprocessing import PostProcess


class SimulatonEngineRAYUI():
        
    def __init__(self, ray_ui_location:str) -> None:
        self.ray_ui_location = ray_ui_location

    def check_if_simulation_is_done(self):
        return self.a._simulation_done
    
    def setup_simulation(self):
        self.r = RayUIRunner(ray_path=self.ray_ui_location, hide=True)
        self.a = RayUIAPI(self.r)
        return self.a

    def simulate(self, path, rml, exports_list):
        # make sure tmp folder exists, if not create it
        if not os.path.exists(path):
            os.makedirs(path)
        rml.write(os.path.join(path,'tmp.rml'))
        self.r.run()
        self.a.load(os.path.join(path,'tmp.rml'))
        self.a.trace(analyze=False)
        self.a.save(os.path.join(path,'tmp.rml'))
        for exp in exports_list:
            self.a.export(exp, "RawRaysOutgoing", path, '')
            pp = PostProcess()
            pp.postprocess_RawRays(exported_element=exp, 
                                exported_object='RawRaysOutgoing', 
                                dir_path=path, 
                                sim_number='', 
                                rml_filename=os.path.join(path,'tmp.rml'))
        
        self.a.quit()
        return 






    