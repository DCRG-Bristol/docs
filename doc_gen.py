import csv
import os
from collections import defaultdict
import shutil

MATLAB_SRC_DIR = 'tbxs'
DOCS_DIR = 'docs'
API_DIR = os.path.join(DOCS_DIR, 'api')

def is_class_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('%')]
            return lines[0].startswith('classdef') if lines else False
    except Exception:
        return False


def is_function_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('%')]
            return lines[0].startswith('function') if lines else False
    except Exception:
        return False

def find_matlab_items(package_dir):
    class_map = defaultdict(set)
    function_map = defaultdict(set)
    seen_class_folders = set()

    for root, dirs, files in os.walk(package_dir):
        rel_path = os.path.relpath(root, package_dir)
        domain_parts = rel_path.split(os.sep) if rel_path != '.' else []
        in_class_folder = any(part.startswith('@') for part in domain_parts)

        domain_list = [part[1:] for part in domain_parts if part.startswith('+')]
        domain = '.'.join(domain_list)

        if in_class_folder:
            continue

        for d in dirs:
            if d.startswith('@'):
                class_name = d[1:]
                seen_class_folders.add((domain, class_name.lower()))
                class_map[domain].add(class_name)

        for file in files:
            if file.endswith('.m') and not file.startswith('.'):
                full_path = os.path.join(root, file)
                item_name = file[:-2]

                if is_class_file(full_path):
                    if (domain, item_name.lower()) not in seen_class_folders:
                        class_map[domain].add(item_name)
                elif is_function_file(full_path):
                    function_map[domain].add(item_name)

    return class_map, function_map


def get_full_qualified_name(root_package, subpackage, name):
    if subpackage:
        return f"+{root_package}" + ''.join([f".+{p}" for p in subpackage.split('.')]) + f".{name}"
    return f"+{root_package}.{name}"


def find_class_readme_file(package_dir, subpackage, class_name):
    parts = [f'+{p}' for p in subpackage.split('.')] if subpackage else []
    class_dir = os.path.join(package_dir, *parts, f'@{class_name}')
    if not os.path.exists(class_dir):
        return None
    for file in os.listdir(class_dir):
        if file.lower() == 'readme.rst':
            return os.path.join(class_dir, file)
    return None


def include_readme_content(f, path):
    try:
        with open(path, 'r', encoding='utf-8') as readme:
            content = readme.read().strip()
            if content:
                f.write("Overview\n--------\n\n")
                f.write(content + "\n\n")
    except Exception as e:
        print(f"⚠️  Could not read {path}: {e}")


def write_class_rst(subpackage, class_name, package_dir, root_package):
    # Place all files for each submodule in docs/api/{package}/...
    base_dir = os.path.join(API_DIR, root_package)
    sub_dir = os.path.join(base_dir, subpackage.replace('.', os.sep)) if subpackage else base_dir
    os.makedirs(sub_dir, exist_ok=True)
    path = os.path.join(sub_dir, f'{class_name.lower()}.rst')
    full_name = get_full_qualified_name(root_package, subpackage, class_name)
    readme = find_class_readme_file(package_dir, subpackage, class_name)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"{class_name} class\n")
        f.write("=" * (len(class_name) + 7) + "\n\n")
        if readme:
            include_readme_content(f, readme)
        f.write(f".. mat:autoclass:: {full_name}\n   :members:\n   :undoc-members:\n   :show-inheritance:\n")
    return class_name.lower()


def write_function_rst(subpackage, func_name, root_package):
    # Place all files for each submodule in docs/api/{package}/...
    base_dir = os.path.join(API_DIR, root_package)
    sub_dir = os.path.join(base_dir, subpackage.replace('.', os.sep)) if subpackage else base_dir
    os.makedirs(sub_dir, exist_ok=True)
    path = os.path.join(sub_dir, f'{func_name.lower()}.rst')
    full_name = get_full_qualified_name(root_package, subpackage, func_name)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"{func_name} function\n")
        f.write("=" * (len(func_name) + 10) + "\n\n")
        f.write(f".. mat:autofunction:: {full_name}\n")
    return func_name.lower()


