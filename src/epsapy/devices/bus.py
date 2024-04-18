#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.bus` module provides the bus class to model.
"""

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