#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


def get_path():
    current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return current_path
