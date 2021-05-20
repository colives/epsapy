#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example is based on European LV distribution network benchmark model
"""
import numpy as np
import epsapy
#  System
cigre_eu = epsapy.System(50, 100e6, 3, 4)

# Buses
cigre_eu.bus('bus0', 20e3/np.sqrt(3))
cigre_eu.bus('busR0', 20e3/np.sqrt(3))
cigre_eu.bus('busI0', 20e3/np.sqrt(3))
cigre_eu.bus('busC0', 20e3/np.sqrt(3))
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
cigre_eu.bus('busI1', 230)
cigre_eu.bus('busI2', 230)
cigre_eu.bus('busC1', 230)
cigre_eu.bus('busC2', 230)
cigre_eu.bus('busC3', 230)
cigre_eu.bus('busC4', 230)
cigre_eu.bus('busC5', 230)
cigre_eu.bus('busC6', 230)
cigre_eu.bus('busC7', 230)
cigre_eu.bus('busC8', 230)
cigre_eu.bus('busC9', 230)
cigre_eu.bus('busC10', 230)
cigre_eu.bus('busC11', 230)
cigre_eu.bus('busC12', 230)
cigre_eu.bus('busC13', 230)
cigre_eu.bus('busC14', 230)
cigre_eu.bus('busC15', 230)
cigre_eu.bus('busC16', 230)
cigre_eu.bus('busC17', 230)
cigre_eu.bus('busC18', 230)
cigre_eu.bus('busC19', 230)
cigre_eu.bus('busC20', 230)

# Lines
cigre_eu.line('line1','bus0','bus1',['a','b','c','n'],1,1,1,1,1,1,1)