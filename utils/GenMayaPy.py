#!/usr/bin/python
# -*- coding: utf-8 -*-

import MyUtils
import os
import JsonConf
import mypath


class GeneratePyFileByJson(object):
    def __init__(self):
        root_path = mypath.get_path()
        self.path1 = os.path.abspath(root_path+os.sep+"data/re_sub1.py")
        self.path2 = os.path.abspath(root_path+os.sep+"data/re_sub2.py")
        self.path3 = os.path.abspath(root_path+os.sep+"data/re_sub3.py")

        self.merged_path = os.path.abspath(root_path+os.sep+'data/execute.py')
        self.filenames = [self.path1, self.path2, self.path3]
        self.json_conf = JsonConf.MyJsonConf(root_path+os.sep+'utils/export_options.json').load()
        globals().update(self.json_conf)

    @staticmethod
    def typeof(variate):
        t_type = None
        if isinstance(variate, int):
            t_type = "int"
        elif isinstance(variate, str):
            t_type = "str"
        elif isinstance(variate, float):
            t_type = "float"
        elif isinstance(variate, list):
            t_type = "list"
        elif isinstance(variate, tuple):
            t_type = "tuple"
        elif isinstance(variate, dict):
            t_type = "dict"
        elif isinstance(variate, set):
            t_type = "set"
        return t_type

    @staticmethod
    def getType(variate):
        arr = {"int": "integer", "float": "floating", "str": "String",
               "list": "list", "tuple": "tuple", "dict": "Dictionary", "set": "set"}
        vartype = GeneratePyFileByJson.typeof(variate)
        if not (vartype in arr):
            return "Unknown"
        return arr[vartype]

    def run(self):
        with open(self.path2, 'w') as f:
            f.write("# ################################## Sub2 ############################################### #\n")
            for k, v in self.json_conf.items():
                MyUtils.DebugInfo(GeneratePyFileByJson.getType(v), "getFileType", 0)
                if GeneratePyFileByJson.getType(v) in ("integer", "list"):
                    f.write(str(k) + ' = ' + str(v) + '\n')
                elif GeneratePyFileByJson.getType(v) == "String":
                    f.write(str(k) + ' = \"' + str(v) + '\"\n')
                else:
                    f.write(str(k) + ' = \"' + str(v) + '\"\n')
            f.write("\n")

    def writeMerge(self):
        MyUtils.mergeFiles(self.filenames, self.merged_path)


if __name__ == '__main__':
    gpfbj = GeneratePyFileByJson()
    gpfbj.run()
    gpfbj.writeMerge()

