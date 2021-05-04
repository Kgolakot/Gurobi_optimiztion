# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from gurobipy import*
#boxes weight
b = [34,6,8,17,16,5,13,21,25,31,14,13,33,9,25,25]
#no of wagons 
m = 3
#no of boxes
n = 16
x = {}

model = Model('Packing')
#decision variable
for i in range(n):
    for j in range(m):
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x")
        
model.update()
#add constraints
for j in range(m):
    model.addConstr(quicksum(x[i,j]*b[i] for i in range(n)) <= 100)
    
#add constraint 2
for i in range(n):
    model.addConstr(quicksum(x[i,j] for j in range(m)) == 1)

#objective function
for j in range(m):
    obj = quicksum(x[i,j]*b[i] for i in range(n))
    
#minimize the objective function
model.setObjective(obj, GRB.MINIMIZE)

#optimize the model
model.optimize()
