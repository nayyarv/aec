#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Varun Nayyar <nayyarv@gmail.com>"

import os

cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache"))

rawdir = os.path.join(cachedir, "data")
procdir = os.path.join(cachedir, "processedData")
