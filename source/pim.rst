Package Installer for Matlab (pim)
==================================

A simple package manager for Matlab (inspired by `pip <https://github.com/pypa/pip>`_. Downloads packages from Matlab Central's File Exchange, GitHub repositories, or any other url pointing to a .zip file.

This has been slightly edited to suite the style used in the dcrg repositories.

Quickstart
----------
| Downlaod the latest Binary from the github repository https://github.com/DCRG-Bristol/pim/releases
| run the binary **pim.mltbx** with Matlab open

writing ``pim freeze`` should now complain no packages are installed.

The following is a brief list of pim commands:

- `pim install [package-name]`: install package by name
- `pim uninstall [package-name]`: remove package, if installed
- `pim search [package-name]`: search for package given name (checks Github and Matlab File Exchange)
- `pim freeze`: lists all packages currently installed
- `pim init`: adds all installed packages to path (run when Matlab starts up)
- `pim clear`: uninstall all pacakges
- `pim install -i [myfile.txt]`: install a set of packages from a file
Install a single package
************************

Install (searches FileExchange and Github)::

    pim install export_fig

When installing, pim checks for a file in the package called `install.m`, which it will run after confirming (or add `--force` to auto-confirm). It also checks for a file called `pathlist.txt` which tells it which paths (if any) to add.

**Install a Github release (by tag, branch, or commit)** ::

    pim install matlab2tikz -t 1.0.0
    pim install matlab2tikz -t develop
    pim install matlab2tikz -t ca56d9f

**Uninstall** ::

    pim uninstall matlab2tikz

When uninstalling, pim checks for a file in the package called `uninstall.m`, which it will run after confirming (or add `--force` to auto-confirm).

**Search without installing** ::

    pim search export_fig

**Install from a url** ::

    pim install covidx -u https://www.mathworks.com/matlabcentral/fileexchange/76213-covidx
    pim install export_fig -u https://github.com/altmany/export_fig.git

.. note:: 
    1. When specifying Github repo urls you must add the '.git' to the url.
    2. I may have broken this with the latest re-factor...

**Install local package** ::

    pim install my_package -u path/to/package --local

The above will copy `path/to/package` into the default install directory. To skip the copy, add `-e` to the above command.

**Overwrite existing packages** ::

     pim install matlab2tikz --force

**Install/uninstall packages in a specific directory** ::
     
     pim install matlab2tikz -d /Users/mobeets/mypath
     
The default installation directory is `pim-packages/`.

**Installing multiple packages from file** ::

    pim install -i /Users/mobeets/example/requirements.txt

Specifying a requirements file lets you install or search for multiple packages at once. See 'requirements-example.txt' for an example. Make sure to provide an absolute path to the file!

To automatically confirm installation without being prompted, set `--approve`. Note that this is only available when installing packages from file.

What it does
---------------

By default, pim installs all Matlab packages to the directory `pim-packages/`. (You can edit `pim_config.m` to specify a custom default installation directory.)

If you restart Matlab, you'll want to run `pim init` to re-add all the folders in the installation directory to your Matlab path. Better yet, just run `pim init` from your Matlab `startup script <http://www.mathworks.com/help/matlab/ref/startup.html>`_.

Which directoies are added to the path
------------------

By default no directories are added to the path. pim looks for the file `pathlist.txt` it will then add all the the specified directories to the path.

pim keeps track of the packages it's downloaded in matlab preferences.

Requirements
---------------

pim should work cross-platform on versions Matlab 2014b and later.
