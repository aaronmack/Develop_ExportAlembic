#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class Houdini_Import_Alembic_FromDisk(object):
    def __init__(self, path):
        self.source_path = path

    def getList(self):
        ale_list = os.listdir(self.source_path)
        ale_lists = []
        dir_lists = []
        ale_path_dir = {}
        for x in ale_list:
            j = self.source_path + os.sep + x
            if os.path.isdir(j):
                ale_path_dir[x] = j
                dir_lists.append(x)
            elif os.path.isfile(j):
                ale_lists.append(x)
            else:
                raise NameError('unknown error')
        dir_path = os.path.abspath(self.source_path)

        return ale_lists, dir_lists, ale_path_dir, dir_path


if __name__ == '__main__':
    pass
