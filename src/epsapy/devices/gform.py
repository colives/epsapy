#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.gform` module provides the gform class to model.
"""

import numpy as np
from shunt import Shunt


class GridFormer(Shunt):
    gf_id = 0
    
    def __init__(self, name, bus, v_ref, angle_a):
        super().__init__(name, bus)
        self.v_ref = v_ref
        self.angle_a = angle_a
        self.id = GridFormer.gf_id
        GridFormer.gf_id += 1
        