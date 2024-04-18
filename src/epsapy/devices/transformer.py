#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.transformer` module provides the transformer class 
to model.
"""

import numpy as np
from branch import Branch


class Transformer(Branch):

    def __init__(self, name, bus_i, bus_j, r, x, v_inom, v_jnom, conn):
        super().__init__(name, bus_i, bus_j)
        self.v_inom = v_inom
        self.v_jnom = v_jnom
        self.conn = conn
