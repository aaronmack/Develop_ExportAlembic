#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import MyUtils

# Init data
data_dire = {"MAYA_BATCH_PATH": r"C:/Program Files/Autodesk/Maya2018/bin",
             "HOUDINI_INSTALL_PATH": r"C:/Program Files/Side Effects Software/Houdini 17.5.258/bin",
             }


class MyJsonConf(object):

    json_config_path = ""

    def __init__(self, path, default=1, force=0):
        self.json_config_path = path
        if default:
            self.data_dire = data_dire
            if force:
                self.store(self.data_dire)
        else:
            self.data_dire = {}
        MyUtils.DebugInfo(self.json_config_path, 'self.json_config_path', 0)

    @classmethod
    def setJsonConfigPath(cls, path):
        cls.json_config_path = path
        MyUtils.DebugInfo(cls.json_config_path, 'cls.json_config_path', 1)

    def update_config(self, config):
        with open(self.json_config_path, 'w') as json_file:
            json.dump(config, json_file, indent=4)
        return None

    def read_config(self):
        with open(self. json_config_path) as json_file:
            config = json.load(json_file)
        return config

    def store(self, data):
        with open(self.json_config_path, 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    def load(self):
        if not os.path.exists(self.json_config_path):
            with open(self.json_config_path, 'w') as json_file:
                pass
        with open(self.json_config_path) as json_file:
            try:
                data = json.load(json_file)
            except Exception, e:
                MyUtils.DebugInfo(e, 'json load file Exception', 1)
                MyUtils.DebugInfo('None json data', 'json load', 0)
                self.store(self.data_dire)

                data = json.load(json_file)
        MyUtils.DebugInfo(data, "Json data", 0)

        return data

    def set(self, data_dict):
        json_obj = self.load()
        for key in data_dict:
            json_obj[key] = data_dict[key]
        self.store(json_obj)
