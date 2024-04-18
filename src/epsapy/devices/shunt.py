#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.shunt` module provides the shunt class to model.
"""

class Shunt(object):

    def __init__(self, name, bus):
        self.name = name
        self.bus = bus