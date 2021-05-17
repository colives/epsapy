#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 11:09:46 2020

@author: carlosolives
"""

import epsapy

ieee4 = epsapy.System(50, 100e6, 3, 4)

ieee4.bus('bus0',230)
ieee4.bus('bus1',230)
ieee4.bus('bus2',230)
ieee4.bus('bus3',230)

ieee4.line('line1','bus0','bus1',['a','b','c','n'],1,1,1,1,1,1,1)

ieee4.gridformer('gf1', 'bus0', ['a','b','c','n'], 1.02, 0.0)