def find_readme_file(package_dir, subpackage):
    parts = [f'+{p}' for p in subpackage.split('.')] if subpackage else []
    pkg_path = os.path.join(package_dir, *parts)
    if not os.path.exists(pkg_path):
        return None
    for file in os.listdir(pkg_path):
        if file.lower() == 'readme.rst':
            return os.path.join(pkg_path, file)
    return None


def write_subpackage_index(subpackage, classes, functions, all_subpackages, package_dir, root_package):
    # Place all files for each submodule in docs/api/{package}/...
    base_dir = os.path.join(API_DIR, root_package)
    sub_dir = os.path.join(base_dir, subpackage.replace('.', os.sep)) if subpackage else base_dir
    os.makedirs(sub_dir, exist_ok=True)
    path = os.path.join(sub_dir, 'index.rst')
    title = f"{root_package}.{subpackage}" if subpackage else f"{root_package}"
    readme = find_readme_file(package_dir, subpackage)
    children = [pkg.split('.')[-1] for pkg in all_subpackages if pkg.startswith(subpackage + '.') and '.' not in pkg[len(subpackage)+1:]] if subpackage else [pkg for pkg in all_subpackages if '.' not in pkg]
    children.sort()

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n")
        f.write("=" * len(title) + "\n\n")
        if readme:
            include_readme_content(f, readme)
        if children:
            f.write("\n.. toctree::\n   :maxdepth: 1\n   :caption: Subpackages\n\n")
            for child in children:
                if child:
                    f.write(f"   {child}/index\n")
            f.write("\n")
        if classes:
            f.write("\n.. toctree::\n   :maxdepth: 1\n   :caption: Classes\n\n")
            for name in sorted(classes):
                f.write(f"   {name}\n")
            f.write("\n")
        if functions:
            f.write("\n.. toctree::\n   :maxdepth: 1\n   :caption: Functions\n\n")
            for name in sorted(functions):
                f.write(f"   {name}\n")
            f.write("\n")

def print_summary(class_map, function_map):
    total_classes = sum(len(v) for v in class_map.values())
    total_functions = sum(len(v) for v in function_map.values())
    all_packages = set(class_map.keys()) | set(function_map.keys())
    print("\n📊 Summary")
    print("=" * 40)
    print(f"Total Classes: {total_classes}\nTotal Functions: {total_functions}\nTotal Packages: {len(all_packages)}")
    for pkg in sorted(all_packages, key=lambda x: (x.count('.'), x)):
        print(f"  📦 {pkg or '[root]'}: {len(class_map.get(pkg, []))} classes, {len(function_map.get(pkg, []))} functions")


def detect_root_packages():
    if not os.path.isdir(MATLAB_SRC_DIR):
        print(f"❌ Error: MATLAB source directory '{MATLAB_SRC_DIR}' not found!")
        return []
    return [item[1:] for item in os.listdir(MATLAB_SRC_DIR)
            if item.startswith('+') and os.path.isdir(os.path.join(MATLAB_SRC_DIR, item))]


def extract_overviews_to_docs(root_package):
    """
    Copy tbxs/+{package}/docs/overview.rst to docs/overviews/{package}.rst.
    If overview.rst does not exist, create a blank one in docs/overviews.
    """
    overviews_dir = os.path.join(DOCS_DIR, "overviews")
    os.makedirs(overviews_dir, exist_ok=True)
    src = os.path.join(MATLAB_SRC_DIR, f'+{root_package}', 'docs', 'overview.rst')
    dst = os.path.join(overviews_dir, f'{root_package}.rst')
    if os.path.exists(src):
        with open(src, 'r', encoding='utf-8') as fsrc, open(dst, 'w', encoding='utf-8') as fdst:
            fdst.write(fsrc.read())
    else:
        with open(dst, 'w', encoding='utf-8') as fdst:
            title = f"{root_package.upper()} Documentation\n"
            fdst.write(title)
            fdst.write("=" * len(title))

