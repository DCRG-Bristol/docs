Binary Aircraft File Format (baff)
===================================
https://github.com/dcrg-bristol/baff

Baff is a platfrom agnostic, binary, schema for aircraft structures. It aims to allow engineers to exchange infomration between different analysis tools is a seemless fashion.

By ensuring all analysis tools start with a common model description, data tranfers / comparisons can easily be made between differnt tools

.. image:: https://github.com/DLR-SL/CPACS/blob/develop/development/images/centralized.png?raw=true
    :align: center


The struture is inspired by similar projects such as `CPACS <https://github.com/DLR-SL/CPACS>`_, indeed the image above is lifted from that project. However the primary differences with Baff are:

1. The code is fully open-source
2. Baff objects can be saved to Binary HDF5 files, rather than seriilsed text such as XML or Json.

So far only a Matlab reader is available for Baff, and the descriptions in the guide will leverage Matlab syntax. However, the schema has been design for use across multiple langauges and paltforms.

Basic Achitecture
------------------

A Baff model is made up from a series of *Elements* which have the following properties:
(Orientation Parameters)

- **Parent** - a link to a Parent element this location of this object is defined from
- **Children** - Elements whos location is derived from this element
- **Offset** - a 3x1 vector defining the offset between the orign of the parent and the origin of the element (in the parents reference frame)
- **A** - a 3x3 rotation matrix defining the orientation of the elements frame of refernce (relative to the elements parent)
- ------*(Normalised Positon along some refernce line: for use in beam elements)*------
- **Eta** Normailised postion along the Parents reference line - default 0
- **EtaLength** Length to normalise the reference line with - default 0
- ------*(Extra Info)*------
- **Index** - Unique reference for each element
- **Name** - name of the element


All elements in a baff model are derived from this Base Elements. Current Element Types are:

- **Point** - a point in 3D space
- **Mass** - (derived from *Point*) a discrete mass and inertia tensor
- **Beam** - Defines a 1D beam along a reference line
- **Bluff Body** - (derived from *Beam*) adds volume to a beam (e.g. for fuselages)
- **Wing** - (derived from *Beam*) adds a lifting surface to a beam.
- **Constraint** - restricts the degrees of freedom at a point
- ------*(other more specifc elements)*------
- **Fuel** - (derived from *Mass*) a special mass to easily change the fuel filling level of a model
- **Payload** - (derived from *Mass*) a special mass to easily change the payload filling level of a model
- **Control Surface** - Defines a control surface on a wing.

All elements are stored in a *Model* object, which along is lists of all elements instances has a list of *Orphans*. Orphans are Elements without a Parent, there positon and orientation is defined from the global reference frame. Orphans are the starting point for decending the *tree* of elements.

Beam Elements
++++++++++++++

Beam elements are a foundation for flexible and rigid structures. They have a notion of a normalised 1D refernce line (e.g. its length is nomralised by EtaLength).

Beam Element have a Property **Station** which is an array of *Station* elements. Each station has the following properties:

- **A** - 1D beam Aero
- **I** - 3x3 second moment of area tensor
- **J** - Torsion constant
- **Mat** - Material properties
- **Eta** - Normalise location along the reference line
- **EtaDir** - the direction of the eference line at this station (nominaly points along the x axis)
- **Station Dir** - defined the beams y axis (for loads etc...)

The array of *stations* must monotoniclly increase in Eta, and there defines the 1D refernce line in space and its structural / mass properties.

Wing Elements
++++++++++++++

Wing elements are the same as Beam elements, but have an additonal array of *AeroStations*. Each *AeroStations* defines the variton in aerodyanmic properties along the refernce line. e.g.:

- **Eta** - Normalise location along the reference line
- **Station Dir** - chordwise direcion of the station
- **Chord** - wing chord
- **Twist** - Twist
- **BeamLoc** - the chordwise position of the beam refernce line, normalised by the chord
- **Airfoil** - normalised Airfoil geometry
- **ThicknessRatio** - Thickness to Chord Ratio
- **LiftCurveSlope** - Local Linear Lift Curve Slope 
- ------*(Spanwise distributed mass properties)*-------
- **Lienar Density** - wings mass per unit length
- **Linear Ineria** - inertia tensor per unit length
- **MassLoc** - Chordwise location of distributed mass (normalised to chord)

Wings also have a list of control surfaces

Wing Elements
++++++++++++++

Bluff bodys are similar to wings and have a array of bluff body station. which are the same as a beam station with the addition of a *Radius* property.

Matlab Implentation
---------------------

The matlab specific implemntation of a Baff object has a series of helper function to simplify the creation, manipulation and visulisation process.

This documentation is not exhaustive, it is a good idea to familirise yourself with the structure of the baff codebase as it may be the best place to search fro helper functions
https://github.com/DCRG-Bristol/baff

- The main namespace :code:`baff.` contains all of teh base elements.
- :code:`baff.Model` is teh main model file which all baff elements are added to.
- The namespace :code:`baff.station.` contains all of the refernce line station definitions.
- the folder *examples* has some example making simple structures and is a good starting point 

All elements have the method :code:`.draw()` which will draw the object (and all its children to the screen). Looking in the draw methods is a good way to learn how to get the global location of differnt elemets!

Other examples of Baff models can be found here https://github.com/DCRG-Bristol/aeroelastic_examples/tree/master/tbx/%2Bae_models 


More documentation to follow......




