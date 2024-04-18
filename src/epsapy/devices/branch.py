#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.branch` module provides the branch class to model.
"""

class Branch(object):

    def __init__(self, name, bus_i, bus_j):
        self.name = name
        self.bus_i = bus_i
        self.bus_j = bus_j
        self.id = int(str(bus_i)+str(bus_j))