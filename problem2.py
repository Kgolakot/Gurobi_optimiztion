#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 04:46:15 2019

@author: krishnasaigolakoti
"""

from gurobipy import*
#no of pilots
n = 7

#language knowledge of the pilots
lang_p = [[20,14,0,13,0,0,8,8],
          [12,0,0,10,15,20,8,9],
          [0,20,12,0,8,11,14,12],
          [0,0,0,0,17,0,0,16]]

#plane type knowledge
type_p = [[18,12,15,0,0,0,8,0],
          [0,17,0,11,13,10,0,0],
          [0,17,0,11,13,10,0,0],
          [0,0,14,0,0,12,16,0],
          [0,0,0,0,12,18,0,18]]
l = 3
t = 4

#model
x = {}
model = Model("pilot assignment")
#decision variable
for i in range(n):
    for j in range(n):
        x[i,j]=model.addVar(vtype = GRB.BINARY, name = "x")
#update variables
model.update()

#add constraint 1
for i in range(n):
    model.addConstr(quicksum(x[i,j] for j in range(n)) == 1)
#add constraint 2 
for j in range(n):
    model.addConstr(quicksum(x[i,j] for j in range(n)) == 1)
#add constraint 3
for i in range(n): 
    model.addConstr(x[i,i] == 0)
#add constraint 4
for i in range(n):
    for j in range(n):
        for k in range(l):
            model.addConstr((lang_p[i][k] + lang_p[j][k]) * x[i,j] >= 10)
#add constraint 5
for i in range(n):
    for j in range(n):
        for z in range(t):
            model.addConstr((type_p[i][z] + type_p[j][z]) * x[i,j] >= 10)
#objective function
obj = quicksum(x[i,j] for i in range(n) for j in range(n))
model.setObjective(obj, GRB.MAXMIZE)
#optimize
model.optimize()





