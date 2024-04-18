#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.generator` module provides the generator class
 to model.
"""
# excitacion T_e de 0.5 - 1 s
import numpy as np
from shunt import Shunt


class Generator(Shunt):
    gen_id = 0
    
    def __init__ (self, name, bus, p_max, p_min, q_max, q_min):
        super().__init__(name, bus)
        self.p_max = p_max
        self.p_min = p_min
        self.q_max = q_max
        self.q_min = q_min
        self.id = Generator.gen_id
        Generator.gen_id += 1
        