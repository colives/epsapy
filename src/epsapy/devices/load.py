#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.load` module provides the load class to model.
"""

import numpy as np
from shunt import Shunt


class Load(Shunt):
    load_id = 0
    
    def __init__(self, name, bus, p_0, q_0, k_z, k_i, k_p):
        super().__init__(name, bus)
        self.id = Load.load_id
        self.p_0 = p_0
        self.q_0 = q_0
        self.k_z = k_z        
        self.k_i = k_i
        self.k_p = k_p
        Load.load_id += 1
        