.PHONY: all submodules copy-packages doc-gen html

all: html

submodules:
	@echo "📚 initialise submodules"
	git submodule update --init --recursive

copy-packages: submodules
	@echo "Copy files to one matlab folder..."
	python copy_packages.py

doc-gen: copy-packages
	@echo "📚 Building documentation..."
	python doc_gen.py

html: doc-gen
	@echo "Building Sphinx HTML documentation..."
	python -m sphinx -b html docs $(READTHEDOCS_OUTPUT)/html
	@echo "✅ Documentation build complete!"
	@echo "📂 Output: $(READTHEDOCS_OUTPUT)/html/index.html"