@echo off
setlocal enabledelayedexpansion

REM --- Submodule Checkout Script ---
git submodule update --init --recursive

REM Loop through each submodule path and call a subroutine for each
for /f "tokens=2" %%s in ('git config --file .gitmodules --get-regexp path') do (
    if not "%%s"=="" call :update_submodule "%%s"
)
goto :after_submodules

:update_submodule
set "SUBMODULE=%~1"
echo Updating %SUBMODULE%
pushd %SUBMODULE%

git fetch --all --tags

REM Get latest tag
set "LATEST_TAG="
for /f "delims=" %%t in ('git tag --sort=-v:refname') do (
    if not defined LATEST_TAG set "LATEST_TAG=%%t"
)

if defined LATEST_TAG (
    echo Found latest tag: !LATEST_TAG!
    git checkout !LATEST_TAG!
) else (
    REM Get default branch name
    set "BRANCH="
    for /f "tokens=3" %%b in ('git remote show origin ^| findstr /c:"HEAD branch"') do (
        set "BRANCH=%%b"
    )
    if not defined BRANCH set "BRANCH=master"
    echo No tags found, checking out latest on !BRANCH!
    git checkout !BRANCH!
    git pull origin !BRANCH!
)

popd
exit /b

:after_submodules

REM Continue with your build steps...
echo 📋 Cleaning Output and Copying Default docs
python copy_packages.py
if %errorlevel% neq 0 (
    echo ❌ Error copying package docs
    exit /b 1
)

echo.
echo 📚 Building BAFF documentation...
python docs\generate_matlab_api.py
if %errorlevel% neq 0 (
    echo ❌ Error generating BAFF API files
    exit /b 1
)

sphinx-build -b html docs docs\build\html
if %errorlevel% neq 0 (
    echo ❌ Error building BAFF docs
    cd ..\..\..
    exit /b 1
)

echo.
echo ✅ Documentation build complete!
echo 📂 Output: build\html\index.html
pause