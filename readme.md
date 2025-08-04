# DCRG Documentation Build
Build project to create DCRG documentation, which is hoted at

https://dcrgdocs.readthedocs.io/en/latest/

# Updating the documentation links
To update the pacakge links, the latest commits have to be set in the submodules. Run the script `update_submodules.py` to update each of the submodules to the latest commit on the `master` branch.

# Active development

run `python update_submodules.py` to update to the latest commits on each submodule

run `pip install -r requirments.txt` to install dependencies

run `sphinx-autobuild source build/html` to host a local, auto-updating, set of the docs

push changes to the master branch to trigger a build of the readthedocs domain.