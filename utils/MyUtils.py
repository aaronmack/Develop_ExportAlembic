#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import inspect
import collections
# import shlex
import subprocess
import time
import JsonConf as mjc


class PathIrregularError(Exception):
    pass


def judge_yes_or_no_houdini():
    try:
        # Use try import hou module to determine if the current operating environment is Houdini
        import hou
        return True
    except Exception:
        return False


if judge_yes_or_no_houdini():
    GLOBAL_HOUDINI = 1
else:
    GLOBAL_HOUDINI = 0


def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


def DebugInfo(info, theMessageFrom='', show=1):
    if show:
        print("Debug Info: -- %s -- %s" % (theMessageFrom, info))
    else:
        pass


def file_extension(path):
    return os.path.splitext(path)[-1]


def get_depth(path, depth=0):
    if not os.path.isdir(path): return depth
    maxdepth = depth
    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        maxdepth = max(maxdepth, get_depth(fullpath, depth + 1))
    return maxdepth


def get_directory_structure(startpath):
    max_depth = get_depth(startpath)
    mul_list_dict = collections.defaultdict(list)

    for root, dir_list, file_list in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        for dir_name in dir_list:
            print(os.path.join(root, dir_name))
            print(level)
            item = "list"+bytes(level)
            mul_list_dict[item].append(dir_name)
    print ("The initialized lists are : ")
    print ("List 1 : " + str(mul_list_dict['list0']))
    print ("List 2 : " + str(mul_list_dict['list1']))
    print ("List 3 : " + str(mul_list_dict['list2']))
    print ("List 4 : " + str(mul_list_dict['list3']))


def convert_slash_type(data, double=False):

    # find slash type
    if data.find('/') != -1:
        str_temp = data.replace('/', '\\')
        return str_temp
    if data.find('\\') != -1:
        str_temp = data.replace('\\', '\\')
        return str_temp


def convert_slash_type_to_backslash(data):
    if data.find('/') != -1:
        str_temp = data.replace('/', "\\")
        return str_temp

def convert_slash_type_to_backslash_from_front(data):
    if data.find('\\') != -1:
        str_temp = data.replace('\\', "\\\\")
        return str_temp


def get_previous_level_path(path):
    if os.path.exists(path):
        previous_path = os.path.abspath(os.path.join(path, os.pardir))
    else:
        raise NameError("The path is inexistence")
    return previous_path


def get_subLevel1_dirsAndFiles(root_path):
    convered_root_path=convert_slash_type(root_path)
    root_depth = len(convered_root_path.split(os.path.sep))
    for root, dirs, files in os.walk(convered_root_path, topdown=True):
        for name in dirs:
            dir_path = os.path.join(root, name)
        return files, dirs


def checkAbcPath(exportPath):
    if not exportPath.endswith('abc'):
        exportPath += os.sep + "abc"
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
    else:
        pass
    DebugInfo(exportPath, "exportPath before", 0)
    exportPath = convert_slash_type_to_backslash_from_front(exportPath)
    DebugInfo(exportPath, "exportPath after", 0)
    return exportPath


def fibList(n):
    i = 0
    while(i < n):
        yield (i)
        i += 1


def fun_call(*popenargs, **kwargs):
    if GLOBAL_HOUDINI:
        subprocess.Popen(*popenargs, shell=True)
        return
    cal_obj = subprocess.Popen(*popenargs, shell=True, stdout=subprocess.PIPE, **kwargs)
    output, unused_err = cal_obj.communicate()
    retcode = cal_obj.poll()

    if retcode:
        cmd = kwargs.get("args")
        raise subprocess.CalledProcessError(retcode, cmd)
    return retcode


def mergeFiles(files, merged_path):
    filenames = files
    with open(merged_path, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


def mayaExportAbc(thatAllNeed, curentSelect):
    """The main idea:
        1. Exported directory (abs subdirectory under the current Houdini project directory)
        2. Export the Maya script file to be executed, bat batch command, vbs hide cmd window command, and put it in the temp directory.
        3. Need to dynamically generate bat mayapy and vbs commands"""
    #try:
    import mypath
    currentPathFatherFolder = mypath.get_path()

    data_path = currentPathFatherFolder+os.sep+'data'
    tempPath = os.getenv('TEMP')

    DebugInfo(currentPathFatherFolder, "currentPathFatherFolder", 0)
    DebugInfo(tempPath, "tempPath", 0)
    DebugInfo(thatAllNeed, "AllThatIsNeeded", 0)

    js_options_path = currentPathFatherFolder+os.sep+"utils/export_options.json"
    js_config_path = currentPathFatherFolder+os.sep+"utils/config.json"
    UtilsJS_Options = mjc.MyJsonConf(js_options_path, default=0, force=0)
    UtilsJS_Config = mjc.MyJsonConf(js_config_path, default=0, force=0)

    json_config = UtilsJS_Config.load()

    # Convert the dictionary to a variable
    globals().update(json_config)
    DebugInfo(json_config, 'JsonConf', 0)

    # Set Ready Generated config json
    UtilsJS_Options.set(thatAllNeed)
    DebugInfo('Set All', 'From Utils', 0)

    # Generated maya execute .py file
    import GenMayaPy as Gen
    GenObj = Gen.GeneratePyFileByJson()
    GenObj.run()
    GenObj.writeMerge()

    # Generated windows execute .bat file
    import GenWinBat
    GenWinBat.getNeed(data_path, MAYA_BATCH_PATH, curentSelect)

    # Execute scripts
    import mypath
    # import win32api

    exe_cute = "\""+mypath.get_path()+os.sep+"data"+os.sep+"execute.bat"+"\""
    if GLOBAL_HOUDINI:
        os.environ['PYTHONHOME'] = MAYA_PYTHON_HOME
    else:
        pass
    sub_obj = fun_call(exe_cute)

    DebugInfo(MAYA_PYTHON_HOME, "MAYA_PYTHON_HOME", 0)
    DebugInfo(exe_cute, "ExeCute Command", 0)
    DebugInfo(sub_obj, "subprocess execute", 0)
    # par.event_notice()

    # except Exception, e:
    #     print("Error From Utils Export Alembic")
    #     print(e)

    return True


def get_windows_dekstopFolder():
    import _winreg
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    win_desktop_directory_path = _winreg.QueryValueEx(key, "Desktop")[0]
    return win_desktop_directory_path


if __name__ == '__main__':
    pass
