#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 01:49:06 2019

@author: krishnasaigolakoti
"""

from gurobipy import*
#litres of product available
p_litres = [1200,700,1000,450,1200]
#amount of products
p = 5
#tanks available 
t = 9
#quantity of the tanks
t_litres = [500,300,400,600,600,900,500,800,800]
#model
x = {}
model = Model("Tank_filling")
#decision variable
for i in range(t):
    for j in range(p):
        x[i,j]=model.addVar(vtype = GRB.BINARY, name = "x")
#update variables
model.update()
#constraint 1
for j in range(p):
    model.addConstr(quicksum(x[i,j]*t_litres[i] for i in range(t)) >= p_litres[j])
#constraint 2
for i in range(t):
    model.addConstr(quicksum(x[i,j] for j in range(p)) - x[1,0] - x[7,4] <= 1)

#objective function
obj = quicksum(x[i,j] for i in range(t) for j in range(p))
model.setObjective(obj, GRB.MINIMIZE)
#optimize
model.optimize()




