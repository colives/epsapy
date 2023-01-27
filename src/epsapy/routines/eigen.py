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
The :mod:`epsapy.eigen` module is intended to contain the tools for eigenvalue
analysis.
"""

import numpy as np
from scipy.optimize import minimize


def fun(x):
    return 0


def v_init(buses):
    v0 = list()
    for bus in buses:
        for v in buses[bus].v:
            v0 += [v.real, v.imag]
    return v0


def i_sp(syst, x):
    n = syst.num_phs
    m = syst.num_cond
    id_x = 0
    id_l = 0
    i = list()
    for bus in syst.elmts['Buses'].values():
        if bus.type == 'trns':
            i.append(np.vectorize(complex)(m*[0],m*[0]))
            id_x += m
        if bus.type == 'load':
            load = syst.elmts['Loads'][id_l]
            for i in range(n):
                vi = abs(x[id_x])
                zipl = load.k_z[i]*vi*vi + load.k_i[i]*vi + load.k_p[i]
                p = load.p_0[i]*zipl
                q = load.q_0[i]*zipl
                i_re = (p*x[id_x].real + q*x[id_x].imag)/(vi*vi)
                i_im = (p*x[id_x].imag - q*x[id_x].real)/(vi*vi)
                i.append(complex(i_re,i_im))
                id_x += 1
            i.append(sum(i[-n:]))
            id_l += 1
        else:
            pass
    return i


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
    for v,s in zip(xc, st):
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
