@echo off
setlocal enabledelayedexpansion

REM --- Submodule Checkout Script ---
echo 📚 initiilise submodules
git submodule update --init --recursive


echo.
echo Copy files to one matlab folder...
python copy_packages.py
if %errorlevel% neq 0 (
    echo ❌ Error copying doc files
    exit /b 1
)

echo.
echo 📚 Building documentation...
python doc_gen.py
if %errorlevel% neq 0 (
    echo ❌ Error generating API files
    exit /b 1
)

sphinx-autobuild docs docs\build\html
if %errorlevel% neq 0 (
    echo ❌ Error building documentation
    cd ..\..\..
    exit /b 1
)

echo.
echo ✅ Documentation build complete!
echo 📂 Output: build\html\index.html