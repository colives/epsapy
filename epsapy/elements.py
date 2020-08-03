#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:41:54 2020

@author: carlosolives
"""

class node(object):
    
    next_id = 0
    node_list = []
    
    def __init__ (self,name):
        self.name = name
        self.id = node.next_id
        self.v, self.angle = None, None
        self.kind = 'pq'
        self.p,self.q = 0,0
        node.node_list.append(self)
        node.next_id += 1
    
    def __str__(self):
        return str(self.name)+', ID node: '+str(self.id)+', V = '+str(self.v)+' |'+str(self.angle)
        
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_kind(self):
        return self.kind
    def get_p(self):
        return self.p
    def get_q(self):
        return self.q
    def get_volt(self):
        return self.v
    def get_angle(self):
        return self.angle
    
    def set_name(self, newname):
        self.name = newname
    def set_kind(self, newkind):
        self.kind = newkind
    def set_p(self,newp):
        self.p = newp
    def set_q(self,newq):
        self.q = newq
    def set_volt(self, newv):
        self.v = newv        
    def set_angle(self, newtheta):
        self.angle = newtheta

class branch(object):

    branch_list = []

    def __init__(self,name,node1,node2,smax):
        self.name = name
        self.node1 = reallocation(node1)
        self.node2 = reallocation(node2)
        self.smax = smax
        self.p, self.q = None, None

    def get_name(self):
        return self.name
    def get_nodes_connected(self):
        return self.node1, self.node2
    def get_p_lim(self):
        return self.p_max
    def get_q_lim(self):
        return self.q_max

    def set_p(self, newp):
        self.p = newp
    def set_q(self, newq):
        self.q = newq

class transformer(branch):

    def __init__(self,name,node1,node2,r,x,smax,v1_nom,v2_nom):
        branch.__init__(self,name,node1,node2,smax)
        self.v1_nom, self.v2_nom = v1_nom, v2_nom
        transformer.branch_list.append(self)

    def get_rt(self):
        return self.v1_nom/self.v2_nom
    def get_r(self):
        return self.r
    def get_x(self):
        return self.x

class line(branch):
    
    def __init__(self,name,node1,node2,smax,long,r,x):
        branch.__init__(self,name,node1,node2,smax)
        self.long = long
        self.r = r
        self.x = x
        line.branch_list.append(self)

    def get_r(self):
        return self.r*self.long
    def get_x(self):
        return self.x*self.long
    def get_long(self):
        return self.long

class generator(object):
    
    generator_list = []
    
    def __init__ (self,name,node,kind,p_max,p_min,q_max,q_min,p=None,q=None,v=None,theta=None):
        self.name = name
        self.node = reallocation(node)
        self.kind = kind
        self.p_max,self.p_min = p_max,p_min
        self.q_max,self.q_min = q_max,q_min
        self.p,self.q = p,q
        self.v,self.theta = v,theta
        generator.generator_list.append(self)
        update_node(self)
        
    def get_name(self):
        return self.name
    def get_node(self):
        return self.node
    def get_kind(self):
        return self.kind
    def get_p_lim(self):
        return self.p_min,self.p_max
    def get_q_lim(self):
        return self.q_min,self.q_max
    def get_p(self):
        return self.p
    def get_q(self):
        return self.q
    def get_volt(self):
        return self.v
    def get_angle(self):
        return self.theta
    
    def set_kind(self,newkind):
        self.kind = newkind
        update_node(self)
    def set_p(self, newp):
        self.p = newp
        update_node(self)
    def set_q(self, newq):
        self.q = newq
        update_node(self)
    def set_volt(self, newv):
        self.v = newv
        update_node(self)
    def set_angle(self, newtheta):
        self.theta = newtheta
        update_node(self)
        
class load(object):
    
    load_list = []
    
    def __init__(self,name,node,kind,p_sp,q_sp,p=None,q=None,v=None,theta=None):
        self.name = name
        self.node = reallocation(node)
        self.kind = kind
        self.p_sp,self.q_sp = p_sp,q_sp
        self.p,self.q = p,q
        self.v,self.theta = v,theta
        load.load_list.append(self)
        update_node(self)
        
    def get_name(self):
        return self.name
    def get_node(self):
        return self.node
    def get_kind(self):
        return self.kind
    def get_p_sp(self):
        return self.p_sp
    def get_q_sp(self):
        return self.q_sp
    def get_p(self):
        return self.p
    def get_q(self):
        return self.q
    def get_volt(self):
        return self.v
    def get_angle(self):
        return self.theta
    
    def set_kind(self,newkind):
        self.kind = newkind
        update_node(self)
    def set_p(self, newp):
        self.p = newp
        update_node(self)
    def set_q(self, newq):
        self.q = newq
        update_node(self)
    def set_volt(self, newv):
        self.v = newv
        update_node(self)
    def set_angle(self, newtheta):
        self.theta = newtheta
        update_node(self)
        
def reallocation(node_name):
    aux = None
    for bus in node.node_list:
        if bus.get_name() == node_name:
            aux = bus.get_id()
            break
    else:
        print('Node '+node_name+' does not exist')
    return aux

def update_node(generator):
    for bus in node.node_list:
        if bus.get_id() == generator.get_node():
            bus.set_kind(generator.get_kind())
            if generator.get_kind() == 'pq':
                bus.set_p(generator.get_p())
                bus.set_q(generator.get_q())
            elif generator.get_kind() == 'pv':
                bus.set_volt(generator.get_volt())
                bus.set_p(generator.get_p())
            elif generator.get_kind() == 'slack':
                bus.set_volt(generator.get_volt())
                bus.set_angle(generator.get_angle())
            break