from gurobipy import *

# Define the set of Tasks and corresponding parameters.

Tasks, duration, max_speedup, cost_of_speedup = multidict({
1: [2, 0 ,0],
2: [16, 3, 30],
3: [9, 1, 26],
4: [8, 2, 12],
5: [10, 2, 17],
6: [6, 1, 15],
7: [2, 1, 8],
8: [2, 0, 0],
9: [9, 2, 42],
10:[5, 1, 21],
11:[3, 1, 18],
12:[2, 0, 0],
13:[1, 0, 0],
14:[7, 2, 22],
15:[4, 2, 12],
16:[3, 1, 6],
17:[9, 3, 16],
18:[1, 0, 0]
})

# Create a list of the precedence arcs

Arcs = [(1,2), (2,3), (2,4), (2,14), (3,5), (4,6),(4,7),(4,9),(4,10),(4,15),
    (5,6),(6,8),(6,9), (6,11), (7,13), (8,16), (9,12), (11,16), (12,17), (14,15),
    (14,16), (17,18)]

# Create an adjacency list for the precedence graph.

Children = [[] for i in Tasks]
for i,j in Arcs:
    Children[i-1].append(j)

speedup_incentive = 30


def Task_Model(Tasks, Precedences, AdjList, duration):

    model = Model('TaskModel')

    finish_time = model.addVar(vtype=GRB.CONTINUOUS, obj = 1, name='z')
    start_time = {}
    for i in Tasks:
        start_time[i] = model.addVar(vtype=GRB.CONTINUOUS, obj = 0, name='x_%g' %i)

    model.modelSense = GRB.MINIMIZE
    model.update()

    # Finishing time constraints
    for i in Tasks:
        if len(AdjList[i-1]) == 0:
            model.addConstr(start_time[i] + duration[i] <= finish_time, name='finish_%g'%i)

    # Precedence constraints

    for i, j in Precedences:
        model.addConstr(start_time[i] + duration[i] <= start_time[j], name='precedence (%g, %g)'%(i,j))

    # Print Solution

    def printSolution():
        if model.status == GRB.status.OPTIMAL:
            print("\nOptimal Solution: %g weeks" %model.objVal)
            for i in Tasks:
                print('Start task %g during week %g. Finish at week %g'%(i, start_time[i].x, start_time[i].x + duration[i]))
        else:
            print('No solution')

    model.optimize()
    printSolution()

    if model.status == GRB.status.OPTIMAL:
        return model.objVal

def Speedup_Model(Tasks, Precedences, AdjList, duration, max_speedup, cost_of_speedup, optimal_time, speedup_incentive):

    model = Model('SpeedupModel')

    finish_time = model.addVar(vtype=GRB.CONTINUOUS, name='z')
    start_time = {}
    speed_up = {}
    for i in Tasks:
        start_time[i] = model.addVar(vtype=GRB.CONTINUOUS, name='x_%g' %i)
        speed_up[i] = model.addVar(vtype=GRB.INTEGER, ub = max_speedup[i], name='y_%g' %i)

    model.setObjective(speedup_incentive*(optimal_time-finish_time) - quicksum(cost_of_speedup[i]*speed_up[i] for i in Tasks), GRB.MAXIMIZE)
    model.update()

    # Finishing time constraints
    for i in Tasks:
        if len(AdjList[i-1]) == 0:
            model.addConstr(start_time[i] + duration[i] - speed_up[i] <= finish_time, name='finish_%g'%i)

    # Precedence constraints

    for i, j in Precedences:
        model.addConstr(start_time[i] + duration[i] - speed_up[i] <= start_time[j], name='precedence (%g, %g)'%(i,j))

    # Print Solution

    def printSolution():
        if model.status == GRB.status.OPTIMAL:
            print("\nOptimal Solution: %g in profit" %model.objVal)
            print("Project finish %g weeks ahead of schedule" %(optimal_time-finish_time.x))
            print('Total cost of speed up %g'%(quicksum(cost_of_speedup[i]*speed_up[i] for i in Tasks).getValue()))
            print(' ')
            for i in Tasks:
                print('Start task %g during week %g. Finish at week %g. Speed up %g weeks'%(i, start_time[i].x, start_time[i].x + duration[i], speed_up[i].x))
        else:
            print('No solution')

    model.optimize()
    printSolution()


optimal_time = Task_Model(Tasks, Arcs, Children, duration)
print('---------------------------')
Speedup_Model(Tasks, Arcs, Children, duration, max_speedup, cost_of_speedup, optimal_time, speedup_incentive)
