Toolkit Overview
=================
The aim of this toolkit is to provide an easy way for researchers to share and use MATLAB code for aircraft design and analysis. The toolkit is made up of several packages, each of which provides a specific set of tools or functionality.
These packages can be installed and used independently, but they are designed to work together to provide a comprehensive set of tools for aircraft aeroelastic design and analysis.

The installation and usage of these packages is made easier by the use of a package manager for MATLAB, which allows users to install packages from various sources such as GitHub, MATLAB Central's File Exchange, or any URL pointing to a .zip file.

Below is a list of some of the packages included in this toolkit, along with their descriptions and links to their respective repositories. These packages are designed to be used in conjunction with each other, but can also be used independently depending on the user's needs.

This is followed by a brief installation guide and a tutorial on how to use the tools provided by these packages.

Package Overviews
+++++++++++++++++

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


Installation
+++++++++++++
Note – these tools have primarily been developed in Matlab 2024a; I make no guarantees that it will work in other versions…

1. Install Package Installer for matlab (pim) - go to the latest release page on Github `https://github.com/DCRG-Bristol/pim/releases/latest`` and download “pim.mltbx”. Opening this file with MATLAB already open will install the package manager.
2. Install the relevent package using pim. For example to install baff you can either:

   * run the command `pim install dcrg-bristo/baff` to install the latest release of the package from matlab in the MATLAB command window
   * run the command `pim install dcrg-bristo/baff -t vX.X.X.X”` to install the a specific version from github
   * clone the repository from github and run the command `pim install ads -u <INSTALL_DIR> --local -e –force` to install a local copy of the package

To install the latest verison of all the packages run the following commands in the MATLAB command window
:: 
   pim install dcrg-bristol/matlab-utilities
   pim install dcrg-bristol/matran
   pim install dcrg-bristol/baff
   pim install dcrg-bristol/ads
   pim install dcrg-bristol/flexcast
   pim install dcrg-bristol/laca

At this point all the latest toolboxes are installed. If you write the MATLAB command “pim freeze” it should show the installed toolboxes. This may seem like a lot of faff just to some examples, but the point here is that these codes are modular, and by being able to track which versions are installed on your machine it will be easier for you / other people to update the codebases on their machines and ... dare I say it … collaborate...

Getting Started
++++++++++++++++
Please see the Getting Started guides for the individual packages for more information on how to use the tools.


Developing your Own Package
+++++++++++++++++++++++++++
Below are a series of design guidelines for developing packages to contribute to this toolkit. These guidelines are not exhaustive, but they should help you get started with developing your own package.

1. Package Structure

   Your package should follow a consistent directory structure to make it easy to navigate and understand. Here is a suggested structure:

   ::

      project
      ├── tbx
      │   ├── +{your package name}
      │   │   ├── +{your package submodule}
      │   │   ├── your_functions.m
      ├── docs
      │   ├── index.rst
      ├── examples
      │   ├── example1.m
      ├── tests
      │   ├── your_functions_test.m
      ├── README.md
      ├── pathlist.txt
      ├── version.txt

   Your package should be placed in the ``tbx`` directory, with subdirectories for each module or submodule. An ``examples`` directory should contain example scripts demonstrating how to use your package, and the ``tests`` directory should contain unit tests for your package's functionality.

   - Package installer for matlab (pim) will read the ``pathlist.txt`` file to find the paths to your package directories. This file should contain the paths you want added to the matlab path, one per line (e.g. one line with tbx for simple packages).
   - The ``version.txt`` file should contain the version number of your package, which will be used by pim to manage package versions.
   - The ``README.md`` file should provide an overview of your package, including its purpose, how to install it, and how to use it.
1. Documentation

    Your package should include documentation to help users understand how to use it. If your package is included as a submodule in the drcg docs repository then

    - The `docs` directory will be copied to the docs repository and the documentation will be built using sphinx and included in the pacakge overview section. The entry point for sphinx will be `index.rst`. If this does nto exist only stub documentation will be made for this package.
    - The contents of `tbx` will be copied to the docs repository and the matlab sphinx extension will be used to generate documentation for the package. This auto-generated documentation is available in the API reference section of this website.


