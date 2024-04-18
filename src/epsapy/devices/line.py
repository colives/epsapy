#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.line` module provides the line class to model.
"""

import numpy as np
from branch import Branch


class Line(Branch):
    
    def __init__(self, name, bus_i, bus_j, nc, long, r_L, x_L, b_Li, g_Li, b_Lj, g_Lj):
        super().__init__(name, bus_i, bus_j)
        self.long = long
        self.r_L = r_L*long*np.eye(nc)
        self.x_L = x_L*long*np.eye(nc)
        self.b_Li = b_Li
        self.g_Li = g_Li
        self.b_Lj = b_Lj
        self.g_Lj = g_Lj
        z = np.vectorize(complex)(r_L, x_L)
        self.y_conn = 1/z
        self.y_sh_i = np.vectorize(complex)(g_Li, b_Li)
        self.y_sh_j = np.vectorize(complex)(g_Lj, b_Lj)