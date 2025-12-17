# crossword_solver.py
import copy
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import networkx as nx

# ---------------- Puzzle input ----------------
grid = [
    "1_2_3",
    "BB_B_",
    "B4___",
    "BB_BB"
]

word_list = [
    "astar","happy","hello","hoses",   # length 5
    "live","load","loom","peal","peel","save","talk",  # length 4
    "ant","oak","old"  # length 3
]

# ---------------- Utilities & parsing ----------------
R = len(grid)
C = len(grid[0])

def is_block(r, c):
    return grid[r][c] == 'B'

# Treat digits and underscores as fillable blanks.
def is_fillable(r, c):
    ch = grid[r][c]
    return ch != 'B'  # any non-B is fillable (digits or _)

def find_slots(min_length=3):
    """Return slot dicts (name, orient, cells, length) for slots of length >= min_length."""
    slots = []
    counter = 1
    # Across
    for r in range(R):
        c = 0
        while c < C:
            if is_fillable(r, c):
                start = c
                while c < C and is_fillable(r, c):
                    c += 1
                length = c - start
                if length >= min_length:
                    slots.append({
                        "name": f"A{counter}",
                        "orient": "across",
                        "cells": [(r, cc) for cc in range(start, start + length)],
                        "length": length
                    })
                    counter += 1
            else:
                c += 1
    # Down
    for c in range(C):
        r = 0
        while r < R:
            if is_fillable(r, c):
                start = r
                while r < R and is_fillable(r, c):
                    r += 1
                length = r - start
                if length >= min_length:
                    slots.append({
                        "name": f"D{counter}",
                        "orient": "down",
                        "cells": [(rr, c) for rr in range(start, start + length)],
                        "length": length
                    })
                    counter += 1
            else:
                r += 1
    return slots

slots = find_slots(min_length=3)

print("Discovered slots:")
for s in slots:
    print(f"  {s['name']:3} {s['orient']:6} len={s['length']} cells={s['cells']}")
print()

# ---------------- Domains by length ----------------
domains = {}
for s in slots:
    L = s["length"]
    domains[s["name"]] = [w for w in word_list if len(w) == L]

print("Initial domains (by slot):")
for v, d in domains.items():
    print(f"  {v}: {d}")
print()

# ---------------- Intersections (constraints) ----------------
vars_by_cell = defaultdict(list)
for s in slots:
    for idx, (r, c) in enumerate(s["cells"]):
        vars_by_cell[(r, c)].append((s["name"], idx))

intersections = {}   # (v1, v2) -> (i1, i2)
for cell, entries in vars_by_cell.items():
    if len(entries) > 1:
        for i in range(len(entries)):
            for j in range(i+1, len(entries)):
                v1, i1 = entries[i]
                v2, i2 = entries[j]
                intersections[(v1, v2)] = (i1, i2)
                intersections[(v2, v1)] = (i2, i1)

print("Intersections (var1,var2) -> (index_in_var1, index_in_var2):")
for k, v in intersections.items():
    print(f"  {k} -> {v}")
print()

# ---------------- Graph drawing utility ----------------
def draw_constraint_graph(assign=None, title="Constraint graph"):
    G = nx.Graph()
    for s in slots:
        G.add_node(s["name"])
    for (v1, v2) in set((a,b) if a<b else (b,a) for (a,b) in intersections.keys()):
        if v1 != v2:
            G.add_edge(v1, v2)
    pos = nx.spring_layout(G, seed=1)
    node_colors = None
    if assign:
        # color by assigned word (map to unique colors)
        palette = ["#ff9999", "#99ff99", "#9999ff", "#ffcc99", "#c2c2f0", "#ffb3e6"]
        color_map = {}
        idx = 0
        for n in G.nodes():
            if n in assign:
                color_map[n] = palette[idx % len(palette)]; idx += 1
            else:
                color_map[n] = "lightgray"
        node_colors = [color_map[n] for n in G.nodes()]
    plt.figure(figsize=(6,4))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, edge_color='gray', font_weight='bold')
    plt.title(title)
    plt.show()

# ---------------- Consistency check ----------------
def consistent_assignment(assign, var, word):
    """Check compatibility of word for var with already assigned neighbors."""
    for other_var, other_word in assign.items():
        if (var, other_var) in intersections:
            i1, i2 = intersections[(var, other_var)]
            if word[i1] != other_word[i2]:
                return False
    return True

# ---------------- Plain backtracking ----------------
plain_steps = 0
def backtrack_plain(assign, domains_local):
    global plain_steps
    plain_steps += 1
    if len(assign) == len(domains_local):
        return assign
    # pick first unassigned variable
    for v in domains_local:
        if v not in assign:
            var = v; break
    for w in domains_local[var]:
        if consistent_assignment(assign, var, w):
            assign[var] = w
            result = backtrack_plain(assign, domains_local)
            if result:
                return result
            del assign[var]
    return None

# ---------------- MRV + LCV helpers ----------------
mrv_lcv_steps = 0
def select_var_mrv(domains_local, assign):
    unassigned = [v for v in domains_local if v not in assign]
    return min(unassigned, key=lambda v: len(domains_local[v]))

def order_values_lcv(var, domains_local, assign):
    """Return domain values ordered by least-constraining-value heuristic (fewer neighbor eliminations first)."""
    def ruled_out_count(value):
        count = 0
        for (v1, v2), (i1, i2) in intersections.items():
            if v1 == var:
                nbr = v2
                if nbr in assign: continue
                for w in domains_local[nbr]:
                    if value[i1] != w[i2]:
                        count += 1
        return count
    vals = list(domains_local[var])
    vals.sort(key=lambda val: ruled_out_count(val))
    return vals

