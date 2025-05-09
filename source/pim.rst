Package Installer for Matlab (pim)
==================================

A simple package manager for Matlab (inspired by `pip <https://github.com/pypa/pip>`_. Downloads packages from Matlab Central's File Exchange, GitHub repositories, or any other url pointing to a .zip file.

This has been slightly edited to suite the style used in the dcrg repositories.

Quickstart
----------

Download/clone this repo and add it to your Matlab path. To persevre this after install please add the following two line to you `startup.m script <https://uk.mathworks.com/help/matlab/ref/startup.html>`_. Now try the following:

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

When installing, mpm checks for a file in the package called `install.m`, which it will run after confirming (or add `--force` to auto-confirm). It also checks for a file called `pathlist.txt` which tells it which paths (if any) to add.

Install a Github release (by tag, branch, or commit)::
    pim install matlab2tikz -t 1.0.0
    pim install matlab2tikz -t develop
    pim install matlab2tikz -t ca56d9f

Uninstall::
    pim uninstall matlab2tikz

When uninstalling, pim checks for a file in the package called `uninstall.m`, which it will run after confirming (or add `--force` to auto-confirm).

Search without installing::
    pim search export_fig

Install from a url::
    pim install covidx -u https://www.mathworks.com/matlabcentral/fileexchange/76213-covidx
    pim install export_fig -u https://github.com/altmany/export_fig.git

(Note that when specifying Github repo urls you must add the '.git' to the url.)
(Note - I may have broken this with the latest re-factor....)

Install local package::
    pim install my_package -u path/to/package --local

The above will copy `path/to/package` into the default install directory. To skip the copy, add `-e` to the above command.

Overwrite existing packages::
    pim install matlab2tikz --force

Install/uninstall packages in a specific directory::
    pim install matlab2tikz -d /Users/mobeets/mypath

Note that the default installation directory is `pim-packages/`.

Installing multiple packages from file::
    pim install -i /Users/mobeets/example/requirements.txt

Specifying a requirements file lets you install or search for multiple packages at once. See 'requirements-example.txt' for an example. Make sure to provide an absolute path to the file!

To automatically confirm installation without being prompted, set `--approve`. Note that this is only available when installing packages from file.

What it does
---------------

By default, pim installs all Matlab packages to the directory `pim-packages/`. (You can edit `pim_config.m` to specify a custom default installation directory.)

If you restart Matlab, you'll want to run `pim init` to re-add all the folders in the installation directory to your Matlab path. Better yet, just run `pim init` from your Matlab [startup script](http://www.mathworks.com/help/matlab/ref/startup.html).

Troubleshooting
------------------

Because there's no standard directory structure for a Matlab package, automatically adding paths can get a bit messy. When pim downloads a package, it adds a single folder within that package to your Matlab path. If there are no `*.m` files in the package's base directory, it looks in folders called 'bin', 'src', 'lib', or 'code' instead. You can specify the name of an internal directory by passing in an `-n` or `internaldir` argument. To install a package without modifying any s, set `--nos`. Or to add _all_ subfolders in a package to the , set `--alls`.

pim keeps track of the packages it's downloaded in matlab preferences, within each installation directory.

Requirements
---------------

pim should work cross-platform on versions Matlab 2014b and later.
