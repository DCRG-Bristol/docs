@echo off
setlocal enabledelayedexpansion

echo 🔄 Updating submodules...
git submodule update --init --recursive
if %errorlevel% neq 0 (
    echo ❌ Error updating submodules
    exit /b 1
)

echo.
echo 📦 Installing BAFF documentation requirements...
cd external\baff
pip install -r docs\docRequirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error installing BAFF requirements
    cd ..\..
    exit /b 1
)

echo.
echo 📚 Building BAFF documentation...
cd external\baff
python docs\generate_matlab_api.py
if %errorlevel% neq 0 (
    echo ❌ Error generating BAFF API files
    cd ..\..\..
    exit /b 1
)

sphinx-build -b html docs docs\build\html
if %errorlevel% neq 0 (
    echo ❌ Error building BAFF docs
    cd ..\..\..
    exit /b 1
)
cd ..\..

echo.
echo 📚 Building ADS documentation...
REM cd external\ads\docs  
REM python generate_matlab_api.py
REM if %errorlevel% neq 0 (
REM     echo ❌ Error generating ADS API files
REM     cd ..\..\..
REM     exit /b 1
REM )
REM sphinx-build -b html . build\html
REM if %errorlevel% neq 0 (
REM     echo ❌ Error building ADS docs
REM     cd ..\..\..
REM     exit /b 1
REM )
REM cd ..\..\..

echo.
echo 📋 Copying built docs to main site...
if not exist "source\_static" mkdir _static
if not exist "source\_static\baff_docs" mkdir _static\baff_docs
xcopy /E /I /Y external\baff\docs\build\html\* source\_static\baff_docs\
if %errorlevel% neq 0 (
    echo ❌ Error copying BAFF docs
    exit /b 1
)

REM if not exist "source\_static\ads_docs" mkdir source\_static\ads_docs
REM xcopy /E /I /Y external\ads\docs\build\html\* source\_static\ads_docs\

echo.
echo 🏗️ Building main documentation...
sphinx-autobuild source build\html
if %errorlevel% neq 0 (
    echo ❌ Error building main documentation
    exit /b 1
)

echo.
echo ✅ Documentation build complete!
echo 📂 Output: build\html\index.html
pause