from gurobipy import *

Jobs = [1,2,3]
Machines = [1,2,3]
MachineOrder = {
1: (1, 3),
2: (2, 1, 3),
3: (3, 1, 2)
}
Tasks, duration = multidict({
1: 45,
2: 10,
3: 10,
4: 20,
5: 34,
6: 28,
7: 12,
8: 17
})

M = sum([45,10,10,20,34,28,12,17])
print(M)

TaskConjunctive = [(1,2), (3,4), (4,5), (6,7), (7,8)]
TaskConjunctive = tuplelist(TaskConjunctive)

TaskDisjunctive = [[1,4],[1,7], [4,7], [3,8], [2,5], [2,6], [5,6]]

jobModel = Model()

finish = jobModel.addVar(vtype=GRB.CONTINUOUS, obj = 1 , name="finishTime")
start = {}
disjunctive = {}
for i in Tasks:
    start[i] = jobModel.addVar(vtype=GRB.CONTINUOUS, name="start_%g"%i)
    for j in Tasks:
        if i < j and [i,j] in TaskDisjunctive:
            disjunctive[i,j] = jobModel.addVar(vtype=GRB.BINARY, name="disjunct_%g_%g"%(i,j))

jobModel.update()
jobModel.modelSense = GRB.MINIMIZE

for j in Tasks:
    jobModel.addConstr(start[j] + duration[j] <= finish, name="finishingTime_%g"%j)

for i,j in TaskConjunctive:
    jobModel.addConstr(start[i] + duration[i] <= start[j], name="precedent_%g_%g"%(i,j))

for i,j in TaskDisjunctive:
    jobModel.addConstr(start[i] + duration[i] <= start[j] + M*(1-disjunctive[i,j]))
    jobModel.addConstr(start[j] + duration[j] <= start[i] + M*disjunctive[i,j])


jobModel.optimize()

for i in Tasks:
    print("Start time for task {} is {}, Finish time {}".format(i, start[i].x, start[i].x + duration[i]))
