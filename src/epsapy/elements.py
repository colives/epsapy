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

class Node(object):
    
    def __init__ (self, cond):
        self.cond = cond
        self.volt = None
        self.curr = None
        self.p = None
        self.q = None


class Bus(object):
    bus_id = 0
    node_cls = Node
    
    def __init__ (self, name, v_b, conds):
        self.id = Bus.bus_id
        self.name = name
        self.v_b = v_b
        self.type = 'trns'
        self.y_sh = None
        self.v = list()
        self.s = list()
        for cond in conds:
            exec('self.node_'+cond+' = '+"self.node_cls('"+cond+"')")
        Bus.bus_id += 1


class Branch(object):

    def __init__(self, name, bus_i, bus_j, phases):
        self.name = name
        self.bus_i = bus_i
        self.bus_j = bus_j
        self.phases = phases
        self.id = int(str(bus_i)+str(bus_j))


class Shunt(object):

    def __init__(self, name, bus, phases):
        self.name = name
        self.bus = bus
        self.phases = phases
        

class Line(Branch):
    
    def __init__(self, name, bus_i, bus_j, phases, long, r_L, x_L, b_Li, g_Li, b_Lj, g_Lj):
        super().__init__(name, bus_i, bus_j, phases)
        self.long = long
        self.r_L = r_L
        self.x_L = x_L
        self.b_Li = b_Li
        self.g_Li = g_Li
        self.b_Lj = b_Lj
        self.g_Lj = g_Lj
        z = np.vectorize(complex)(r_L, x_L)
        self.y_conn = 1/z
        self.y_sh_i = np.vectorize(complex)(g_Li, b_Li)
        self.y_sh_j = np.vectorize(complex)(g_Lj, b_Lj)
        

class Transformer(Branch):

    def __init__(self, name, bus_i, bus_j, r, x, phases, v_inom, v_jnom, conn):
        super().__init__(name, bus_i, bus_j, phases)
        self.v_inom = v_inom
        self.v_jnom = v_jnom
        self.conn = conn


class Load(Shunt):
    load_id = 0
    
    def __init__(self, name, bus, phases, p_0, q_0, k_z, k_i, k_p):
        super().__init__(name,bus,phases)
        self.p_0 = p_0
        self.q_0 = q_0
        self.k_z = k_z        
        self.k_i = k_i
        self.k_p = k_p
        self.id = Load.load_id
        Load.load_id += 1
        

class GridFormer(Shunt):
    gf_id = 0
    
    def __init__(self, name, bus, phases, v_ref, angle_a):
        super().__init__(name, bus, phases)
        self.v_ref = v_ref
        self.angle_a = angle_a
        self.id = GridFormer.gf_id
        GridFormer.gf_id += 1
        

class Generator(Shunt):
    gen_id = 0
    
    def __init__ (self,name,bus,phases,p_max,p_min,q_max,q_min):
        super().__init__(name,bus,phases)
        self.p_max = p_max
        self.p_min = p_min
        self.q_max = q_max
        self.q_min = q_min
        self.id = Generator.gen_id
        Generator.gen_id += 1


class System(object):
    
    def __init__(self,freq,s_b,num_phs,num_cond):
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
        bus = System.new_element(self,'Buses', Bus(name, v_b, self.conds))
        self.elmts['Buses'][bus].v = self.set_v(1.0, 0.0)
        self.conns[bus] = list()
        self.n = bus+1
        
    def line(self,name,bus_i,bus_j,phases,long,r_L,x_L,b_Li,g_Li,b_Lj,g_Lj):
        bus_i = self.info['Buses'][bus_i].id
        bus_j = self.info['Buses'][bus_j].id
        self.conns[bus_i] += [bus_j]
        self.conns[bus_j] += [bus_i]
        System.new_element(self,'Lines',Line(name,bus_i,bus_j,phases,long,r_L,x_L,b_Li,g_Li,b_Lj,g_Lj))
    
    def transformer(self,name,bus_i,bus_j,r,x,s_max,phases,v_inom,v_jnom,conn):
        bus_i = self.info['Buses'][bus_i].id
        bus_j = self.info['Buses'][bus_j].id
        System.new_element(self,'Transformers',Transformer(name,bus_i,bus_j,r,x,s_max,phases,v_inom,v_jnom,conn))
    
    def gridformer(self, name, bus, phases, v_ref, angle_a):
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Grid Formers', GridFormer(name, bus, phases, v_ref, angle_a))
        self.elmts['Buses'][bus].type = 'gf'
        self.elmts['Buses'][bus].v = self.set_v(v_ref, angle_a)
        
    def generator(self,name,bus,p_max,p_min,q_max,q_min):
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Generators', Generator(name,bus,p_max,p_min,q_max,q_min))
        self.elmts['Buses'][bus].type = 'gen'
    
    def load(self,name,bus,p_sp,q_sp,v_max,v_min):
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Loads', Load(name,bus,p_sp,q_sp,v_max,v_min))
        self.elmts['Buses'][bus].type = 'load'
    
    def shunt(self,name,bus,phases):
        bus = self.info['Buses'][bus].id
        System.new_element(self, 'Shunts', Shunt(name,bus,phases))
        
    def set_v(self, v_ref, angle_a):
        n = self.num_phs
        m = self.num_cond
        v = list()
        for k in range(n):
            v.append(v_ref*complex(np.cos(angle_a - k*2*np.pi/n), np.sin(angle_a - k*2*np.pi/n)))
        for k in range(m-n):
            v.append(complex(0, 0))
        return np.array(v)