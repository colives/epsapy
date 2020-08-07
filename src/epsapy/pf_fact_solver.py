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
The :mod:`epsapy.pf_fact_solver` module is intended to contain the specific 
algorithm to solve a three phase power flow problem.
"""

import numpy as np

def start(node_list):
    v,theta = [],[]
    for bus in node_list:
        bus.set_angle(0.0)
        if bus.get_volt() == None:
            bus.set_volt(1.0)
        v.append(bus.get_volt())
        theta.append(bus.get_angle())
    return np.array(v+theta)

def initial_map(x_0,N):
    return np.concatenate((2*np.log(x_0[0:N]),x_0[N:-1]))

def final_map(x,N):
    return np.vstack((np.exp(x[0:N]/2),np.zeros(1),x[N:]))

def p_fill(N,node_list):
    p = np.zeros(2*N-1)
    i = 0
    for bus in node_list:
        if bus.get_kind() == 'pq':
            p[i] = bus.get_q()
            p[i+N-1] = bus.get_p()
        elif bus.get_kind() == 'pv':
            p[i] = (bus.get_volt())**2
            p[i+N-1] = bus.get_p()
        else:
            p[i] = (bus.get_volt())**2
        i += 1
    return p

def admitance(branch_list,N):
    Y = np.zeros((N,N),dtype = 'complex64')
    for element in branch_list:
        Y[element.get_nodes_connected()[0],element.get_nodes_connected()[1]] = -(element.get_r()+1j*element.get_x())**(-1)
        Y[element.get_nodes_connected()[1],element.get_nodes_connected()[0]] = -(element.get_r()+1j*element.get_x())**(-1)
    for i in range(N):
        Y[i,i] = -sum(Y[i,:])
    return Y

def f(y,N,b,branch_list):
    alphai = np.log(y[:N])
    alphaij = []
    for branch in branch_list:
        alphaij.append(alphai[branch.get_nodes_connected()[0]]+alphai[branch.get_nodes_connected()[1]])
    alphaij = np.array(alphaij)
    theta = []
    for j in range(0,2*b,2):
        theta.append(np.arctan2(y[N+1+j],y[N+j]))
    theta = np.array(theta)
    return np.concatenate((alphai,alphaij,theta))

def finv(u,N,b):
    U = np.exp(u[:N])
    aux = np.exp(u[N:N+b])
    theta = u[N+b:N+2*b]
    K = aux*np.cos(theta)
    L = aux*np.sin(theta)
    return np.block([[U.reshape((-1,1))],[np.vstack((K,L)).reshape((-1,1),order='F')]])

def C_maker(N,b,branch_list):
    c3 = np.zeros((b,N))
    c6 = np.zeros_like(c3)
    for i in range(b):
        c3[i,branch_list[i].get_nodes_connected()[0]] = 1
        c3[i,branch_list[i].get_nodes_connected()[1]] = 1
        c6[i,branch_list[i].get_nodes_connected()[0]] = 1
        c6[i,branch_list[i].get_nodes_connected()[1]] = -1
    c6 = c6[:,1:]
    return np.block([[np.eye(N),np.zeros((N,N-1))],[c3,np.zeros((b,N-1))],[np.zeros((b,N)),c6]])

def E_maker(N,b,Y,node_list,branch_list):
    e1 = np.zeros((N-1,N))
    e2 = np.zeros((N-1,N))
    e3 = np.zeros((N-1,2*b))
    e4 = np.zeros((N-1,2*b))
    i = 0
    for node in node_list:
        if node.get_kind() == 'pq':
            e1[i,node.get_id()] = -np.imag(Y[node.get_id(),node.get_id()])
            e2[i,node.get_id()] = np.real(Y[node.get_id(),node.get_id()])
            j = 0
            for branch in branch_list:
                if branch.get_nodes_connected()[0] == node.get_id() or branch.get_nodes_connected()[1] == node.get_id():
                    e3[i,j] = -np.imag(Y[branch.get_nodes_connected()[0],branch.get_nodes_connected()[1]])
                    e4[i,j] = np.real(Y[branch.get_nodes_connected()[0],branch.get_nodes_connected()[1]])
                    s = 1 if branch.get_nodes_connected()[0] == node.get_id() else -1
                    e3[i,j+1] = s*np.real(Y[branch.get_nodes_connected()[0],branch.get_nodes_connected()[1]])
                    e4[i,j+1] = s*np.imag(Y[branch.get_nodes_connected()[0],branch.get_nodes_connected()[1]])
                j += 2
            i+=1
        elif node.get_kind() == 'pv':
            e1[i,node.get_id()] = 1
            e2[i,node.get_id()] = np.real(Y[node.get_id(),node.get_id()])
            j = 0
            for branch in branch_list:
                if branch.get_nodes_connected()[0] == node.get_id() or branch.get_nodes_connected()[1] == node.get_id():
                    e4[i,j] = np.real(Y[branch.get_nodes_connected()[0],branch.get_nodes_connected()[1]])
                    s = 1 if branch.get_nodes_connected()[0] == node.get_id() else -1
                    e4[i,j+1] = s*np.imag(Y[branch.get_nodes_connected()[0],branch.get_nodes_connected()[1]])
                j += 2    
            i+=1
        else:
            pass
    e0 = np.concatenate((np.array([1.0]),np.zeros((N-1+2*b))))
    return np.block([[e0],[e1,e3],[e2,e4]])

def F_inv_maker(N,b,y):
    u = y[0:N]
    Finv = np.block([[np.eye(N)*u, np.zeros((N,2*b))],[np.zeros((2*b,N+2*b))]])
    for i in range(N,N+2*b,2):
        Finv[i,i] = 0.5*y[i,0]
        Finv[i+1,i] = 0.5*y[i+1,0]
        Finv[i,i+1] = -y[i+1,0]
        Finv[i+1,i+1] = y[i,0]
    return Finv

def update(x,N,node_list,generator_list,load_list):
    v = x[0:N]
    theta = x[N:]
    for bus in node_list:
        bus.set_volt(v[bus.get_id()])
        bus.set_angle(theta[bus.get_id()])

def fact_solv(node_list,branch_list,generator_list,load_list,tol,maxIter):
    
    N = len(node_list)
    b = len(branch_list)
    it = 0
    x_0 = start(node_list)
    x = initial_map(x_0,N)
    Y = admitance(branch_list,N)
    C = C_maker(N, b, branch_list)
    y = finv(C@x, N, b)
    E = E_maker(N,b,Y,node_list,branch_list)
    E_strg = np.linalg.inv(E@E.transpose())
    p = np.reshape(p_fill(N,node_list),[-1,1])
    delta = p - E@y
    while it < maxIter:
        landa = -E_strg@(delta)
        y_corr = y + E.transpose()@landa
        Finv = F_inv_maker(N,b,y_corr)
        H = E@Finv@C
        x = np.linalg.inv(H)@E@Finv@f(y_corr,N,b,branch_list)
        y = finv(C@x, N, b)
        delta = p - E@y
        it += 1
        if all(np.abs(delta)<tol):
            break
    else:
        print('Maximum number of iterations was reached: '+str(maxIter))
    x = final_map(x,N)
    return x,it