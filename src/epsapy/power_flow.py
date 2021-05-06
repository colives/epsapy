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
from scipy.sparse.linalg import lsqr


def cnstr():
    pass


def solver():
    pass


def power_flow(system, tol, maxIter):
    Ybus = system.Ybus()
    if sparse.issparse(Ybus):
        Ysp = Ybus.copy()
    else:
        Ysp = sparse.coo_matrix((Ybus))
    n = Ysp.shape[0]
    pass
