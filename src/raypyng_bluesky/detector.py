from ophyd.signal import Signal
import time
import queue   
import threading
import os

import numpy as np

from ophyd.status import Status
from ophyd import Component as Cpt
from ophyd.device import Device


from raypyng.runner import RayUIRunner, RayUIAPI
from raypyng.postprocessing import PostProcess


class RaypyngDetector(Signal):
    raypyng = True
    _rays   = None
    def __init__(self, *args, information_to_extract='intensity', parent_detector_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.rml=None
        self.information_to_extract = information_to_extract
        self.parent_detector_name = parent_detector_name

    def set_rml(self, rml):
        self.rml = rml
        
    def put(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))

    def set(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))
    
    def set_simulation_temporary_folder(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def check_if_simulation_is_done(self,result_queue):
        # make sure tmp folder exists, if not create it
        sim_done = os.path.join(self.path,"simulation_done.txt")
        while not os.path.exists(os.path.join(self.path, self.parent_detector_name+"-RawRaysOutgoing.csv")):
            time.sleep(.1)
        result_queue.put(('done'))
        return 
    
    def trigger(self):
        
        q = queue.Queue()
        threads = threading.Thread(target=self.check_if_simulation_is_done(q), args=())
        threads.daemon = True
        threads.start()

        d = Status(self)
        d._finished()
        return d

    def get(self): 
        self._file_to_read = os.path.join(self.path, self.parent_detector_name+"_analyzed_rays.dat")
        self._rays = np.loadtxt(self._file_to_read)
        self.d = {'intensity':3, 
                'bandwidth':4, 
                'hor_foc':5, 
                'ver_foc':6, 
                }
        self.correction_for_ampere={'intensity':3, 
                'bandwidth':1, 
                'hor_foc':1, 
                'ver_foc':1, 
                }
        result = self._rays[self.d[self.information_to_extract]]
        result *= self.correction_for_ampere[self.information_to_extract]
        return result


class RaypyngTriggerDetector(Signal):
    raypyng = True
    raypyngTriggerDet = True
    def __init__(self, *args, rml, temporary_folder, **kwargs):
        super().__init__(*args, **kwargs)
        self.rml=rml
        self.path = temporary_folder
        self.exports_list = []

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def set_rml(self, rml):
        self.rml = rml
        
    def put(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))

    def set(self, value, *, timestamp=None, force=False):
        raise ReadOnlyError("The signal {} is readonly.".format(self.name))
    
    def set_simulation_temporary_folder(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def remove_done_simulation_file(self):
        sim_done = os.path.join(self.path,"simulation_done.txt")
        if os.path.exists(sim_done):
            os.remove(sim_done)

    def simulate(self,result_queue):
        self.remove_done_simulation_file()
        # make sure tmp folder exists, if not create it
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        r = RayUIRunner(ray_path=None, hide=True)
        a = RayUIAPI(r)
        self.rml.write(os.path.join(self.path,'tmp.rml'))
        r.run()
        a.load(os.path.join(self.path,'tmp.rml'))
        a.trace(analyze=False)
        a.save(os.path.join(self.path,'tmp.rml'))
        for exp in self.exports_list:
            aa=a.export(exp, "RawRaysOutgoing", self.path, '')
            pp = PostProcess()
            pp.postprocess_RawRays(exported_element=exp, 
                                exported_object='RawRaysOutgoing', 
                                dir_path=self.path, 
                                sim_number='', 
                                rml_filename=os.path.join(self.path,'tmp.rml'))
        
        a.quit()
        result_queue.put(('done'))
        return 
    
    def update_exports(self, exp):
        self.exports_list= exp

    def trigger(self):
        self.exports_list = list(set(self.exports_list))
        q = queue.Queue()
        threads = threading.Thread(target=self.simulate(q), args=())
        threads.daemon = True
        threads.start()

        d = Status(self)
        d._finished()
        sim_done = os.path.join(self.path,"simulation_done.txt")
        os.mknod(sim_done)
        return d
        
    def get(self): 
        return 1


class RaypyngDetectorDevice(Device):
    raypyng   = True
    intensity = Cpt(RaypyngDetector, name='_intensity[ph/s/0.1A/BW]', kind='hinted')
    bw =        Cpt(RaypyngDetector, name='_bandwidth[eV]', kind='hinted')
    hor_foc =   Cpt(RaypyngDetector, name='_hor_foc[um]', kind='hinted')
    ver_foc =   Cpt(RaypyngDetector, name='_Ver_foc[um]', kind='hinted')


    def __init__(self, *args,rml, tmp, **kwargs):
        super().__init__(*args, **kwargs)
        self.intensity.rml=rml
        self.intensity.set_simulation_temporary_folder(tmp)
        self.intensity.information_to_extract='intensity'
        self.intensity.parent_detector_name=self.name
        self.intensity.name = self.name+'_intensity[photons]'

        self.bw.rml=rml
        self.bw.set_simulation_temporary_folder(tmp)
        self.bw.information_to_extract='bandwidth'
        self.bw.parent_detector_name=self.name
        self.bw.name = self.name+'_bandwidth[eV]'

        self.hor_foc.rml=rml
        self.hor_foc.set_simulation_temporary_folder(tmp)
        self.hor_foc.information_to_extract='hor_foc'
        self.hor_foc.parent_detector_name=self.name
        self.hor_foc.name = self.name+self.hor_foc.name
        self.hor_foc.name = self.name+'_horizontal_focus[um]'


        self.ver_foc.rml=rml
        self.ver_foc.set_simulation_temporary_folder(tmp)
        self.ver_foc.information_to_extract='ver_foc'
        self.ver_foc.parent_detector_name=self.name
        self.ver_foc.name = self.name+self.ver_foc.name
        self.ver_foc.name = self.name+'_vertical_focus[num]'



        

    