Tutorial
********

The code is thought to be used in an environment where bluesky is setup. For doing this it is convenient to create an ipython profile.
In the startup folder of the ipython profile create a file called ``0-bluesky.py`` that contains a minimal setup of bluesky and raypyng-bluesky. 

.. code:: python
    import os
    from bluesky import RunEngine
    from raypyng_bluesky.RaypyngOphydDevices import RaypyngOphydDevices

    RE = RunEngine({})	

    # Send all metadata/data captured to the BestEffortCallback.
    from bluesky.callbacks.best_effort import BestEffortCallback
    bec = BestEffortCallback()


    # Make plots update live while scans run.
    from bluesky.utils import install_kicker
    install_kicker()

    # create a temporary database
    from databroker import Broker
    db = Broker.named('temp')
    RE.subscribe(db.insert)
    RE.subscribe(bec)

    # import the magics
    from bluesky.magics import BlueskyMagics
    get_ipython().register_magics(BlueskyMagics)

    # import plans
    from bluesky.plans import (
        relative_scan as dscan, 
        scan, scan as ascan,
        list_scan,
        rel_list_scan,
        rel_grid_scan,  rel_grid_scan as dmesh,
        list_grid_scan,
        adaptive_scan,
        rel_adaptive_scan,
        inner_product_scan            as a2scan,
        relative_inner_product_scan   as d2scan,
        tweak)
    
    # import stubs
    from bluesky.plan_stubs import (
        abs_set,rel_set,
        mv, mvr,
        trigger,
        read, rd,
        stage, unstage,
        configure,
        stop)


    # insert here the path to the rml file that you want to use
    rml_path = ...

    RaypyngOphydDevices(RE=RE, rml_path=rml_path, temporary_folder=None, name_space=None, prefix=None)

Now you can start the ipython profile using:

.. code:: python
    ipython --profile=raypyng --matplotlib=qt5

Now you can access all the elements present in the rml file. If you set ``prefix=None``, the prefix ``rp_`` is automatically
prepended to the name of the optical elements found in the rml file to create the dame of the object in python. If you have a Dipole called 
``D13``, then the name would be: ``rp_D13``. You can now use the simulated motors as you would normally do in bluesky.



