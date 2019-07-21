@echo off

set PYTHONPATH=C:\Google Drive\Dev\Houdini\python2.7libs\automation\data

set PATH=%PATH%;%PYTHONPATH%

set CURPATH=%cd%

set File="C:/Google Drive/Dev/Houdini/python2.7libs/other/ExportTest/Test_02.mb"

"G:/Program Files/Autodesk/Maya2018/bin/mayabatch.exe" -file %File%  -command "python(\"import execute\")"

exit