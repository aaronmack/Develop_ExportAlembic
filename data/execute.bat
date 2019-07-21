@echo off

set PYTHONPATH=C:\Google Drive\Dev\Houdini\python2.7libs\automation\data

set PATH=%PATH%;%PYTHONPATH%

set CURPATH=%cd%

set File="H:/HoudiniProject/Project/Test/XHQS_EP001_SC009_0037_ANI_V001.mb"

"C:/Program Files/Autodesk/Maya2018/bin/mayabatch.exe" -file %File%  -command "python(\"import execute\")"

exit