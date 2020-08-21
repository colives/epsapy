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

class Node(object):
    
    def __init__ (self,cond):
        self.cond = cond
        self.volt = None
        self.angle_v = None
        self.curr = None
        self.angle_i = None
        self.p = None
        self.q = None


class Bus(object):
    bus_id = 0
    node_cls = Node
    
    def __init__ (self,name,v_b,conds):
        self.name = name
        self.id = Bus.bus_id
        self.v_b = v_b
        for cond in conds:
            exec('self.node_'+cond+' = '+"self.node_cls('"+cond+"')")
        Bus.bus_id += 1


class Branch(object):

    def __init__(self,name,bus_i,bus_j,s_max,phases):
        self.name = name
        self.s_max = s_max
        self.bus_i = bus_i
        self.bus_j = bus_j
        self.p, self.q = None, None

    def limit(p,q,s_max):
        lim = False
        if p*p + q*q < s_max*s_max:
            lim = True
        return lim


class Line(Branch):
    
    def __init__(self,name,bus_i,bus_j,smax,phases,long,r1,l1,r0,l0):
        super().__init__(self,name,bus_i,bus_j,smax,phases)
        self.long = long
        self.r1 = r1
        self.l1 = l1
        self.r0 = r0
        self.l0 = l0


class Transformer(Branch):

    def __init__(self,name,bus_i,bus_j,r,x,smax,phases,v_inom,v_jnom,conn):
        super().__init__(name,bus_i,bus_j,smax,phases)
        self.v_inom = v_inom
        self.v_jnom = v_jnom
        self.conn = conn


class Shunt(object):

    def __init__(self,name,bus,phases):
        self.name = name
        self.bus = bus
        self.phases = phases
    

class Load(object):
    
    def __init__(self,name,bus,p_sp,q_sp,v_max,v_min):
        self.name = name
        self.bus = bus
        self.p_sp = p_sp
        self.q_sp = q_sp
        self.v_max = v_max
        self.v_min = v_min
        

class Generator(object):
    
    def __init__ (self,name,bus,p_max,p_min,q_max,q_min):
        self.name = name
        self.bus = bus
        self.p_max = p_max
        self.p_min = p_min
        self.q_max = q_max
        self.q_min = q_min


class System(object):
    
    def __init__(self,freq,s_b,num_phs,num_cond):
        self.freq = freq
        self.s_b = s_b
        self.num_phs = num_phs
        self.num_cond = num_cond
        self.phases = [string.ascii_lowercase[i] for i in range(num_phs)]
        _all = self.phases + ['n','gr']
        self.conds = [_all[i] for i in range(num_cond)]
        self.info = {'Buses': {}, 'Lines': {}, 'Transformers': {}, 'Generators': {}, 'Loads': {}, 'Shunts':{}}
        
    def new_element(self,key,value):
        self.info[key][value.name] = value

    def bus(self,name,v_b):
        System.new_element(self,'Buses', Bus(name, v_b, self.conds))
        
    def line(self,name,bus_i,bus_j,s_max,phases,long,r,l):
        bus_i = self.info['Buses'][bus_i].id
        bus_j = self.info['Buses'][bus_j].id
        System.new_element(self, 'Lines', Line(name,bus_i,bus_j,s_max,phases,long,r,l))
    
    def transformer(self,name,bus_i,bus_j,r,x,s_max,phases,v_inom,v_jnom,conn):
        bus_i = self.info['Buses'][bus_i].id
        bus_j = self.info['Buses'][bus_j].id
        System.new_element(self,'Transformers',Transformer(name,bus_i,bus_j,r,x,s_max,phases,v_inom,v_jnom,conn))
    
    # def generator(self,name,bus):
    #     bus = self.info['Buses'][bus].id
    #     pass
    
    # def load(self,name,bus,p_sp,q_sp,v_max,v_min):
    #     bus = self.info['Buses'][bus].id
    #     System.new_element(self, 'Loads', Load(name,bus,p_sp,q_sp,v_max,v_min))
    
    # def shunt(self,name,bus,phases):
    #     bus = self.info['Buses'][bus].id
    #     pass