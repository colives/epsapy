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
The :mod:`epsapy.power_flow` module is intended to contain the specific 
algorithm to solve a three phase power flow problem.
"""

import numpy as np
from scipy import sparse
from scipy.linalg import block_diag
from scipy.sparse.linalg import spsolve

def E_maker(Ysp,n,b,pv):
    Ydiag = Ysp.diagonal()
    aux = sparse.triu(Ysp,k=1)
    colqii = np.arange(n)
    rowqii = np.arange(n)
    dataqii = np.imag(Ydiag)
    dataqii[pv] = 1
    colpii = np.arange(1,n)
    rowpii = np.arange(n,2*n-1)
    datapii = np.real(Ydiag[1:])
    colqij = np.arange(2*n,2*(n+2*b))//2
    rowqij = np.reshape(np.column_stack((aux.row,aux.col,aux.row,aux.col)),-1)
    dataqij = np.reshape(np.column_stack((np.reshape(np.column_stack((-np.imag(aux.data),np.real(aux.data))),-1),np.reshape(np.column_stack((-np.imag(aux.data),-np.real(aux.data))),-1))),-1)
    colpij = colqij[rowqij>0]
    rowpij = rowqij[rowqij>0]+n-1
    datapij = np.reshape(np.column_stack((np.reshape(np.column_stack((np.real(aux.data),np.imag(aux.data))),-1),np.reshape(np.column_stack((np.real(aux.data),-np.imag(aux.data))),-1))),-1)[rowqij>0]
    pvfilter = np.isin(rowqij,rowqii[np.logical_not(pv)])
    colqij = colqij[pvfilter]
    rowqij = rowqij[pvfilter]
    dataqij = dataqij[pvfilter]
    ###
    row = np.concatenate((rowqii,rowpii,rowqij,rowpij))
    col = np.concatenate((colqii,colpii,colqij,colpij))
    data = np.concatenate((dataqii,datapii,dataqij,datapij))
    return sparse.coo_matrix((data,(row,col))).tocsr()

def C_maker(Ysp,n,b):
    aux = sparse.triu(Ysp,k=1)
    row0 = np.arange(n)
    col0 = np.arange(n-1,2*n-1)
    data0 = np.ones(n)
    row1 = np.concatenate((np.arange(n,n+b),np.arange(n,n+b)))
    col1 = np.concatenate((aux.row+n-1,aux.col+n-1))
    data1 = np.ones_like(row1)
    col2 = col1[col1>n-1][:]-n
    row2 = row1[col1>n-1]+b
    data2 = np.concatenate((np.ones(n),-1*np.ones(n)))[col1>n-1]
    row = np.concatenate((row0,row1,row2))
    col = np.concatenate((col0,col1,col2))
    data = np.concatenate((data0,data1,data2))
    return sparse.coo_matrix((data,(row,col))).tocsr()

def p_maker(p_x,pv,n):
    for ind in range(n):
        if pv[ind] == True:
            p_x[ind] = p_x[ind]**2
    return p_x

def flat_start(n,p): #Falta multiplicar la tensión del slack
    return np.concatenate((np.zeros(n-1),2*np.log(p[0]*np.ones(n))))

def f(y,n,b):
    return np.concatenate((np.log(y[:n],dtype=np.complex64),np.log(y[n::2]**2+y[n+1::2]**2),np.arctan2(np.real(y[n+1::2]),np.real(y[n::2]))))
    
def f_(u,n,b):
    y1 = np.exp(u[:n])
    aux = np.column_stack((np.exp(0.5*u[n:n+b])*np.cos(u[n+b:]),np.exp(0.5*u[n:n+b])*np.sin(u[n+b:])))
    aux = np.reshape(aux,-1)
    return np.concatenate((y1,aux))

def F_(y,n):
    u = y[:n]
    ks = y[n::2]
    ls = y[n+1::2]
    F_ = np.diag(u)
    for k,l in zip(ks,ls):
        F_ = block_diag(F_,[[0.5*k,-l],[0.5*l,k]])
    return sparse.csr_matrix((F_))

def solver(x,n,b,C,E,p,tol,maxIter):
    E2 = E.dot(E.transpose())
    for _ in range(maxIter):
        y = f_(C.dot(x),n,b)
        res = p -E.dot(y)
        if np.linalg.norm(res,ord=np.inf)<tol:
            return x,
        beta = spsolve(E2,res)
        y = y + E.transpose().dot(beta)
        Fi = F_(y,n)
        aux = E.dot(Fi)
        x = spsolve(aux.dot(C),aux.dot(f(y,n,b)))
    else:
        print('Maximum number of iterations has been reached: '+str(maxIter))

def power_flow(system, tol, maxIter):
    Ybus = system.Ybus()
    p = system.p()
    pv = system.pv()
    if sparse.issparse(Ybus):
        Ysp = Ybus.copy()
    else:    
        Ysp = sparse.coo_matrix((Ybus))
    n = Ysp.shape[0]
    b = (len(sparse.find(Ysp)[0])-n)//2
    x0 = flat_start(n,p)
    C = C_maker(Ysp,n,b)
    E = E_maker(Ysp,n,b,pv)
    px = p_maker(p,pv,n)
    return solver(x0,n,b,C,E,px,tol,maxIter)