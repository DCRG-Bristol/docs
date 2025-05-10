Binary Aircraft File Format (Baff)
===================================
https://github.com/dcrg-bristol/baff

Baff is a platform-agnostic, binary schema for aircraft structures. It aims to allow engineers to exchange information seamlessly between different analysis tools.

By ensuring all analysis tools start with a common model description, data transfers/comparisons can easily be made between different tools

.. image:: https://github.com/DLR-SL/CPACS/blob/develop/development/images/centralized.png?raw=true
    :align: center


The structure is inspired by similar projects such as `CPACS <https://github.com/DLR-SL/CPACS>`_. Indeed, the image above is lifted from that project. However, the primary differences with Baff are:

1. The code is fully open-source
2. Baff objects can be saved to Binary HDF5 files rather than serialised text such as XML or JSON.

So far, only a Matlab reader is available for Baff, and the descriptions in the guide will leverage Matlab syntax. However, the schema has been designed for use across multiple languages and platforms.

Basic Architecture
------------------

A Baff model is made up of a series of *Elements* which have the following properties:
(Orientation Parameters)

- **Parent** - a link to a Parent element. The location of this object is defined from
- **Children** - Elements whose location is derived from this element
- **Offset** - a 3x1 vector defining the offset between the origin of the parent and the origin of the element (in the reference frame of the parent)
- **A** - a 3x3 rotation matrix defining the orientation of the element's frame of reference (relative to the element's parent)
- ------*(Normalised Positon along some reference line: for use in beam elements)*------
- **Eta** Normalised position along the Parents reference line - default 0
- **EtaLength** Length to normalise the reference line with - default 0
- ------*(Extra Info)*------
- **Index** - Unique reference for each element
- **Name** - name of the element


All elements in a baff model are derived from this base element. Current element types are:

- **Point** - a point in 3D space
- **Mass** - (derived from *Point*) a discrete mass and inertia tensor
- **Beam** - Defines a 1D beam along a reference line
- **Bluff Body** - (derived from *Beam*) adds volume to a beam (e.g. for fuselages)
- **Wing** - (derived from *Beam*) adds a lifting surface to a beam.
- **Constraint** - restricts the degrees of freedom at a point
- ------*(other more specific elements)*------
- **Fuel** - (derived from *Mass*) a special mass to easily change the fuel filling level of a model
- **Payload** - (derived from *Mass*) a special mass to easily change the payload filling level of a model
- **Control Surface** - Defines a control surface on a wing.

All elements are stored in a *Model* object, which, along with lists of all element instances, has a list of *Orphans*. Orphans are Elements without a Parent; their position and orientation are defined from the global reference frame. Orphans are the starting point for deciding the *tree* of elements.

Beam Elements
++++++++++++++

Beam elements are the foundation for flexible and rigid structures. They have a notion of a normalised 1D reference line (e.g., their length is normalised by EtaLength).

Beam Element has a Property **Station**, an array of *Station* elements. Each station has the following properties:

- **A** - 1D beam Aero
- **I** - 3x3 second moment of area tensor
- **J** - Torsion constant
- **Mat** - Material properties
- **Eta** - Normalise location along the reference line
- **EtaDir** - the direction of the reference line at this station (nominally points along the x-axis)
- **Station Dir** - defines the beam's y-axis (for loads etc...)

The array of *stations* must monotonically increase in Eta; therefore, it defines the 1D reference line in space and its structural / mass properties.

Wing Elements
++++++++++++++

Wing elements are the same as Beam elements, but have an additional array of *AeroStations*. Each *AeroStations* defines the variation in aerodynamic properties along the reference line. e.g.:

.. param: test

- **Eta** - Normalise location along the reference line
- **Station Dir** - chordwise direction of the station
- **Chord** - wing chord
- **Twist** - Twist
- **BeamLoc** - the chordwise position of the beam reference line, normalised by the chord
- **Airfoil** - normalised Airfoil geometry
- **ThicknessRatio** - Thickness to Chord Ratio
- **LiftCurveSlope** - Local Linear Lift Curve Slope 
- ------*(Spanwise distributed mass properties)*-------
- **Linear Density** - wings mass per unit length
- **Linear Ineria** - inertia tensor per unit length
- **MassLoc** - Chordwise location of distributed mass (normalised to chord)

Wings also have a list of control surfaces.

Wing Elements
++++++++++++++

Bluff bodies are similar to wings and have an array of bluff body stations, which are the same as beam stations with the addition of a *Radius* property.

Matlab Implementation
---------------------

The Matlab-specific implementation of a Baff object has a series of helper functions to simplify the creation, manipulation, and visualisation process.

This documentation is not exhaustive; it is a good idea to familiarise yourself with the structure of the baff codebase as it may be the best place to search for helper functions
https://github.com/DCRG-Bristol/baff

- The main namespace ``baff.`` contains all base elements.
- ``baff.Model`` is the main model file to which all baff elements are added.
- The namespace ``baff.station.`` contains all the reference line station definitions.
- the folder *examples* has some examples of making simple structures and is a good starting point 

All elements have the method ``.draw()``, which draws the object (and all its children to the screen). Looking at the "draw" methods is a good way to learn how to get the global location of different elements!

Other examples of Baff models can be found here https://github.com/DCRG-Bristol/aeroelastic_examples/tree/master/tbx/%2Bae_models 


More documentation to follow...

