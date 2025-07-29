#!/usr/bin/env python3
"""
Package Copier for DCRG Documentation

This script reads a list of package directories from 'packageList.csv' and
copies their tbx/* contents into a unified 'tbxs' directory structure.

Usage:
    python copy_packages.py

File format for packageList.csv:
    Each line should contain a relative path to a package directory
    that contains a 'tbx' subdirectory.
    
    Example packageList.csv:
        Package,autogen
        external/baff,1
        external/ads,1
"""

import csv
import os
import shutil
import sys
from pathlib import Path

# Configuration
PACKAGE_LIST_FILE = 'packageList.csv'
OUTPUT_DIR = 'tbxs'

def read_package_list():
    """Read the package list from packageList.csv, ignoring the header row.
    Returns a list of (package_path, tbx_folder) tuples where tbx_folder != "0".
    """
    if not os.path.exists(PACKAGE_LIST_FILE):
        print(f"❌ Error: {PACKAGE_LIST_FILE} not found!")
        print(f"Please create {PACKAGE_LIST_FILE} with a header and one package path per line.")
        print("Example content:")
        print("  Package,autogen")
        print("  external/baff,tbx")
        print("  external/ads,tbx")
        return None

    packages = []
    try:
        with open(PACKAGE_LIST_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header row
            for row in reader:
                if not row or not row[0].strip() or row[0].strip().startswith('#'):
                    continue
                package_path = row[0].strip()
                tbx_folder = row[1].strip() if len(row) > 1 else "tbx"
                if tbx_folder == "0":
                    continue
                packages.append((package_path, tbx_folder))
    except Exception as e:
        print(f"❌ Error reading {PACKAGE_LIST_FILE}: {e}")
        return None

    return packages

def validate_package(package_path, tbx_folder):
    """Validate that a package directory exists and has the specified subdirectory."""
    if not os.path.exists(package_path):
        print(f"⚠️  Warning: Package directory '{package_path}' not found")
        return False

    tbx_path = os.path.join(package_path, tbx_folder)
    if not os.path.exists(tbx_path):
        print(f"⚠️  Warning: No '{tbx_folder}' directory found in '{package_path}'")
        return False

    return True

def copy_package_contents(package_path, tbx_folder, output_dir):
    """Copy contents of package/{tbx_folder}/* to output_dir."""
    tbx_path = os.path.join(package_path, tbx_folder)
    package_name = os.path.basename(package_path)

    print(f"  📦 Processing {package_name} ({tbx_folder})...")

    # Get all items in the tbx directory
    try:
        tbx_items = os.listdir(tbx_path)
    except OSError as e:
        print(f"    ❌ Error reading {tbx_path}: {e}")
        return False

    copy_count = 0
    for item in tbx_items:
        source_item = os.path.join(tbx_path, item)
        dest_item = os.path.join(output_dir, item)

        try:
            if os.path.isdir(source_item):
                # Copy directory
                if os.path.exists(dest_item):
                    print(f"    ⚠️  Destination '{item}' already exists, skipping")
                    continue
                shutil.copytree(source_item, dest_item)
                print(f"    ✅ Copied directory: {item}")
                copy_count += 1
            else:
                # Copy file
                if os.path.exists(dest_item):
                    print(f"    ⚠️  File '{item}' already exists, skipping")
                    continue
                shutil.copy2(source_item, dest_item)
                print(f"    ✅ Copied file: {item}")
                copy_count += 1
        except Exception as e:
            print(f"    ❌ Error copying '{item}': {e}")
            continue

    print(f"    📊 Copied {copy_count} items from {package_name}")
    return copy_count > 0

def main():
    """Main function."""
    print("🚀 DCRG Package Copier")
    print("=" * 30)

    # Read package list
    packages = read_package_list()
    if not packages:
        return 1

    print(f"📋 Found {len(packages)} packages in {PACKAGE_LIST_FILE}")

    # Validate packages
    valid_packages = []
    for package_path, tbx_folder in packages:
        if validate_package(package_path, tbx_folder):
            valid_packages.append((package_path, tbx_folder))

    if not valid_packages:
        print("❌ No valid packages found!")
        return 1

    print(f"✅ {len(valid_packages)} valid packages found")

    # Create/clean output directory
    if os.path.exists(OUTPUT_DIR):
        print(f"🧹 Cleaning existing {OUTPUT_DIR} directory...")
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 Created {OUTPUT_DIR} directory")

    # Copy packages
    print(f"📦 Copying packages to {OUTPUT_DIR}...")
    success_count = 0

    for package_path, tbx_folder in valid_packages:
        if copy_package_contents(package_path, tbx_folder, OUTPUT_DIR):
            success_count += 1

    # Summary
    print("\n" + "=" * 40)
    print(f"📊 Copy Summary:")
    print(f"   Total packages: {len(packages)}")
    print(f"   Valid packages: {len(valid_packages)}")
    print(f"   Successfully copied: {success_count}")

    if success_count > 0:
        print(f"\n✅ Package copying completed!")
        print(f"📁 All package contents are now in: {OUTPUT_DIR}")

        # List what was copied
        try:
            copied_items = os.listdir(OUTPUT_DIR)
            if copied_items:
                print(f"\n📦 Copied items:")
                for item in sorted(copied_items):
                    item_path = os.path.join(OUTPUT_DIR, item)
                    if os.path.isdir(item_path):
                        print(f"   📂 {item}/")
                    else:
                        print(f"   📄 {item}")
        except OSError:
            pass

        return 0
    else:
        print(f"\n❌ No packages were successfully copied!")
        return

if __name__ == "__main__":
    sys.exit(main())