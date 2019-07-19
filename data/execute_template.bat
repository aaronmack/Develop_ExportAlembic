@echo off

set PYTHONPATH=*__RE__PYPA__*

set PATH=%PATH%;%PYTHONPATH%

set CURPATH=%cd%

set File="*__RE__EXFI__*"

"*__RE__MAEXFI__*" -file %File%  -command "python(\"import execute\")"

exit