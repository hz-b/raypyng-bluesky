How To Guides
**************

Change grating
===========================
This feature is stil experimental, and the implementation is somehow poor. However, the method can still be used to implement a grating change.


When the ``RaypyngOphydDevices`` class is called, Ophyd devices are automatically created
.. code:: python

    from raypyng_bluesky.RaypyngOphydDevices import RaypyngOphydDevices

    # define here the path to the rml file
    rml_path = ('...rml/elisa.rml')

    RaypyngOphydDevices(RE=RE, rml_path=rml_path, temporary_folder=None, name_space=None, ray_ui_location='/home/simone/RAY-UI-development')#sys._getframe(0))

In this case we know that inside the ``elisa.rml`` file we have a plane grating monochromator, and an elment that is the a plane grating called ``PG``, 
and that an Ophyd device called ``rp_PG`` is therefore created. The gratings can hold any number of different configurations, and the configuration found in the 
rml file is saved with the name ``'default'``
We can rename the default grating to a more meaningful name, in this case since it is a 1200 lines/mm blazed grating we will call it simply '1200'
.. code:: python

    rp_PG.rename_default_grating('1200')


the second grating is a laminar grating with a pitch of 400 lines/mm. 

.. code:: python

    rrp_PG.gratings=('400', {'lineDensity':400, 
                        'orderDiffraction':1,
                        'lineProfile':'laminar',
                        'aspectAngle':90,
                        'grooveDepth':15,
                        'grooveRatio':0.65,}
                )

To change the gratings then, one can use the method implmented in the grating Ophyd device to change the grating, giving as
argument the pitch of the grating. To use the blazed grating use:

.. code:: python

    rp_PG.change_grating('1200')

while to use the laminar grating:

.. code:: python

    rp_PG.change_grating('400')


Four different kind of gratings can be implemented: ``blazed``,
``laminar``, ``sinus``, and ``unknown``. Each grating needs slightly different
parameters:

.. code:: python
    
    grating_dict_keys_blazed = {'name': 
                                    {'lineDensity':value,
                                    'orderDiffraction':value,
                                    'lineProfile':value,
                                    'blazeAngle':value,
                                    'aspectAngle':value,
                                    }
                                }
    grating_dict_keys_laminar = {'name':
                                    {'lineDensity':value,
                                    'orderDiffraction:value',
                                    'lineProfile':value,
                                    'aspectAngle':value,
                                    'grooveDepth':value,
                                    'grooveRatio':value,
                                    }
                                }
    grating_dict_keys_sinus   = {'name':
                                    {'lineDensity':value,
                                    'orderDiffraction':value,
                                    'lineProfile':value,
                                    'grooveDepth':value,
                                    }
                                }

    grating_dict_keys_unknown = {'name':
                                    {'lineDensity':value,
                                    'orderDiffraction':value,
                                    'lineProfile':value,
                                    'gratingEfficiency':value
                                    }
                                }

Write your own simulation Engine
=================================

The simulations are performed using RAY-UI on a local computer. However, in the future,
more simulation engine can be easily written, as long the following three methods are provided.


.. code:: python

    class SimulatonEngineCUSTOM():
        
        def __init__(self) -> None:
                
            pass

        def check_if_simulation_is_done(self):
            pass
        
        def setup_simulation(self):
            pass

        def simulate(self, path):
            '''the result of the simulation must be saved in the temporary_folder
            os.path.join(path,'tmp')
            '''
            pass

Your simulation engine should export in the `tmp` folder a file with the following columns and a header:

.. code:: bash

    # SourcePhotonFlux	NumberRaysSurvived	PercentageRaysSurvived	PhotonFlux	Bandwidth	HorizontalFocusFWHM	VerticalFocusFWHM
    6.934960000000000000e+12	1.000000000000000000e+04	1.000000000000000000e+02	6.934960000000000000e+12	-4.999559755833615782e-02	1.904934623550874839e+00	5.918353021235417399e-01

At the moment the detectors will extract only the `PhotonFlux`, `Bandwidth`, `HorizontalFocusFWHM`, and the `VerticalFocusFWHM`.
Since it is not clear how the program will develop in the future, even if not used save all the columns, including the not used
`SourcePhotonFlux`,	`NumberRaysSurvived`, and `PercentageRaysSurvived` (They can be zeros). 
