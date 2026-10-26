@ECHO OFF

pushd "%~dp0"

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=uv run sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The documentation command was not found. Install uv and run
	echo.uv sync --locked from the project root before building the documentation.
	echo.
	echo.Uv installation instructions:
	echo.https://docs.astral.sh/uv/getting-started/installation/
	popd
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

:end
popd
