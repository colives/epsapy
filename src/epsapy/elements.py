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
        self.volt, self.angle_v = None, None
        self.curr, self.angle_i = None, None
        self.p,self.q = 0, 0


class Bus(object):
    bus_id = 0
    node_cls = Node
    
    def __init__ (self,name,phs,conds):
        self.name = name
        self.id = Bus.bus_id
        for i in range(phs):
            exec('self.node_'+str(string.ascii_lowercase[i])+' = '+"self.node_cls('"+str(string.ascii_lowercase[i])+"')")
        if conds -phs == 1:
            self.node_n = self.node_cls('n')
        Bus.bus_id += 1


class Branch(object):

    def __init__(self,name,bus_i,bus_j,smax,phases):
        self.name = name
        self.smax = smax
        self.p, self.q = None, None


class Line(Branch):
    
    def __init__(self,name,node1,node2,smax,phases,long,r,l):
        Branch.__init__(self,name,node1,node2,smax,phases)
        self.long = long
        self.r = r
        self.l = l


class System(object):
    
    def __init__(self,freq,s_b,num_phs,num_cond):
        self.freq = freq
        self.s_b = s_b
        self.num_phs = num_phs
        self.num_cond = num_cond
        self.info = {}
        
    def new_element(self,key,value):
        if key in self.info.keys():
            self.info[key].append(value)
        else:
            self.info[key] = [value]

    def bus(self,name):
        System.new_element(self,'Buses', Bus(name, self.num_phs, self.num_cond))
        
    def line(self,name,bus_i,bus_j,s_max,phases,long,r,l):
        System.new_element(self, 'Lines', Line(name,bus_i,bus_j,s_max,phases,long,r,l))
    
    def transformer(self,name):
        pass
    
    def generator(self,name):
        pass
    
    def load(self,name):
        pass

# class transformer(branch):

#     def __init__(self,name,node1,node2,r,x,smax,v1_nom,v2_nom):
#         super().__init__(name,node1,node2,smax)
#         self.v1_nom, self.v2_nom = v1_nom, v2_nom
#         transformer.branch_list.append(self)


# class generator(object):
    
#     generator_list = []
    
#     def __init__ (self,name,node,kind,p_max,p_min,q_max,q_min,p=None,q=None,v=None,theta=None):
#         self.name = name
#         self.node = reallocation(node)
#         self.kind = kind
#         self.p_max,self.p_min = p_max,p_min
#         self.q_max,self.q_min = q_max,q_min
#         self.p,self.q = p,q
#         self.v,self.theta = v,theta
#         generator.generator_list.append(self)
#         update_node(self)
        
# class load(object):
    
#     load_list = []
    
#     def __init__(self,name,node,kind,p_sp,q_sp,p=None,q=None,v=None,theta=None):
#         self.name = name
#         self.node = reallocation(node)
#         self.kind = kind
#         self.p_sp,self.q_sp = p_sp,q_sp
#         self.p,self.q = p,q
#         self.v,self.theta = v,theta
#         load.load_list.append(self)
#         update_node(self)

        
# def reallocation(node_name):
#     aux = None
#     for bus in Node.node_list:
#         if bus.get_name() == node_name:
#             aux = bus.get_id()
#             break
#     else:
#         print('Node '+node_name+' does not exist')
#     return aux

# def update_node(generator):
#     for bus in Node.node_list:
#         if bus.get_id() == generator.get_node():
#             bus.set_kind(generator.get_kind())
#             if generator.get_kind() == 'pq':
#                 bus.set_p(generator.get_p())
#                 bus.set_q(generator.get_q())
#             elif generator.get_kind() == 'pv':
#                 bus.set_volt(generator.get_volt())
#                 bus.set_p(generator.get_p())
#             elif generator.get_kind() == 'slack':
#                 bus.set_volt(generator.get_volt())
#                 bus.set_angle(generator.get_angle())
#             break
