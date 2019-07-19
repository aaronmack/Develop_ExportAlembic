#!/usr/bin/python
# -*- coding: utf-8 -*-

# Need: 1.Current script directory 2. File name 3.maya execute file folder
import collections
import os
import mypath

def getNeed(tempPath, mayaExcutePath, curentSelect):
    win_bat = {}
    win_bat_list = []
    root_path = mypath.get_path()
    path = root_path+os.sep+"data/execute_template.bat"
    writePath = root_path+os.sep+"data/execute.bat"

    mayaExecutePro = ''
    if str(mayaExcutePath).endswith('/') or str(mayaExcutePath).endswith('\\'):
        mayaExecutePro += mayaExcutePath+'mayabatch.exe'
    else:
        mayaExecutePro += mayaExcutePath+'/mayabatch.exe'

    win_bat = collections.OrderedDict()

    win_bat['set_python_path'] = tempPath
    win_bat['set_file'] = curentSelect
    win_bat['command'] = mayaExecutePro


    fillSomeFile(path, writePath)

    replaceFromFile(writePath, "*__RE__PYPA__*", win_bat['set_python_path'])
    replaceFromFile(writePath, "*__RE__EXFI__*", win_bat['set_file'])
    replaceFromFile(writePath, "*__RE__MAEXFI__*", win_bat['command'])


def fillSomeFile(path, writePath):
    source = open(path, "r")
    desk = open(writePath, "w")

    while True:
        content = source.read(1024)
        if len(content) == 0:
            break
        desk.write(content)
    source.close()
    desk.close()


def replaceFromFile(file, mark, data):
    with open(file, 'r') as fr:
        read_lines = fr.readlines()
        with open(file, 'w') as fw:
            for line in read_lines:
                if mark in line:
                    line = line.replace(mark, data)
                    fw.write(line)
                else:
                    fw.write(line)