def backtrack_mrv_lcv(assign, domains_local):
    global mrv_lcv_steps
    mrv_lcv_steps += 1
    if len(assign) == len(domains_local):
        return assign
    var = select_var_mrv(domains_local, assign)
    for val in order_values_lcv(var, domains_local, assign):
        if consistent_assignment(assign, var, val):
            assign[var] = val
            result = backtrack_mrv_lcv(assign, domains_local)
            if result:
                return result
            del assign[var]
    return None

# ---------------- AC-3 (arc consistency) ----------------
def ac3(domains_local, log=None):
    """In-place AC-3. domains_local is dict var->list of words. Returns True if no domain empty."""
    queue = deque()
    for (xi, xj) in intersections.keys():
        queue.append((xi, xj))
    while queue:
        xi, xj = queue.popleft()
        i_idx, j_idx = intersections[(xi, xj)]
        revised = False
        new_dom = []
        for a in domains_local[xi]:
            if any(a[i_idx] == b[j_idx] for b in domains_local[xj]):
                new_dom.append(a)
        if len(new_dom) < len(domains_local[xi]):
            removed = set(domains_local[xi]) - set(new_dom)
            domains_local[xi] = new_dom
            revised = True
            if log is not None:
                log.append(f"AC-3 pruned {xi}: removed {sorted(list(removed))}")
        if revised:
            # add arcs (xk, xi) for all neighbors xk != xj
            for (xk, xk2), (k1,k2) in intersections.items():
                if xk2 == xi and xk != xj:
                    queue.append((xk, xi))
    # fail if any domain empty
    return all(len(domains_local[v]) > 0 for v in domains_local)

# ---------------- Backtracking with MRV+LCV+AC3 ----------------
ac3_steps = 0
def backtrack_mrv_lcv_ac3(assign, domains_local, log):
    global ac3_steps
    ac3_steps += 1
    if len(assign) == len(domains_local):
        return assign
    # MRV pick
    var = select_var_mrv(domains_local, assign)
    for val in order_values_lcv(var, domains_local, assign):
        if not consistent_assignment(assign, var, val):
            continue
        # snapshot domains & assign var = [val]
        new_domains = copy.deepcopy(domains_local)
        new_domains[var] = [val]
        # forward prune neighbors immediately
        for (v1, v2), (i1, i2) in intersections.items():
            if v1 == var:
                nbr = v2
                new_domains[nbr] = [w for w in new_domains[nbr] if w[i2] == val[i1]]
        log.append(f"Assign {var}='{val}' -> forward-pruned neighbors")
        # run AC-3 to enforce further arc consistency
        ac3_log = []
        ok = ac3(new_domains, ac3_log)
        log.extend(ac3_log)
        if not ok:
            log.append(f"After assignment {var}='{val}' -> contradiction (empty domain). Backtrack.")
            continue
        assign[var] = val
        result = backtrack_mrv_lcv_ac3(assign, new_domains, log)
        if result:
            return result
        del assign[var]
    return None

# ---------------- Run solvers ----------------
print("=== Solver: Plain backtracking ===")
plain_steps = 0
plain_solution = backtrack_plain({}, copy.deepcopy(domains))
print("Plain solution:", plain_solution)
print("Plain recursive calls:", plain_steps)
print()

print("=== Solver: MRV + LCV ===")
mrv_lcv_steps = 0
mrv_solution = backtrack_mrv_lcv({}, copy.deepcopy(domains))
print("MRV+LCV solution:", mrv_solution)
print("MRV+LCV recursive calls:", mrv_lcv_steps)
print()

print("=== Solver: MRV + LCV + AC-3 ===")
domains_ac3 = copy.deepcopy(domains)
ac3_initial_log = []
ok_init = ac3(domains_ac3, ac3_initial_log)
print("Initial AC-3 success:", ok_init)
print("Initial AC-3 log:")
for line in ac3_initial_log:
    print("  ", line)
print("Domains after initial AC-3:")
for v, d in domains_ac3.items():
    print("  ", v, d)
print()

ac3_log_main = []
ac3_solution = backtrack_mrv_lcv_ac3({}, domains_ac3, ac3_log_main)
print("MRV+LCV+AC3 solution:", ac3_solution)
print("MRV+LCV+AC3 recursive calls:", ac3_steps)
print("AC-3 propagation log during search:")
for line in ac3_log_main:
    print("  ", line)
print()

# choose best solution to visualize (prefer AC3 result)
final_solution = ac3_solution or mrv_solution or plain_solution
if final_solution:
    print("Final solution chosen for visualization:")
    for k, v in final_solution.items():
        print(f"  {k}: {v}")
else:
    print("No solution found by any method.")

# ---------------- Visualize constraint graph and filled grid ----------------
draw_constraint_graph(final_solution, title="Constraint graph (filled nodes colored)")

# Build a filled grid (with blanks for single-letter cells not filled)
filled = [['#' if is_block(r,c) else '.' for c in range(C)] for r in range(R)]
if final_solution:
    # place words
    for s in slots:
        name = s["name"]
        if name in final_solution:
            w = final_solution[name]
            for idx, (r,c) in enumerate(s["cells"]):
                filled[r][c] = w[idx]
# print filled grid
print("\nFilled grid (B=blocked shown as #):")
for row in filled:
    print(''.join(row))

# also pretty-print grid with B for blocks
print("\nOriginal grid (B=blocked):")
for r in range(R):
    print(''.join(grid[r]))
