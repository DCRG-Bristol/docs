Installation
============
Note – these tools have primarily been developed in Matlab 2024a; I make no guarantees that it will work in other versions…

1. Install Package Installer for matlab (pim) - go to the latest release page on Github `https://github.com/DCRG-Bristol/pim/releases`` and download “pim.mltbx”. Opening this file with MATLAB already open will install the package manager.
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
---------------
Please see the Getting Started guides for the individual packages for more information on how to use the tools.