Package Overviews
============
An overview of each of the packages is given below, followed by an installation guide and a brief tutorial on how to use the tools.

Package Installer for Matlab (pim)
**********************************
https://github.com/DCRG-Bristol/pim

A simple package manager for Matlab (inspired by pip). can install local pacakges or download packages from Matlab Central's File Exchange, GitHub repositories, or any other url pointing to a .zip file.
This is a slightly adapted version of the original package installer developed by mobeets. The original version can be found `here <https://uk.mathworks.com/matlabcentral/fileexchange/54548-mobeets-mpm>`_.
All the packages listed here can be installed with this package manager.

Matlab Utilities
****************
https://github.com/DCRG-Bristol/Matlab-Utilities

A collection of smaller MATLAB functions for shared collaboration across researchers. Many of the other packages decribed here depend on this package.

Matran
******
https://github.com/DCRG-Bristol/Matran

A collection of functions and classes for importing, visualising and writing Nastran bulk data entries and results files.

Bristol Aircraft File Format (baff)
***********************************
https://github.com/DCRG-Bristol/baff

A matlab toolbox to create platform / analysis tool agnostic files defining aircraft geometries.
Items such as the fuselage / wings / engines can be defined programmatically and can be saved in a format that is independent of a particular analysis tool.
Currently BAFF geometries can only be generated in Matlab, however all BAFF aircraft can be saved to an hdf5 file, which could be read by any analysis tool on any platform.
The aim in the future would be for different researchers to make different analysis toolboxes all of which could run from the same BAFF files.

Aeroelastic Development Suite (ads)
***********************************
https://github.com/DCRG-Bristol/ads

A collection of functions and classes to generate Nastran models programmatically and run in Nastran. Works well with BAFF to create generic geometries and run analysis.

Conceptual aircraft sizing tool for flexible aircraft (FlexCAST)
****************************************************************
https://github.com/DCRG-Bristol/flexcast

A conceptual aircraft sizing tool that can be used to size flexible aircraft. The tool is based on the BAFF and ADS packages and can be used to generate a Nastran model of a flexible aircraft, run aeroelastic analysis and size the aircrafts wing structure.

LACA Framework
**************
https://github.com/DCRG-Bristol/LACA

A unpolished collection of function to generate VLM models for aeroealstic anaylsis.