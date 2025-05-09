Frequently Asked Questions
==========================

**When I restart Matlab the installed packages are not availible?**

Each time you restart matlab you will need to run the command “pim init” to add all the toolbox paths to MATLAB’s path. If you want to automate this, you can add the command to your <startup.m 'https://uk.mathworks.com/help/matlab/ref/startup.html'>_ file.

**When running Nastran analysis the program exits prior to the analysis being completed?**

The first time you run a Nastran analysis a file dialog box will open asking you to select a Nastran executable. These can be found somewhere like “C:\MSC.Software\MSC_Nastran\2022.1\bin”. You want to select the “nastran.exe” executable, not for example the “nastranw.exe”…. If you select the wrong one or just want to change which executable you use, run the command “ads.nast.getExe(true)”, this will reopen the dialog box so you can pick a different executable.

**I Cant read the results on an Aeroelastic analysis from the HDF5 file (Nastran)?**

Aeroelastic analysis in Nastran changed significantly between the 2018 and 2022 releases (the two we can install on Uni machines). The sol144 and 145 solution probably will only work with Nastran 2022 whereas the sol103 solution should work with previous versions (more results are now stored in the hdf5 file which is much quicker to read). 

**Is there more documentation?**

Documentation for each of the toolboxes is limited however in each of the repositories there are a few examples files (e.g. https://github.com/DCRG-Bristol/baff/tree/master/Examples or https://github.com/DCRG-Bristol/ads/tree/master/Examples). More examples will be added with time. Additionally, I like to think the codebases are well structured, so by looking though the code bases you can get a feel for what it does. In the future though more documentation will be made (if these toolboxes gain any traction….)

