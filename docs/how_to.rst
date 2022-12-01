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
