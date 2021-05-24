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
cigre_eu.bus('busR0', 20e3/np.sqrt(3))
cigre_eu.bus('busR1', 230)
cigre_eu.bus('busR2', 230)
cigre_eu.bus('busR3', 230)
cigre_eu.bus('busR4', 230)
cigre_eu.bus('busR5', 230)
cigre_eu.bus('busR6', 230)
cigre_eu.bus('busR7', 230)
cigre_eu.bus('busR8', 230)
cigre_eu.bus('busR9', 230)
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
cigre_eu.line('line1','busR0','busR1',['a','b','c','n'],1,1,1,1,1,1,1)

# Generators
cigre_eu.gridformer('bat1', 'busR6', ['a','b','c','n'], 1.01, 0.00)

# Loads name, bus, phases, p_0, q_0, k_z, k_i, k_p)
cigre_eu.load('load1', 'busR11', ['a','b','c','n'], [ 850., 1700., 2295.], [ 526.78268764, 1053.56537529, 1422.31325664], 0.4, 0.3, 0.3)

# Run Power Flow