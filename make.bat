@REM @echo off
@REM setlocal enabledelayedexpansion

@echo off
echo 🔄 Updating submodules...
git submodule update --init --recursive

REM Loop through each submodule using PowerShell
for /f "tokens=*" %%s in ('git config --file .gitmodules --get-regexp path ^| powershell -Command "$input | ForEach-Object { ($_ -split ' ')[1] }"') do (
    echo Updating %%s
    pushd %%s

    REM Fetch all tags and branches
    git fetch --all --tags

    REM Get the latest tag
    for /f %%t in ('powershell -Command "git tag --sort=-v:refname ^| Select-Object -First 1"') do (
        git checkout %%t 2>nul
        if errorlevel 1 (
            echo ❌ Checkout of tag %%t failed, falling back to default branch
            for /f %%d in ('powershell -Command "(git remote show origin) -match 'HEAD branch' -replace '.*: ', ''"') do git checkout origin/%%d
        ) else (
            echo Checked out latest tag: %%t
        )
        goto :done
    )

    REM If no tag was found, fallback to default branch
    echo No tags found, checking out default branch
    for /f %%d in ('powershell -Command "(git remote show origin) -match 'HEAD branch' -replace '.*: ', ''"') do git checkout origin/%%d

    :done
    popd
)

echo 📋 Cleaning Output and Copying Default docs
python copy_package_docs.py
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