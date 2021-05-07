import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model


def JobScheduling(plats_data):
    """Minimal platoon problem."""
    # Create the model.
    model = cp_model.CpModel()

    nodes_count = 1 + max(task[0] for plat in plats_data for task in plat)
    all_nodes = range(nodes_count)

    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for plat in plats_data for task in plat)

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start plat index duration')

    # Creates plat intervals and add to the corresponding node lists.
    all_tasks = {}
    node_to_intervals = collections.defaultdict(list)

    for plat_id, plat in enumerate(plats_data):
        for task_id, task in enumerate(plat):
            node = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (plat_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[plat_id, task_id] = task_type(start=start_var,
                                                    end=end_var,
                                                    interval=interval_var)
            node_to_intervals[node].append(interval_var)

    # Create and add disjunctive constraints.
    for node in all_nodes:
        model.AddNoOverlap(node_to_intervals[node])

    # Precedences inside a plat.
    for plat_id, plat in enumerate(plats_data):
        for task_id in range(len(plat) - 1):
            model.Add(all_tasks[plat_id, task_id +
                                1].start >= all_tasks[plat_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[plat_id, len(plat) - 1].end
        for plat_id, plat in enumerate(plats_data)
    ])
    model.Minimize(obj_var)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Create one list of assigned tasks per node.
        assigned_plats = collections.defaultdict(list)
        for plat_id, plat in enumerate(plats_data):
            for task_id, task in enumerate(plat):
                node = task[0]
                assigned_plats[node].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[plat_id, task_id].start),
                        plat=plat_id,
                        index=task_id,
                        duration=task[1]))

        # Create per node output lines.
        output = ''
        for node in all_nodes:
            # Sort by starting time.
            assigned_plats[node].sort()
            sol_line_tasks = 'node ' + str(node) + ': '
            sol_line = '           '

            for assigned_task in assigned_plats[node]:
                name = 'plat_%i_%i' % (assigned_task.plat, assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-10s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-10s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        # Finally print the solution found.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print(output)

def reservationSimulation(platoon, step):
    rc = []
    rta = []
    rtd = []
    s = platoon.getMaxSpeed()
    dint = s * step
    t = 0
    while platoon.isInIntersection():
        rc.append([cell not in rc for cell in platoon.getCells()])
        rta.append(t - 1)
        rtd.append(t + 1)
        t += 1


