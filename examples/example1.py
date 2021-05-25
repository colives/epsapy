#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example is based on Microgrid Islanding of European LV distribution 
network benchmark model
"""
import numpy as np
import epsapy
#  System
cigre_eu = epsapy.System(50, 100e6, 3, 4)

# Buses
cigre_eu.bus('busR0',  20e3/np.sqrt(3))
cigre_eu.bus('busR1',  230)
cigre_eu.bus('busR2',  230)
cigre_eu.bus('busR3',  230)
cigre_eu.bus('busR4',  230)
cigre_eu.bus('busR5',  230)
cigre_eu.bus('busR6',  230)
cigre_eu.bus('busR7',  230)
cigre_eu.bus('busR8',  230)
cigre_eu.bus('busR9',  230)
cigre_eu.bus('busR10', 230)
cigre_eu.bus('busR11', 230)
cigre_eu.bus('busR12', 230)
cigre_eu.bus('busR13', 230)
cigre_eu.bus('busR14', 230)
cigre_eu.bus('busR15', 230)
cigre_eu.bus('busR16', 230)
cigre_eu.bus('busR17', 230)
cigre_eu.bus('busR18', 230)

# Lines
cigre_eu.line('line1',' busR0', 'busR1', ['a','b','c','n'], 1, 1, 1, 1, 1, 1, 1)

# Generators
cigre_eu.gridformer('grid',  'busR0', ['a','b','c','n'], 20e3/np.sqrt(3), 0.00)
cigre_eu.gridformer('bat1',  'busR6', ['a','b','c','n'], 234.60, 0.00)
cigre_eu.gridformer('bat2', 'busR10', ['a','b','c','n'], 234.60, 0.00)

# 15 wt1
# 16 pv1
# 18 pv2

# Loads name, bus, phases, p_0, q_0, k_z, k_i, k_p)
cigre_eu.load('load1', 'busR11', ['a','b','c','n'], [ 850., 1700., 2295.], [ 526.78, 1053.57, 1422.31], 0.4, 0.3, 0.3)
cigre_eu.load('load2', 'busR15', ['a','b','c','n'], [4080., 5440., 6800.], [2528.56, 3371.41, 4214.26], 0.4, 0.3, 0.3)
cigre_eu.load('load3', 'busR16', ['a','b','c','n'], [4080., 5440., 6800.], [2528.56, 3371.41, 4214.26], 0.4, 0.3, 0.3)
cigre_eu.load('load4', 'busR17', ['a','b','c','n'], [   0.,    0., 2295.], [     0.,      0., 1422.31], 0.4, 0.3, 0.3)
cigre_eu.load('load5', 'busR18', ['a','b','c','n'], [1360., 2720., 3400.], [ 842.85, 1685.70, 2107.13], 0.4, 0.3, 0.3)

# Run Power Flow