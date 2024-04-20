#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epsapy
Electrical Power Systems Analysis

The :mod:`~epsapy.devices.utils` module provides common characteristics.
"""

class Int_Input:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value == None:
            instance.__dict__[self._name] = None
        else:
            try:
                instance.__dict__[self._name] = int(value)
            except ValueError:
                raise ValueError(f'"{self._name}" must be an integer number, got {type(value)}') from None

class Num_Input:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value == None:
            instance.__dict__[self._name] = None
        else:
            try:
                instance.__dict__[self._name] = float(value)
            except ValueError:
                raise ValueError(f'"{self._name}" must be a number, got {type(value)}') from None