#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of epsapy
#
# epsapy is free software: you can redistribute it and/or modify it under the
# terms of the MIT License.
#
# epsapy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY.
"""
The :mod:`~epsapy.elements` module provides basic classes to build the
power flow problem.
"""

import string
import numpy as np
from bus import Node, Bus
from branch import Branch
from shunt import Shunt
from line import Line
from transformer import Transformer
from load import Load
from gform import GridFormer
from generator import Generator
from turbine import Turbine
from governor import Governor
from agc import AGC
from avr import AVR
from pss import PSS


class System(object):
    
    intfloat = [type(1), type(1.), type(np.sqrt(3))]
    
    def __init__(self,freq,s_b,num_phs,num_cond):
        assert type(freq) in self.intfloat, 'freq must be '+str(self.intfloat[0])+' or '+str(self.intfloat[1])
        assert type(s_b) in self.intfloat, 's_b must be '+str(self.intfloat[0])+' or '+str(self.intfloat[1])
        assert type(num_phs) == self.intfloat[0], 'num_phs must be '+str(self.intfloat[0])
        assert type(num_cond) == self.intfloat[0], 'num_cond must be '+str(self.intfloat[0])
        self.freq = freq
        self.s_b = s_b
        self.num_phs = num_phs
        self.num_cond = num_cond
        self.phases = [string.ascii_lowercase[i] for i in range(num_phs)]
        _all = self.phases + ['n','gr']
        self.conds = [_all[i] for i in range(num_cond)]
        self.elmts = {'Buses': {}, 'Lines': {}, 'Transformers': {}, 'Grid Formers':{}, 'Generators': {}, 'Loads': {}, 'Shunts':{}}
        self.info  = {'Buses': {}, 'Lines': {}, 'Transformers': {}, 'Grid Formers':{}, 'Generators': {}, 'Loads': {}, 'Shunts':{}}
        self.conns = dict()
        self.n = 0
        
    def __str__(self):
        return '< freq: '+str(self.freq)+'; s_base: '+str(self.s_b)+'; conds: '+str(self.conds)+'; elements: '+ str(self.info)+' >'
        
    def new_element(self,key,value):
        elmt = value
        self.elmts[key][elmt.id] = elmt
        self.info[key][elmt.name] = elmt
        return elmt.id
    
    def bus(self,name,v_b):
        assert type(v_b) in self.intfloat, 'v_b must be '+str(self.intfloat[0])+' or '+str(self.intfloat[1])
        bus = System.new_element(self,'Buses', Bus(name, v_b, self.conds))
        self.elmts['Buses'][bus].v = self.set_v(1.0, 0.0)
        self.elmts['Buses'][bus].s = self.set_s(0.0, 0.0)
        self.conns[bus] = list()
        self.n = bus+1
    
    def line(self, name, bus_i, bus_j, long, r_L, x_L, b_Li, g_Li, b_Lj, g_Lj):
        assert bus_i and bus_j in self.info['Buses'].keys(), str(bus_i)+' or/and '+str(bus_j)+' are not in Buses'
        assert type(long) and type(r_L) and type(x_L) and type(b_Li) and type(g_Li) and type(b_Lj) and type(g_Lj) in self.intfloat, 'Some variable is not of '+str(self.intfloat)
        bus_i = self.info['Buses'][bus_i].id
        bus_j = self.info['Buses'][bus_j].id
        self.conns[bus_i] += [bus_j]
        self.conns[bus_j] += [bus_i]
        System.new_element(self,'Lines',Line(name, bus_i, bus_j, self.num_cond, long, r_L, x_L, b_Li, g_Li, b_Lj, g_Lj))
    
    def transformer(self, name, bus_i, bus_j, r, x, s_max, v_inom, v_jnom, conn):
        conns = ['Dy', 'Dyn',  'Dyng', 'Yd', 'Ynd', 'Dd', 'Yy']
        assert bus_i and bus_j in self.info['Buses'].keys(), str(bus_i)+' or/and '+str(bus_j)+' are not in Buses'
        assert type(r) and type(x) and type(s_max) and type(v_inom) and type(v_jnom) in self.intfloat, 'Some variable is not of '+str(self.intfloat)
        assert conn in conns, 'Connection is not valid. Valid types are: '+str(conns)
        bus_i = self.info['Buses'][bus_i].id
        bus_j = self.info['Buses'][bus_j].id
        System.new_element(self,'Transformers',Transformer(name, bus_i, bus_j, r, x, s_max, v_inom, v_jnom, conn))
    
    def gridformer(self, name, bus, v_ref, angle_a):
        assert bus in self.info['Buses'].keys(), str(bus)+' is not in Buses'
        assert type(v_ref) and type(angle_a) in self.intfloat, 'Some variable is not of '+str(self.intfloat)
        bus = self.info['Buses'][bus].id
        v_b = self.elmts['Buses'][bus].v_b
        System.new_element(self, 'Grid Formers', GridFormer(name, bus, v_ref/v_b, angle_a))
        self.elmts['Buses'][bus].type = 'gform'
        self.elmts['Buses'][bus].v = self.set_v(v_ref/v_b, angle_a)
    
    def generator(self, name, bus, p_max, p_min, q_max, q_min):
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Generators', Generator(name, bus, p_max, p_min, q_max, q_min))
        self.elmts['Buses'][bus].type = 'gfoll'
    
    def load(self, name, bus, p_0, q_0, k_z, k_i, k_p):
        assert bus in self.info['Buses'].keys(), str(bus)+' is not in Buses'
        assert type(p_0) and type(q_0) and type(k_z) and type(k_i) and type(k_p) in self.intfloat, 'Some variable is not of '+str(self.intfloat)
        s_b = self.s_b
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Loads', Load(name, bus, np.array(p_0)/s_b, np.array(q_0)/s_b, k_z, k_i, k_p))
        self.elmts['Buses'][bus].type = 'load'
    
    def shunt(self,name,bus):
        assert bus in self.info['Buses'].keys(), str(bus)+' is not in Buses'
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Shunts', Shunt(name,bus))
    
    def set_v(self, v_ref, angle_a):
        n = self.num_phs
        m = self.num_cond
        v = list()
        for k in range(n):
            v.append(v_ref*complex(np.cos(angle_a - k*2*np.pi/n), np.sin(angle_a - k*2*np.pi/n)))
        for k in range(m-n):
            v.append(complex(0, 0))
        return np.array(v)
    
    def set_s(self, p, q):
        n = self.num_phs
        return np.vectorize(complex)(n*[0], n*[0])