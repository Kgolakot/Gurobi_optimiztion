#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 05:47:14 2019

@author: krishnasaigolakoti
"""

from gurobipy import*
#demand from each customer
d = [120,80,75,100,110,100,90,60,30,150,95,120]
#capacity of each depot
c = [300,250,100,180,275,300,200,220,270,250,230,180]
#fixed costs for each depot
f = [3500,9000,10000,4000,3000,9000,3000,4000,10000,9000,3500]
#no of depots
n = 12
#no of customers 
t = 12
M = 500
r = 1000
z={}
v = [[100,80,50,50,60,100,120,90,60,70,65,110],
     [120,90,60,70,65,110,140,110,80,80,75,130],
     [140,110,80,80,75,130,160,125,100,100,80,150],
     [160,125,100,100,80,150,190,150,130,M,M,M],
     [190,150,130,M,M,M,200,180,150,M,M,M],
     [200,180,150,M,M,M,100,80,50,50,60,100],
     [100,80,50,50,60,100,120,90,60,70,65,100],
     [120,90,60,70,65,110,140,110,80,80,72,130],
     [140,110,80,80,75,130,160,125,100,100,80,150],
     [160,125,100,100,80,150,190,150,130,M,M,M],
     [190,150,130,M,M,M,200,180,150,M,M,M],
     [200,180,150,M,M,M,100,80,50,50,60,100]]
model=Model("Depot creation")

for i in range(n):
    for j in range(n):
        v[i][j]=v[i][j]*r

#variable for each unit
for i in range(n):
    for j in range(n):
        z[i,j] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="unit" ) 
#depot opening variable
for i in range(n):
    x[j] = model.addVar(vtype=GRB.BINARY, name="x")
model.update()
#Constraint addition
for j in range(n):
    model.addConstr(quicksum(z[i,j] for i in range(n)) == d[j] )
#Constraint 2
for i in range(n):
    model.addConstr((quicksum(z[i,j] for j in range(n))-(x[j]*quicksum(x[j] for j in range(n)))) <= 0)
#objective function
obj = quicksum((v[i][j]/d[j])*z[i,j] for i in range(n) for j in range(n)) + quicksum(f[i]*x[i] for i in range(n))
model.setObjective(obj, GRB.MINIMIZE)
#optimize
model.optimize()

   

