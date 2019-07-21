#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class Houdini_Import_Alembic_FromDisk(object):
    def __init__(self, path):
        super(Houdini_Import_Alembic_FromDisk, self).__init__()
        self.source_path = path

    def getList(self):
        alembic_file_path = self.source_path
        ale_list = os.listdir(alembic_file_path)
        ale_lists = []
        ale_path_dir = {}
        for x in ale_list:
            j = alembic_file_path + os.sep + x
            if os.path.isdir(j):
                ale_path_dir[x] = j
            else:
                ale_lists.append(x)
        dir_path = os.path.abspath(alembic_file_path)

        return ale_lists, ale_path_dir, dir_path

