How To Guides
**************

Change grating
===========================
This feature is stil experimental, and the implementation is poor. However, the method can still be used to implement a grating change.


When we call the ``RaypyngOphydDevices`` class, Ophyd devices are automatically created
.. code:: python

    from raypyng_bluesky.RaypyngOphydDevices import RaypyngOphydDevices

    # define here the path to the rml file
    rml_path = ('...rml/elisa.rml')

    RaypyngOphydDevices(RE=RE, rml_path=rml_path, temporary_folder=None, name_space=None, ray_ui_location='/home/simone/RAY-UI-development')#sys._getframe(0))

In this case we know that inside the ``elisa.rml`` file we have a plane grating monochromator, and an elment that is the a plane grating called ``PG``, 
and that an Ophyd device called ``rp_PG`` is therefore created. The gratings can hold the configuration of up to two gratings, so we can set them up.
The first grating is a laminar grating with 400 lines/mm pitch. In this case we can fill the template below. The parameter ``blazeAngle`` can be set to None, 
since it is not relevant for a laminar grating

.. code:: python

    # PG is automatically created
    rp_PG.grating1={'lineDensity':400, 
                    'orderDiffraction':1,
                    'lineProfile':'laminar',
                    'blazeAngle':None,
                    'aspectAngle':90,
                    'grooveDepth':15,
                    'grooveRatio':0.65,}

the second grating is a blazed grating with a pitch of 1200 lines/mm. In this case the ``grooveDepth`` and the ``grooveRatio`` are not 
relevant, and can be set to any arbitrary number.

.. code:: python

    rp_PG.grating2 = {'lineDensity':1200, 
                    'orderDiffraction':1,
                    'lineProfile':'blazed', 
                    'blazeAngle':0.9,
                    'aspectAngle':176.4,
                    'grooveDepth':15,
                    'grooveRatio':0.65,}

To change the gratings then, one can use the method implmented in the grating Ophyd device to change the grating, giving as
argument the pitch of the grating. To use the blazed grating use:

.. code:: python

    rp_PG.change_grating(lineDensity=1200)

while to use the laminar grating:

.. code:: python

    rp_PG.change_grating(lineDensity=400)


