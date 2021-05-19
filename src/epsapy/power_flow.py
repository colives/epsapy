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
from scipy.optimize import minimize
# from scipy import sparse
# from scipy.linalg import block_diag
# from scipy.sparse.linalg import spsolve


def fun(x):
    return 0


def v_init(buses):
    v0 = list()
    for bus in buses:
        for v in buses[bus].v:
            v0 += [v.real, v.imag]
    return v0


def sl(buses):
    s = list()
    for bus in buses:
        for s_ in buses[bus].s:
            s.append(s_)
    return s


def cf(x, system):
    xc = np.vectorize(complex)(x[0::2], x[1::2])
    st = sl(system.elmts['Buses'])
    i_sp = list()
    for v,s in zip(xc,st):
        ir_sp = (s.real*v.real + s.imag*v.imag)/(v.real**2 + v.imag**2)
        im_sp = (s.real*v.imag - s.imag*v.real)/(v.real**2 + v.imag**2)
        i_sp.append(complex(ir_sp,im_sp))
    i_sp = np.array(i_sp)
    v = np.array([1.02, 0.0]+list(x))
    i_cl = v
    i_cl = np.vectorize(complex)(i_cl[0::2],i_cl[1::2])
    dirk = i_sp.real - i_cl.real
    dimk = i_sp.imag - i_cl.imag
    return (list(zip(dirk,dimk)))


def power_flow(system, tol=1e-6, maxIter=50):
    opt = {'maxiter':maxIter, 'disp':True}
    x0 = v_init(system.elmts['Buses'])
    argspf = (system)
    cons = [{'type':'eq', 'fun': cf, 'args': argspf}]
    res = minimize(fun, x0, constraints= cons, tol= tol, options= opt)
    return res.x
