#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import inspect
import collections
import JsonConf as mjc


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


def get_subLevel1_dirsAndFiles(root_path):
    convered_root_path=convert_slash_type(root_path)
    root_depth = len(convered_root_path.split(os.path.sep))
    for root, dirs, files in os.walk(convered_root_path, topdown=True):
        for name in dirs:
            dir_path = os.path.join(root, name)
        return files, dirs


def fibList(n):
    i = 0
    while(i < n):
        yield (i)
        i += 1


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
    mayaExcutePath = MAYA_BATCH_PATH

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
    GenWinBat.getNeed(data_path, mayaExcutePath, curentSelect)

    # Execute scripts
    import subprocess
    import mypath
    # import win32api

    exe_cute = "\""+mypath.get_path()+os.sep+"data"+os.sep+"execute.bat"+"\""

    sub_obj = subprocess.Popen(exe_cute, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    DebugInfo(exe_cute, "ExeCute Command", 1)
    DebugInfo(sub_obj, "subprocess execute", 1)
    # except Exception, e:
    #     print("Error From Utils Export Alembic")
    #     print(e)

    return True


if __name__ == '__main__':
    pass