def process_package(root_pkg):
    print(f"\n🔍 Processing package: +{root_pkg}")
    package_path = os.path.join(MATLAB_SRC_DIR, f'+{root_pkg}')
    class_map, function_map = find_matlab_items(package_path)
    all_subpackages = set(['']) | set(class_map.keys()) | set(function_map.keys())

    for subpackage in all_subpackages:
        classes = class_map.get(subpackage, set())
        functions = function_map.get(subpackage, set())
        class_rst_files = [write_class_rst(subpackage, cls, package_path, root_pkg) for cls in classes]
        function_rst_files = [write_function_rst(subpackage, func, root_pkg) for func in functions]
        write_subpackage_index(subpackage, class_rst_files, function_rst_files, all_subpackages, package_path, root_pkg)

    print_summary(class_map, function_map)
    return all_subpackages

def write_top_index(overview_pkgs,root_packages):
    """
    Write the top-level index.rst with a section for package overviews and a section for API references.
    """
    path = os.path.join(DOCS_DIR, 'index.rst')
    with open(path, 'a', encoding='utf-8') as f:
        # Section: Package Overviews
        f.write("\n.. toctree::\n   :maxdepth: 1\n   :caption: Package Overviews\n\n")
        for pkg in overview_pkgs:
            f.write(f"   overviews/{pkg}/index\n")
        f.write("\n")

        # Section: API References
        f.write(".. toctree::\n   :maxdepth: 1\n   :caption: API References\n\n")
        for (pkg,subPkgs) in root_packages:
            f.write(f"   api/{pkg}/index\n")

def get_packages_from_csv(csv_path):
    """Return a list of package names from csv where autogen != '0'."""
    packages = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if not row or not row[0].strip() or row[0].strip().startswith('#'):
                continue
            package = row[0].strip().split('/')[-1]
            packages.append(package)
    return packages

def clean_docs_folder():
    """
    Remove all files and folders in the docs directory, and copy contents of source folder.
    """
    for item in os.listdir(DOCS_DIR):
        item_path = os.path.join(DOCS_DIR, item)
        if os.path.isdir(item_path):
            # Remove directory and all contents
            import shutil
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    shutil.copytree('source', DOCS_DIR, dirs_exist_ok=True)

def extract_pkg_docs_to_docs(package):
    """
    Copy tbxs/+{package}/docs/overview.rst to docs/overviews/{package}.rst.
    If overview.rst does not exist, create a blank one in docs/overviews.
    """
    overviews_dir = os.path.join(DOCS_DIR, "overviews")
    os.makedirs(overviews_dir, exist_ok=True)
    src = os.path.join('external',package, 'docs')
    dst = os.path.join(DOCS_DIR, "overviews",package)
    if not os.path.exists(dst):
        os.makedirs(dst, exist_ok=True)
    # copy contents of src to dst
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    indexFile = os.path.join(dst, 'index.rst')
    if not os.path.exists(indexFile):
        print(f"⚠️  Warning: No index File found in directory '{src}'. Creating a blank one.")
        with open(indexFile, 'w', encoding='utf-8') as f:
            t = f"{package.upper()} Documentation\n"
            f.write(t)
            f.write("=" * len(t) + "\n\n")
            f.write(f"This is the overview documentation for the package {package}.\n\n")
   
    
if __name__ == '__main__':
    clean_docs_folder()
    # Get packages from CSV
    PACKAGE_LIST_FILE = 'packageList.csv'
    if not os.path.exists(PACKAGE_LIST_FILE):
        print(f"❌ Error: Package list file '{PACKAGE_LIST_FILE}' not found!")
        print("Please ensure it exists in the current directory.")
        exit(1)
    OverviewPkgs = get_packages_from_csv(PACKAGE_LIST_FILE)
    # copy external/{package}/docs folder into docs/overviews/{package}/
    if not OverviewPkgs:
        print("⚠️ No packages found in packageList.csv. Skipping documentation generation.")
        exit(0)
    for package in OverviewPkgs:
        extract_pkg_docs_to_docs(package)
    
    # Generate auto-gen documentation
    root_packages = detect_root_packages()
    if not root_packages:
        print("⚠️ No valid MATLAB packages found. Skipping documentation generation.")
        exit(0)
    pkgs = list()
    for root_pkg in root_packages:
        # Ensure overview.rst exists for each package
        subPkgs = process_package(root_pkg)
        pkgs.append((root_pkg,subPkgs))
    write_top_index(OverviewPkgs,pkgs)
    print("\n✅ Documentation generated for all packages!")