import sys
class CSP:
    def __init__(self, vars, domains, neighbors, constraints):
        self.vars = vars
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.new_domains = {}

# define AC3 algorithm
def AC3(csp, queue=None):
    if queue is None:
        for v in csp.vars:
            csp.new_domains[v] = csp.domains[v][:]
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj):
            if len(csp.new_domains[Xi]) == 0:
                return False
            for Xk in csp.neighbors[Xi]:
                queue.append((Xk, Xi))
    return True


def revise(csp, Xi, Xj):
    removed = False
    for x in csp.new_domains[Xi][:]:
        c=0
        for y in csp.new_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                c = c+1
        if c == 0:
            csp.new_domains[Xi].remove(x)
            removed = True
    return removed


# define backtracking search
def backtracking_search(csp):
    for v in csp.vars:
        csp.new_domains[v] = csp.domains[v][:]
    assign = {}
    for key in csp.new_domains:
        if len(csp.new_domains[key]) == 1:
            assign[key] = csp.new_domains[key]
    return backtrack(assign, csp)


def backtrack(assignment, csp):
    if len(assignment) == len(csp.vars):
        ass_final= {}
        for key, value in sorted(assignment.items()):
            ass_final[key] = value
        return ass_final

    var = select_unassigned_variable(assignment, csp)
    for val in order_domain_values(var, assignment, csp):
        if num_conflicts(var, val, assignment, csp) == 0:
            assignment[var] = [val]
            csp.new_domains[var] = [val]
            infer = AC3(csp, [(var, Xk) for Xk in csp.neighbors[var]])
            if infer:
                result = backtrack(assignment, csp)
                if result is not None:
                    return result
        if var in assignment:
            del assignment[var]
            for v in csp.vars:
                csp.new_domains[v] = csp.domains[v][:]

    return None


def select_unassigned_variable(assignment, csp):
    for v in csp.vars:
        if v not in assignment:
            return v


# order domain value using least constrained values
def order_domain_values(var, assignment, csp):
    if csp.new_domains:
        domain = csp.new_domains[var]
    else:
        domain = csp.domains[var][:]
    z = [0]*len(domain)
    for i in range(len(domain)):
        z[i] = num_conflicts(var, domain[i], assignment, csp)
    z.sort()
    sorted_domains = [x for _, x in sorted(zip(z, domain))]
    return sorted_domains


# determine number of conflicts
def num_conflicts(var, val, assignment, csp):
    C = 0
    for Y in csp.neighbors[var]:
        y = assignment.get(Y, None)
        if y != None and not csp.constraints(var, [val], Y, y):
            C = C+1
    return C


## solving sudoku
# named 27 places with distinct variables
vars = 'a1 a2 a3 a4 a5 a6 a7 a8 a9 ' \
       'b1 b2 b3 b4 b5 b6 b7 b8 b9 ' \
       'c1 c2 c3 c4 c5 c6 c7 c8 c9 ' \
       'd1 d2 d3 d4 d5 d6 d7 d8 d9 ' \
       'e1 e2 e3 e4 e5 e6 e7 e8 e9 ' \
       'f1 f2 f3 f4 f5 f6 f7 f8 f9 ' \
       'g1 g2 g3 g4 g5 g6 g7 g8 g9 ' \
       'h1 h2 h3 h4 h5 h6 h7 h8 h9 ' \
       'i1 i2 i3 i4 i5 i6 i7 i8 i9 '.split()

domains = {}
# input_str = sys.argv[1]
# '0' means empty places which will be determined by the program
input_str = '000260701680070090190004500820100040004602900050003028009300074040050036703018000'
j = 0
for var in vars:
    if input_str[j] == '0':
        domains[var] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        domains[var] = [int(input_str[j])]
    j = j+1


# define constraints for sudoku
def constraints(X, x, Y, y):
    if (X == 'a1' and Y == 'a2') or (Y == 'a1' and X == 'a2'): return (x != y)
    if (X == 'a1' and Y == 'a3') or (Y == 'a1' and X == 'a3'): return (x != y)
    if (X == 'a1' and Y == 'a4') or (Y == 'a1' and X == 'a4'): return (x != y)
    if (X == 'a1' and Y == 'a5') or (Y == 'a1' and X == 'a5'): return (x != y)
    if (X == 'a1' and Y == 'a6') or (Y == 'a1' and X == 'a6'): return (x != y)
    if (X == 'a1' and Y == 'a7') or (Y == 'a1' and X == 'a7'): return (x != y)
    if (X == 'a1' and Y == 'a8') or (Y == 'a1' and X == 'a8'): return (x != y)
    if (X == 'a1' and Y == 'a9') or (Y == 'a1' and X == 'a9'): return (x != y)

    if (X == 'a1' and Y == 'b1') or (Y == 'a1' and X == 'b1'): return (x != y)
    if (X == 'a1' and Y == 'b2') or (Y == 'a1' and X == 'b2'): return (x != y)
    if (X == 'a1' and Y == 'b3') or (Y == 'a1' and X == 'b3'): return (x != y)
    if (X == 'a1' and Y == 'c1') or (Y == 'a1' and X == 'c1'): return (x != y)
    if (X == 'a1' and Y == 'c2') or (Y == 'a1' and X == 'c2'): return (x != y)
    if (X == 'a1' and Y == 'c3') or (Y == 'a1' and X == 'c3'): return (x != y)

    if (X == 'a1' and Y == 'd1') or (Y == 'a1' and X == 'd1'): return (x != y)
    if (X == 'a1' and Y == 'e1') or (Y == 'a1' and X == 'e1'): return (x != y)
    if (X == 'a1' and Y == 'f1') or (Y == 'a1' and X == 'f1'): return (x != y)
    if (X == 'a1' and Y == 'g1') or (Y == 'a1' and X == 'g1'): return (x != y)
    if (X == 'a1' and Y == 'h1') or (Y == 'a1' and X == 'h1'): return (x != y)
    if (X == 'a1' and Y == 'i1') or (Y == 'a1' and X == 'i1'): return (x != y)

    #a2
    if (X == 'a2' and Y == 'a3') or (Y == 'a2' and X == 'a3'): return (x != y)
    if (X == 'a2' and Y == 'a4') or (Y == 'a2' and X == 'a4'): return (x != y)
    if (X == 'a2' and Y == 'a5') or (Y == 'a2' and X == 'a5'): return (x != y)
    if (X == 'a2' and Y == 'a6') or (Y == 'a2' and X == 'a6'): return (x != y)
    if (X == 'a2' and Y == 'a7') or (Y == 'a2' and X == 'a7'): return (x != y)
    if (X == 'a2' and Y == 'a8') or (Y == 'a2' and X == 'a8'): return (x != y)
    if (X == 'a2' and Y == 'a9') or (Y == 'a2' and X == 'a9'): return (x != y)

    if (X == 'a2' and Y == 'b1') or (Y == 'a2' and X == 'b1'): return (x != y)
    if (X == 'a2' and Y == 'b2') or (Y == 'a2' and X == 'b2'): return (x != y)
    if (X == 'a2' and Y == 'b3') or (Y == 'a2' and X == 'b3'): return (x != y)
    if (X == 'a2' and Y == 'c1') or (Y == 'a2' and X == 'c1'): return (x != y)
    if (X == 'a2' and Y == 'c2') or (Y == 'a2' and X == 'c2'): return (x != y)
    if (X == 'a2' and Y == 'c3') or (Y == 'a2' and X == 'c3'): return (x != y)

    if (X == 'a2' and Y == 'd2') or (Y == 'a2' and X == 'd2'): return (x != y)
    if (X == 'a2' and Y == 'e2') or (Y == 'a2' and X == 'e2'): return (x != y)
    if (X == 'a2' and Y == 'f2') or (Y == 'a2' and X == 'f2'): return (x != y)
    if (X == 'a2' and Y == 'g2') or (Y == 'a2' and X == 'g2'): return (x != y)
    if (X == 'a2' and Y == 'h2') or (Y == 'a2' and X == 'h2'): return (x != y)
    if (X == 'a2' and Y == 'i2') or (Y == 'a2' and X == 'i2'): return (x != y)

    #a3
    if (X == 'a3' and Y == 'a4') or (Y == 'a3' and X == 'a4'): return (x != y)
    if (X == 'a3' and Y == 'a5') or (Y == 'a3' and X == 'a5'): return (x != y)
    if (X == 'a3' and Y == 'a6') or (Y == 'a3' and X == 'a6'): return (x != y)
    if (X == 'a3' and Y == 'a7') or (Y == 'a3' and X == 'a7'): return (x != y)
    if (X == 'a3' and Y == 'a8') or (Y == 'a3' and X == 'a8'): return (x != y)
    if (X == 'a3' and Y == 'a9') or (Y == 'a3' and X == 'a9'): return (x != y)

    if (X == 'a3' and Y == 'b1') or (Y == 'a3' and X == 'b1'): return (x != y)
    if (X == 'a3' and Y == 'b2') or (Y == 'a3' and X == 'b2'): return (x != y)
    if (X == 'a3' and Y == 'b3') or (Y == 'a3' and X == 'b3'): return (x != y)
    if (X == 'a3' and Y == 'c1') or (Y == 'a3' and X == 'c1'): return (x != y)
    if (X == 'a3' and Y == 'c2') or (Y == 'a3' and X == 'c2'): return (x != y)
    if (X == 'a3' and Y == 'c3') or (Y == 'a3' and X == 'c3'): return (x != y)

    if (X == 'a3' and Y == 'd3') or (Y == 'a3' and X == 'd3'): return (x != y)
    if (X == 'a3' and Y == 'e3') or (Y == 'a3' and X == 'e3'): return (x != y)
    if (X == 'a3' and Y == 'f3') or (Y == 'a3' and X == 'f3'): return (x != y)
    if (X == 'a3' and Y == 'g3') or (Y == 'a3' and X == 'g3'): return (x != y)
    if (X == 'a3' and Y == 'h3') or (Y == 'a3' and X == 'h3'): return (x != y)
    if (X == 'a3' and Y == 'i3') or (Y == 'a3' and X == 'i3'): return (x != y)

    #a4
    if (X == 'a4' and Y == 'a5') or (Y == 'a4' and X == 'a5'): return (x != y)
    if (X == 'a4' and Y == 'a6') or (Y == 'a4' and X == 'a6'): return (x != y)
    if (X == 'a4' and Y == 'a7') or (Y == 'a4' and X == 'a7'): return (x != y)
    if (X == 'a4' and Y == 'a8') or (Y == 'a4' and X == 'a8'): return (x != y)
    if (X == 'a4' and Y == 'a9') or (Y == 'a4' and X == 'a9'): return (x != y)

    if (X == 'a4' and Y == 'b4') or (Y == 'a4' and X == 'b4'): return (x != y)
    if (X == 'a4' and Y == 'b5') or (Y == 'a4' and X == 'b5'): return (x != y)
    if (X == 'a4' and Y == 'b6') or (Y == 'a4' and X == 'b6'): return (x != y)
    if (X == 'a4' and Y == 'c4') or (Y == 'a4' and X == 'c4'): return (x != y)
    if (X == 'a4' and Y == 'c5') or (Y == 'a4' and X == 'c5'): return (x != y)
    if (X == 'a4' and Y == 'c6') or (Y == 'a4' and X == 'c6'): return (x != y)

    if (X == 'a4' and Y == 'd4') or (Y == 'a4' and X == 'd4'): return (x != y)
    if (X == 'a4' and Y == 'e4') or (Y == 'a4' and X == 'e4'): return (x != y)
    if (X == 'a4' and Y == 'f4') or (Y == 'a4' and X == 'f4'): return (x != y)
    if (X == 'a4' and Y == 'g4') or (Y == 'a4' and X == 'g4'): return (x != y)
    if (X == 'a4' and Y == 'h4') or (Y == 'a4' and X == 'h4'): return (x != y)
    if (X == 'a4' and Y == 'i4') or (Y == 'a4' and X == 'i4'): return (x != y)

    #a5
    if (X == 'a5' and Y == 'a6') or (Y == 'a5' and X == 'a6'): return (x != y)
    if (X == 'a5' and Y == 'a7') or (Y == 'a5' and X == 'a7'): return (x != y)
    if (X == 'a5' and Y == 'a8') or (Y == 'a5' and X == 'a8'): return (x != y)
    if (X == 'a5' and Y == 'a9') or (Y == 'a5' and X == 'a9'): return (x != y)

    if (X == 'a5' and Y == 'b4') or (Y == 'a5' and X == 'b4'): return (x != y)
    if (X == 'a5' and Y == 'b5') or (Y == 'a5' and X == 'b5'): return (x != y)
    if (X == 'a5' and Y == 'b6') or (Y == 'a5' and X == 'b6'): return (x != y)
    if (X == 'a5' and Y == 'c4') or (Y == 'a5' and X == 'c4'): return (x != y)
    if (X == 'a5' and Y == 'c5') or (Y == 'a5' and X == 'c5'): return (x != y)
    if (X == 'a5' and Y == 'c6') or (Y == 'a5' and X == 'c6'): return (x != y)

    if (X == 'a5' and Y == 'd5') or (Y == 'a5' and X == 'd5'): return (x != y)
    if (X == 'a5' and Y == 'e5') or (Y == 'a5' and X == 'e5'): return (x != y)
    if (X == 'a5' and Y == 'f5') or (Y == 'a5' and X == 'f5'): return (x != y)
    if (X == 'a5' and Y == 'g5') or (Y == 'a5' and X == 'g5'): return (x != y)
    if (X == 'a5' and Y == 'h5') or (Y == 'a5' and X == 'h5'): return (x != y)
    if (X == 'a5' and Y == 'i5') or (Y == 'a5' and X == 'i5'): return (x != y)

    #a6
    if (X == 'a6' and Y == 'a7') or (Y == 'a6' and X == 'a7'): return (x != y)
    if (X == 'a6' and Y == 'a8') or (Y == 'a6' and X == 'a8'): return (x != y)
    if (X == 'a6' and Y == 'a9') or (Y == 'a6' and X == 'a9'): return (x != y)

    if (X == 'a6' and Y == 'b4') or (Y == 'a6' and X == 'b4'): return (x != y)
    if (X == 'a6' and Y == 'b5') or (Y == 'a6' and X == 'b5'): return (x != y)
    if (X == 'a6' and Y == 'b6') or (Y == 'a6' and X == 'b6'): return (x != y)
    if (X == 'a6' and Y == 'c4') or (Y == 'a6' and X == 'c4'): return (x != y)
    if (X == 'a6' and Y == 'c5') or (Y == 'a6' and X == 'c5'): return (x != y)
    if (X == 'a6' and Y == 'c6') or (Y == 'a6' and X == 'c6'): return (x != y)

    if (X == 'a6' and Y == 'd6') or (Y == 'a6' and X == 'd6'): return (x != y)
    if (X == 'a6' and Y == 'e6') or (Y == 'a6' and X == 'e6'): return (x != y)
    if (X == 'a6' and Y == 'f6') or (Y == 'a6' and X == 'f6'): return (x != y)
    if (X == 'a6' and Y == 'g6') or (Y == 'a6' and X == 'g6'): return (x != y)
    if (X == 'a6' and Y == 'h6') or (Y == 'a6' and X == 'h6'): return (x != y)
    if (X == 'a6' and Y == 'i6') or (Y == 'a6' and X == 'i6'): return (x != y)

    #a7
    if (X == 'a7' and Y == 'a8') or (Y == 'a7' and X == 'a8'): return (x != y)
    if (X == 'a7' and Y == 'a9') or (Y == 'a7' and X == 'a9'): return (x != y)

    if (X == 'a7' and Y == 'b7') or (Y == 'a7' and X == 'b7'): return (x != y)
    if (X == 'a7' and Y == 'b8') or (Y == 'a7' and X == 'b8'): return (x != y)
    if (X == 'a7' and Y == 'b9') or (Y == 'a7' and X == 'b9'): return (x != y)
    if (X == 'a7' and Y == 'c7') or (Y == 'a7' and X == 'c7'): return (x != y)
    if (X == 'a7' and Y == 'c8') or (Y == 'a7' and X == 'c8'): return (x != y)
    if (X == 'a7' and Y == 'c9') or (Y == 'a7' and X == 'c9'): return (x != y)

    if (X == 'a7' and Y == 'd7') or (Y == 'a7' and X == 'd7'): return (x != y)
    if (X == 'a7' and Y == 'e7') or (Y == 'a7' and X == 'e7'): return (x != y)
    if (X == 'a7' and Y == 'f7') or (Y == 'a7' and X == 'f7'): return (x != y)
    if (X == 'a7' and Y == 'g7') or (Y == 'a7' and X == 'g7'): return (x != y)
    if (X == 'a7' and Y == 'h7') or (Y == 'a7' and X == 'h7'): return (x != y)
    if (X == 'a7' and Y == 'i7') or (Y == 'a7' and X == 'i7'): return (x != y)

    #a8
    if (X == 'a8' and Y == 'a9') or (Y == 'a8' and X == 'a9'): return (x != y)

    if (X == 'a8' and Y == 'b7') or (Y == 'a8' and X == 'b7'): return (x != y)
    if (X == 'a8' and Y == 'b8') or (Y == 'a8' and X == 'b8'): return (x != y)
    if (X == 'a8' and Y == 'b9') or (Y == 'a8' and X == 'b9'): return (x != y)
    if (X == 'a8' and Y == 'c7') or (Y == 'a8' and X == 'c7'): return (x != y)
    if (X == 'a8' and Y == 'c8') or (Y == 'a8' and X == 'c8'): return (x != y)
    if (X == 'a8' and Y == 'c9') or (Y == 'a8' and X == 'c9'): return (x != y)

    if (X == 'a8' and Y == 'd8') or (Y == 'a8' and X == 'd8'): return (x != y)
    if (X == 'a8' and Y == 'e8') or (Y == 'a8' and X == 'e8'): return (x != y)
    if (X == 'a8' and Y == 'f8') or (Y == 'a8' and X == 'f8'): return (x != y)
    if (X == 'a8' and Y == 'g8') or (Y == 'a8' and X == 'g8'): return (x != y)
    if (X == 'a8' and Y == 'h8') or (Y == 'a8' and X == 'h8'): return (x != y)
    if (X == 'a8' and Y == 'i8') or (Y == 'a8' and X == 'i8'): return (x != y)

    #a9
    if (X == 'a9' and Y == 'b7') or (Y == 'a9' and X == 'b7'): return (x != y)
    if (X == 'a9' and Y == 'b8') or (Y == 'a9' and X == 'b8'): return (x != y)
    if (X == 'a9' and Y == 'b9') or (Y == 'a9' and X == 'b9'): return (x != y)
    if (X == 'a9' and Y == 'c7') or (Y == 'a9' and X == 'c7'): return (x != y)
    if (X == 'a9' and Y == 'c8') or (Y == 'a9' and X == 'c8'): return (x != y)
    if (X == 'a9' and Y == 'c9') or (Y == 'a9' and X == 'c9'): return (x != y)

    if (X == 'a9' and Y == 'd9') or (Y == 'a9' and X == 'd9'): return (x != y)
    if (X == 'a9' and Y == 'e9') or (Y == 'a9' and X == 'e9'): return (x != y)
    if (X == 'a9' and Y == 'f9') or (Y == 'a9' and X == 'f9'): return (x != y)
    if (X == 'a9' and Y == 'g9') or (Y == 'a9' and X == 'g9'): return (x != y)
    if (X == 'a9' and Y == 'h9') or (Y == 'a9' and X == 'h9'): return (x != y)
    if (X == 'a9' and Y == 'i9') or (Y == 'a9' and X == 'i9'): return (x != y)

    #b1
    if (X == 'b1' and Y == 'b2') or (Y == 'b1' and X == 'b2'): return (x != y)
    if (X == 'b1' and Y == 'b3') or (Y == 'b1' and X == 'b3'): return (x != y)
    if (X == 'b1' and Y == 'b4') or (Y == 'b1' and X == 'b4'): return (x != y)
    if (X == 'b1' and Y == 'b5') or (Y == 'b1' and X == 'b5'): return (x != y)
    if (X == 'b1' and Y == 'b6') or (Y == 'b1' and X == 'b6'): return (x != y)
    if (X == 'b1' and Y == 'b7') or (Y == 'b1' and X == 'b7'): return (x != y)
    if (X == 'b1' and Y == 'b8') or (Y == 'b1' and X == 'b8'): return (x != y)
    if (X == 'b1' and Y == 'b9') or (Y == 'b1' and X == 'b9'): return (x != y)

    if (X == 'b1' and Y == 'c1') or (Y == 'b1' and X == 'c1'): return (x != y)
    if (X == 'b1' and Y == 'c2') or (Y == 'b1' and X == 'c2'): return (x != y)
    if (X == 'b1' and Y == 'c3') or (Y == 'b1' and X == 'c3'): return (x != y)

    if (X == 'b1' and Y == 'd1') or (Y == 'b1' and X == 'd1'): return (x != y)
    if (X == 'b1' and Y == 'e1') or (Y == 'b1' and X == 'e1'): return (x != y)
    if (X == 'b1' and Y == 'f1') or (Y == 'b1' and X == 'f1'): return (x != y)
    if (X == 'b1' and Y == 'g1') or (Y == 'b1' and X == 'g1'): return (x != y)
    if (X == 'b1' and Y == 'h1') or (Y == 'b1' and X == 'h1'): return (x != y)
    if (X == 'b1' and Y == 'i1') or (Y == 'b1' and X == 'i1'): return (x != y)

    #b2
    if (X == 'b2' and Y == 'b3') or (Y == 'b2' and X == 'b3'): return (x != y)
    if (X == 'b2' and Y == 'b4') or (Y == 'b2' and X == 'b4'): return (x != y)
    if (X == 'b2' and Y == 'b5') or (Y == 'b2' and X == 'b5'): return (x != y)
    if (X == 'b2' and Y == 'b6') or (Y == 'b2' and X == 'b6'): return (x != y)
    if (X == 'b2' and Y == 'b7') or (Y == 'b2' and X == 'b7'): return (x != y)
    if (X == 'b2' and Y == 'b8') or (Y == 'b2' and X == 'b8'): return (x != y)
    if (X == 'b2' and Y == 'b9') or (Y == 'b2' and X == 'b9'): return (x != y)

    if (X == 'b2' and Y == 'c1') or (Y == 'b2' and X == 'c1'): return (x != y)
    if (X == 'b2' and Y == 'c2') or (Y == 'b2' and X == 'c2'): return (x != y)
    if (X == 'b2' and Y == 'c3') or (Y == 'b2' and X == 'c3'): return (x != y)

    if (X == 'b2' and Y == 'd2') or (Y == 'b2' and X == 'd2'): return (x != y)
    if (X == 'b2' and Y == 'e2') or (Y == 'b2' and X == 'e2'): return (x != y)
    if (X == 'b2' and Y == 'f2') or (Y == 'b2' and X == 'f2'): return (x != y)
    if (X == 'b2' and Y == 'g2') or (Y == 'b2' and X == 'g2'): return (x != y)
    if (X == 'b2' and Y == 'h2') or (Y == 'b2' and X == 'h2'): return (x != y)
    if (X == 'b2' and Y == 'i2') or (Y == 'b2' and X == 'i2'): return (x != y)

    #b3
    if (X == 'b3' and Y == 'b4') or (Y == 'b3' and X == 'b4'): return (x != y)
    if (X == 'b3' and Y == 'b5') or (Y == 'b3' and X == 'b5'): return (x != y)
    if (X == 'b3' and Y == 'b6') or (Y == 'b3' and X == 'b6'): return (x != y)
    if (X == 'b3' and Y == 'b7') or (Y == 'b3' and X == 'b7'): return (x != y)
    if (X == 'b3' and Y == 'b8') or (Y == 'b3' and X == 'b8'): return (x != y)
    if (X == 'b3' and Y == 'b9') or (Y == 'b3' and X == 'b9'): return (x != y)

    if (X == 'b3' and Y == 'c1') or (Y == 'b3' and X == 'c1'): return (x != y)
    if (X == 'b3' and Y == 'c2') or (Y == 'b3' and X == 'c2'): return (x != y)
    if (X == 'b3' and Y == 'c3') or (Y == 'b3' and X == 'c3'): return (x != y)

    if (X == 'b3' and Y == 'd3') or (Y == 'b3' and X == 'd3'): return (x != y)
    if (X == 'b3' and Y == 'e3') or (Y == 'b3' and X == 'e3'): return (x != y)
    if (X == 'b3' and Y == 'f3') or (Y == 'b3' and X == 'f3'): return (x != y)
    if (X == 'b3' and Y == 'g3') or (Y == 'b3' and X == 'g3'): return (x != y)
    if (X == 'b3' and Y == 'h3') or (Y == 'b3' and X == 'h3'): return (x != y)
    if (X == 'b3' and Y == 'i3') or (Y == 'b3' and X == 'i3'): return (x != y)

    #b4
    if (X == 'b4' and Y == 'b5') or (Y == 'b4' and X == 'b5'): return (x != y)
    if (X == 'b4' and Y == 'b6') or (Y == 'b4' and X == 'b6'): return (x != y)
    if (X == 'b4' and Y == 'b7') or (Y == 'b4' and X == 'b7'): return (x != y)
    if (X == 'b4' and Y == 'b8') or (Y == 'b4' and X == 'b8'): return (x != y)
    if (X == 'b4' and Y == 'b9') or (Y == 'b4' and X == 'b9'): return (x != y)

    if (X == 'b4' and Y == 'c4') or (Y == 'b4' and X == 'c4'): return (x != y)
    if (X == 'b4' and Y == 'c5') or (Y == 'b4' and X == 'c5'): return (x != y)
    if (X == 'b4' and Y == 'c6') or (Y == 'b4' and X == 'c6'): return (x != y)

    if (X == 'b4' and Y == 'd4') or (Y == 'b4' and X == 'd4'): return (x != y)
    if (X == 'b4' and Y == 'e4') or (Y == 'b4' and X == 'e4'): return (x != y)
    if (X == 'b4' and Y == 'f4') or (Y == 'b4' and X == 'f4'): return (x != y)
    if (X == 'b4' and Y == 'g4') or (Y == 'b4' and X == 'g4'): return (x != y)
    if (X == 'b4' and Y == 'h4') or (Y == 'b4' and X == 'h4'): return (x != y)
    if (X == 'b4' and Y == 'i4') or (Y == 'b4' and X == 'i4'): return (x != y)

    #b5
    if (X == 'b5' and Y == 'b6') or (Y == 'b5' and X == 'b6'): return (x != y)
    if (X == 'b5' and Y == 'b7') or (Y == 'b5' and X == 'b7'): return (x != y)
    if (X == 'b5' and Y == 'b8') or (Y == 'b5' and X == 'b8'): return (x != y)
    if (X == 'b5' and Y == 'b9') or (Y == 'b5' and X == 'b9'): return (x != y)

    if (X == 'b5' and Y == 'c4') or (Y == 'b5' and X == 'c4'): return (x != y)
    if (X == 'b5' and Y == 'c5') or (Y == 'b5' and X == 'c5'): return (x != y)
    if (X == 'b5' and Y == 'c6') or (Y == 'b5' and X == 'c6'): return (x != y)

    if (X == 'b5' and Y == 'd5') or (Y == 'b5' and X == 'd5'): return (x != y)
    if (X == 'b5' and Y == 'e5') or (Y == 'b5' and X == 'e5'): return (x != y)
    if (X == 'b5' and Y == 'f5') or (Y == 'b5' and X == 'f5'): return (x != y)
    if (X == 'b5' and Y == 'g5') or (Y == 'b5' and X == 'g5'): return (x != y)
    if (X == 'b5' and Y == 'h5') or (Y == 'b5' and X == 'h5'): return (x != y)
    if (X == 'b5' and Y == 'i5') or (Y == 'b5' and X == 'i5'): return (x != y)

    #b6
    if (X == 'b6' and Y == 'b7') or (Y == 'b6' and X == 'b7'): return (x != y)
    if (X == 'b6' and Y == 'b8') or (Y == 'b6' and X == 'b8'): return (x != y)
    if (X == 'b6' and Y == 'b9') or (Y == 'b6' and X == 'b9'): return (x != y)

    if (X == 'b6' and Y == 'c4') or (Y == 'b6' and X == 'c4'): return (x != y)
    if (X == 'b6' and Y == 'c5') or (Y == 'b6' and X == 'c5'): return (x != y)
    if (X == 'b6' and Y == 'c6') or (Y == 'b6' and X == 'c6'): return (x != y)

    if (X == 'b6' and Y == 'd6') or (Y == 'b6' and X == 'd6'): return (x != y)
    if (X == 'b6' and Y == 'e6') or (Y == 'b6' and X == 'e6'): return (x != y)
    if (X == 'b6' and Y == 'f6') or (Y == 'b6' and X == 'f6'): return (x != y)
    if (X == 'b6' and Y == 'g6') or (Y == 'b6' and X == 'g6'): return (x != y)
    if (X == 'b6' and Y == 'h6') or (Y == 'b6' and X == 'h6'): return (x != y)
    if (X == 'b6' and Y == 'i6') or (Y == 'b6' and X == 'i6'): return (x != y)

    #b7
    if (X == 'b7' and Y == 'b8') or (Y == 'b7' and X == 'b8'): return (x != y)
    if (X == 'b7' and Y == 'b9') or (Y == 'b7' and X == 'b9'): return (x != y)

    if (X == 'b7' and Y == 'c7') or (Y == 'b7' and X == 'c7'): return (x != y)
    if (X == 'b7' and Y == 'c8') or (Y == 'b7' and X == 'c8'): return (x != y)
    if (X == 'b7' and Y == 'c9') or (Y == 'b7' and X == 'c9'): return (x != y)

    if (X == 'b7' and Y == 'd7') or (Y == 'b7' and X == 'd7'): return (x != y)
    if (X == 'b7' and Y == 'e7') or (Y == 'b7' and X == 'e7'): return (x != y)
    if (X == 'b7' and Y == 'f7') or (Y == 'b7' and X == 'f7'): return (x != y)
    if (X == 'b7' and Y == 'g7') or (Y == 'b7' and X == 'g7'): return (x != y)
    if (X == 'b7' and Y == 'h7') or (Y == 'b7' and X == 'h7'): return (x != y)
    if (X == 'b7' and Y == 'i7') or (Y == 'b7' and X == 'i7'): return (x != y)

    #b8
    if (X == 'b8' and Y == 'b9') or (Y == 'b8' and X == 'b9'): return (x != y)

    if (X == 'b8' and Y == 'c7') or (Y == 'b8' and X == 'c7'): return (x != y)
    if (X == 'b8' and Y == 'c8') or (Y == 'b8' and X == 'c8'): return (x != y)
    if (X == 'b8' and Y == 'c9') or (Y == 'b8' and X == 'c9'): return (x != y)

    if (X == 'b8' and Y == 'd8') or (Y == 'b8' and X == 'd8'): return (x != y)
    if (X == 'b8' and Y == 'e8') or (Y == 'b8' and X == 'e8'): return (x != y)
    if (X == 'b8' and Y == 'f8') or (Y == 'b8' and X == 'f8'): return (x != y)
    if (X == 'b8' and Y == 'g8') or (Y == 'b8' and X == 'g8'): return (x != y)
    if (X == 'b8' and Y == 'h8') or (Y == 'b8' and X == 'h8'): return (x != y)
    if (X == 'b8' and Y == 'i8') or (Y == 'b8' and X == 'i8'): return (x != y)

    #b9
    if (X == 'b9' and Y == 'c7') or (Y == 'b9' and X == 'c7'): return (x != y)
    if (X == 'b9' and Y == 'c8') or (Y == 'b9' and X == 'c8'): return (x != y)
    if (X == 'b9' and Y == 'c9') or (Y == 'b9' and X == 'c9'): return (x != y)

    if (X == 'b9' and Y == 'd9') or (Y == 'b9' and X == 'd9'): return (x != y)
    if (X == 'b9' and Y == 'e9') or (Y == 'b9' and X == 'e9'): return (x != y)
    if (X == 'b9' and Y == 'f9') or (Y == 'b9' and X == 'f9'): return (x != y)
    if (X == 'b9' and Y == 'g9') or (Y == 'b9' and X == 'g9'): return (x != y)
    if (X == 'b9' and Y == 'h9') or (Y == 'b9' and X == 'h9'): return (x != y)
    if (X == 'b9' and Y == 'i9') or (Y == 'b9' and X == 'i9'): return (x != y)

    #c1
    if (X == 'c1' and Y == 'c2') or (Y == 'c1' and X == 'c2'): return (x != y)
    if (X == 'c1' and Y == 'c3') or (Y == 'c1' and X == 'c3'): return (x != y)
    if (X == 'c1' and Y == 'c4') or (Y == 'c1' and X == 'c4'): return (x != y)
    if (X == 'c1' and Y == 'c5') or (Y == 'c1' and X == 'c5'): return (x != y)
    if (X == 'c1' and Y == 'c6') or (Y == 'c1' and X == 'c6'): return (x != y)
    if (X == 'c1' and Y == 'c7') or (Y == 'c1' and X == 'c7'): return (x != y)
    if (X == 'c1' and Y == 'c8') or (Y == 'c1' and X == 'c8'): return (x != y)
    if (X == 'c1' and Y == 'c9') or (Y == 'c1' and X == 'c9'): return (x != y)

    if (X == 'c1' and Y == 'd1') or (Y == 'c1' and X == 'd1'): return (x != y)
    if (X == 'c1' and Y == 'e1') or (Y == 'c1' and X == 'e1'): return (x != y)
    if (X == 'c1' and Y == 'f1') or (Y == 'c1' and X == 'f1'): return (x != y)
    if (X == 'c1' and Y == 'g1') or (Y == 'c1' and X == 'g1'): return (x != y)
    if (X == 'c1' and Y == 'h1') or (Y == 'c1' and X == 'h1'): return (x != y)
    if (X == 'c1' and Y == 'i1') or (Y == 'c1' and X == 'i1'): return (x != y)

    #c2
    if (X == 'c2' and Y == 'c3') or (Y == 'c2' and X == 'c3'): return (x != y)
    if (X == 'c2' and Y == 'c4') or (Y == 'c2' and X == 'c4'): return (x != y)
    if (X == 'c2' and Y == 'c5') or (Y == 'c2' and X == 'c5'): return (x != y)
    if (X == 'c2' and Y == 'c6') or (Y == 'c2' and X == 'c6'): return (x != y)
    if (X == 'c2' and Y == 'c7') or (Y == 'c2' and X == 'c7'): return (x != y)
    if (X == 'c2' and Y == 'c8') or (Y == 'c2' and X == 'c8'): return (x != y)
    if (X == 'c2' and Y == 'c9') or (Y == 'c2' and X == 'c9'): return (x != y)

    if (X == 'c2' and Y == 'd2') or (Y == 'c2' and X == 'd2'): return (x != y)
    if (X == 'c2' and Y == 'e2') or (Y == 'c2' and X == 'e2'): return (x != y)
    if (X == 'c2' and Y == 'f2') or (Y == 'c2' and X == 'f2'): return (x != y)
    if (X == 'c2' and Y == 'g2') or (Y == 'c2' and X == 'g2'): return (x != y)
    if (X == 'c2' and Y == 'h2') or (Y == 'c2' and X == 'h2'): return (x != y)
    if (X == 'c2' and Y == 'i2') or (Y == 'c2' and X == 'i2'): return (x != y)

    #c3
    if (X == 'c3' and Y == 'c4') or (Y == 'c3' and X == 'c4'): return (x != y)
    if (X == 'c3' and Y == 'c5') or (Y == 'c3' and X == 'c5'): return (x != y)
    if (X == 'c3' and Y == 'c6') or (Y == 'c3' and X == 'c6'): return (x != y)
    if (X == 'c3' and Y == 'c7') or (Y == 'c3' and X == 'c7'): return (x != y)
    if (X == 'c3' and Y == 'c8') or (Y == 'c3' and X == 'c8'): return (x != y)
    if (X == 'c3' and Y == 'c9') or (Y == 'c3' and X == 'c9'): return (x != y)

    if (X == 'c3' and Y == 'd3') or (Y == 'c3' and X == 'd3'): return (x != y)
    if (X == 'c3' and Y == 'e3') or (Y == 'c3' and X == 'e3'): return (x != y)
    if (X == 'c3' and Y == 'f3') or (Y == 'c3' and X == 'f3'): return (x != y)
    if (X == 'c3' and Y == 'g3') or (Y == 'c3' and X == 'g3'): return (x != y)
    if (X == 'c3' and Y == 'h3') or (Y == 'c3' and X == 'h3'): return (x != y)
    if (X == 'c3' and Y == 'i3') or (Y == 'c3' and X == 'i3'): return (x != y)

    #c4
    if (X == 'c4' and Y == 'c5') or (Y == 'c4' and X == 'c5'): return (x != y)
    if (X == 'c4' and Y == 'c6') or (Y == 'c4' and X == 'c6'): return (x != y)
    if (X == 'c4' and Y == 'c7') or (Y == 'c4' and X == 'c7'): return (x != y)
    if (X == 'c4' and Y == 'c8') or (Y == 'c4' and X == 'c8'): return (x != y)
    if (X == 'c4' and Y == 'c9') or (Y == 'c4' and X == 'c9'): return (x != y)

    if (X == 'c4' and Y == 'd4') or (Y == 'c4' and X == 'd4'): return (x != y)
    if (X == 'c4' and Y == 'e4') or (Y == 'c4' and X == 'e4'): return (x != y)
    if (X == 'c4' and Y == 'f4') or (Y == 'c4' and X == 'f4'): return (x != y)
    if (X == 'c4' and Y == 'g4') or (Y == 'c4' and X == 'g4'): return (x != y)
    if (X == 'c4' and Y == 'h4') or (Y == 'c4' and X == 'h4'): return (x != y)
    if (X == 'c4' and Y == 'i4') or (Y == 'c4' and X == 'i4'): return (x != y)

    #c5
    if (X == 'c5' and Y == 'c6') or (Y == 'c5' and X == 'c6'): return (x != y)
    if (X == 'c5' and Y == 'c7') or (Y == 'c5' and X == 'c7'): return (x != y)
    if (X == 'c5' and Y == 'c8') or (Y == 'c5' and X == 'c8'): return (x != y)
    if (X == 'c5' and Y == 'c9') or (Y == 'c5' and X == 'c9'): return (x != y)

    if (X == 'c5' and Y == 'd5') or (Y == 'c5' and X == 'd5'): return (x != y)
    if (X == 'c5' and Y == 'e5') or (Y == 'c5' and X == 'e5'): return (x != y)
    if (X == 'c5' and Y == 'f5') or (Y == 'c5' and X == 'f5'): return (x != y)
    if (X == 'c5' and Y == 'g5') or (Y == 'c5' and X == 'g5'): return (x != y)
    if (X == 'c5' and Y == 'h5') or (Y == 'c5' and X == 'h5'): return (x != y)
    if (X == 'c5' and Y == 'i5') or (Y == 'c5' and X == 'i5'): return (x != y)

    #c6
    if (X == 'c6' and Y == 'c7') or (Y == 'c6' and X == 'c7'): return (x != y)
    if (X == 'c6' and Y == 'c8') or (Y == 'c6' and X == 'c8'): return (x != y)
    if (X == 'c6' and Y == 'c9') or (Y == 'c6' and X == 'c9'): return (x != y)

    if (X == 'c6' and Y == 'd6') or (Y == 'c6' and X == 'd6'): return (x != y)
    if (X == 'c6' and Y == 'e6') or (Y == 'c6' and X == 'e6'): return (x != y)
    if (X == 'c6' and Y == 'f6') or (Y == 'c6' and X == 'f6'): return (x != y)
    if (X == 'c6' and Y == 'g6') or (Y == 'c6' and X == 'g6'): return (x != y)
    if (X == 'c6' and Y == 'h6') or (Y == 'c6' and X == 'h6'): return (x != y)
    if (X == 'c6' and Y == 'i6') or (Y == 'c6' and X == 'i6'): return (x != y)

    #c7
    if (X == 'c7' and Y == 'c8') or (Y == 'c7' and X == 'c8'): return (x != y)
    if (X == 'c7' and Y == 'c9') or (Y == 'c7' and X == 'c9'): return (x != y)

    if (X == 'c7' and Y == 'd7') or (Y == 'c7' and X == 'd7'): return (x != y)
    if (X == 'c7' and Y == 'e7') or (Y == 'c7' and X == 'e7'): return (x != y)
    if (X == 'c7' and Y == 'f7') or (Y == 'c7' and X == 'f7'): return (x != y)
    if (X == 'c7' and Y == 'g7') or (Y == 'c7' and X == 'g7'): return (x != y)
    if (X == 'c7' and Y == 'h7') or (Y == 'c7' and X == 'h7'): return (x != y)
    if (X == 'c7' and Y == 'i7') or (Y == 'c7' and X == 'i7'): return (x != y)

    #c8
    if (X == 'c8' and Y == 'c9') or (Y == 'c8' and X == 'c9'): return (x != y)

    if (X == 'c8' and Y == 'd8') or (Y == 'c8' and X == 'd8'): return (x != y)
    if (X == 'c8' and Y == 'e8') or (Y == 'c8' and X == 'e8'): return (x != y)
    if (X == 'c8' and Y == 'f8') or (Y == 'c8' and X == 'f8'): return (x != y)
    if (X == 'c8' and Y == 'g8') or (Y == 'c8' and X == 'g8'): return (x != y)
    if (X == 'c8' and Y == 'h8') or (Y == 'c8' and X == 'h8'): return (x != y)
    if (X == 'c8' and Y == 'i8') or (Y == 'c8' and X == 'i8'): return (x != y)

    #c9
    if (X == 'c9' and Y == 'd9') or (Y == 'c9' and X == 'd9'): return (x != y)
    if (X == 'c9' and Y == 'e9') or (Y == 'c9' and X == 'e9'): return (x != y)
    if (X == 'c9' and Y == 'f9') or (Y == 'c9' and X == 'f9'): return (x != y)
    if (X == 'c9' and Y == 'g9') or (Y == 'c9' and X == 'g9'): return (x != y)
    if (X == 'c9' and Y == 'h9') or (Y == 'c9' and X == 'h9'): return (x != y)
    if (X == 'c9' and Y == 'i9') or (Y == 'c9' and X == 'i9'): return (x != y)

    #d1
    if (X == 'd1' and Y == 'd2') or (Y == 'd1' and X == 'd2'): return (x != y)
    if (X == 'd1' and Y == 'd3') or (Y == 'd1' and X == 'd3'): return (x != y)
    if (X == 'd1' and Y == 'd4') or (Y == 'd1' and X == 'd4'): return (x != y)
    if (X == 'd1' and Y == 'd5') or (Y == 'd1' and X == 'd5'): return (x != y)
    if (X == 'd1' and Y == 'd6') or (Y == 'd1' and X == 'd6'): return (x != y)
    if (X == 'd1' and Y == 'd7') or (Y == 'd1' and X == 'd7'): return (x != y)
    if (X == 'd1' and Y == 'd8') or (Y == 'd1' and X == 'd8'): return (x != y)
    if (X == 'd1' and Y == 'd9') or (Y == 'd1' and X == 'd9'): return (x != y)

    if (X == 'd1' and Y == 'e1') or (Y == 'd1' and X == 'e1'): return (x != y)
    if (X == 'd1' and Y == 'e2') or (Y == 'd1' and X == 'e2'): return (x != y)
    if (X == 'd1' and Y == 'e3') or (Y == 'd1' and X == 'e3'): return (x != y)
    if (X == 'd1' and Y == 'f1') or (Y == 'd1' and X == 'f1'): return (x != y)
    if (X == 'd1' and Y == 'f2') or (Y == 'd1' and X == 'f2'): return (x != y)
    if (X == 'd1' and Y == 'f3') or (Y == 'd1' and X == 'f3'): return (x != y)

    if (X == 'd1' and Y == 'g1') or (Y == 'd1' and X == 'g1'): return (x != y)
    if (X == 'd1' and Y == 'h1') or (Y == 'd1' and X == 'h1'): return (x != y)
    if (X == 'd1' and Y == 'i1') or (Y == 'd1' and X == 'i1'): return (x != y)

    #d2
    if (X == 'd2' and Y == 'd3') or (Y == 'd2' and X == 'd3'): return (x != y)
    if (X == 'd2' and Y == 'd4') or (Y == 'd2' and X == 'd4'): return (x != y)
    if (X == 'd2' and Y == 'd5') or (Y == 'd2' and X == 'd5'): return (x != y)
    if (X == 'd2' and Y == 'd6') or (Y == 'd2' and X == 'd6'): return (x != y)
    if (X == 'd2' and Y == 'd7') or (Y == 'd2' and X == 'd7'): return (x != y)
    if (X == 'd2' and Y == 'd8') or (Y == 'd2' and X == 'd8'): return (x != y)
    if (X == 'd2' and Y == 'd9') or (Y == 'd2' and X == 'd9'): return (x != y)

    if (X == 'd2' and Y == 'e1') or (Y == 'd2' and X == 'e1'): return (x != y)
    if (X == 'd2' and Y == 'e2') or (Y == 'd2' and X == 'e2'): return (x != y)
    if (X == 'd2' and Y == 'e3') or (Y == 'd2' and X == 'e3'): return (x != y)
    if (X == 'd2' and Y == 'f1') or (Y == 'd2' and X == 'f1'): return (x != y)
    if (X == 'd2' and Y == 'f2') or (Y == 'd2' and X == 'f2'): return (x != y)
    if (X == 'd2' and Y == 'f3') or (Y == 'd2' and X == 'f3'): return (x != y)

    if (X == 'd2' and Y == 'g2') or (Y == 'd2' and X == 'g2'): return (x != y)
    if (X == 'd2' and Y == 'h2') or (Y == 'd2' and X == 'h2'): return (x != y)
    if (X == 'd2' and Y == 'i2') or (Y == 'd2' and X == 'i2'): return (x != y)

    #d3
    if (X == 'd3' and Y == 'd4') or (Y == 'd3' and X == 'd4'): return (x != y)
    if (X == 'd3' and Y == 'd5') or (Y == 'd3' and X == 'd5'): return (x != y)
    if (X == 'd3' and Y == 'd6') or (Y == 'd3' and X == 'd6'): return (x != y)
    if (X == 'd3' and Y == 'd7') or (Y == 'd3' and X == 'd7'): return (x != y)
    if (X == 'd3' and Y == 'd8') or (Y == 'd3' and X == 'd8'): return (x != y)
    if (X == 'd3' and Y == 'd9') or (Y == 'd3' and X == 'd9'): return (x != y)

    if (X == 'd3' and Y == 'e1') or (Y == 'd3' and X == 'e1'): return (x != y)
    if (X == 'd3' and Y == 'e2') or (Y == 'd3' and X == 'e2'): return (x != y)
    if (X == 'd3' and Y == 'e3') or (Y == 'd3' and X == 'e3'): return (x != y)
    if (X == 'd3' and Y == 'f1') or (Y == 'd3' and X == 'f1'): return (x != y)
    if (X == 'd3' and Y == 'f2') or (Y == 'd3' and X == 'f2'): return (x != y)
    if (X == 'd3' and Y == 'f3') or (Y == 'd3' and X == 'f3'): return (x != y)

    if (X == 'd3' and Y == 'g3') or (Y == 'd3' and X == 'g3'): return (x != y)
    if (X == 'd3' and Y == 'h3') or (Y == 'd3' and X == 'h3'): return (x != y)
    if (X == 'd3' and Y == 'i3') or (Y == 'd3' and X == 'i3'): return (x != y)

    #d4
    if (X == 'd4' and Y == 'd5') or (Y == 'd4' and X == 'd5'): return (x != y)
    if (X == 'd4' and Y == 'd6') or (Y == 'd4' and X == 'd6'): return (x != y)
    if (X == 'd4' and Y == 'd7') or (Y == 'd4' and X == 'd7'): return (x != y)
    if (X == 'd4' and Y == 'd8') or (Y == 'd4' and X == 'd8'): return (x != y)
    if (X == 'd4' and Y == 'd9') or (Y == 'd4' and X == 'd9'): return (x != y)

    if (X == 'd4' and Y == 'e4') or (Y == 'd4' and X == 'e4'): return (x != y)
    if (X == 'd4' and Y == 'e5') or (Y == 'd4' and X == 'e5'): return (x != y)
    if (X == 'd4' and Y == 'e6') or (Y == 'd4' and X == 'e6'): return (x != y)
    if (X == 'd4' and Y == 'f4') or (Y == 'd4' and X == 'f4'): return (x != y)
    if (X == 'd4' and Y == 'f5') or (Y == 'd4' and X == 'f5'): return (x != y)
    if (X == 'd4' and Y == 'f6') or (Y == 'd4' and X == 'f6'): return (x != y)

    if (X == 'd4' and Y == 'g4') or (Y == 'd4' and X == 'g4'): return (x != y)
    if (X == 'd4' and Y == 'h4') or (Y == 'd4' and X == 'h4'): return (x != y)
    if (X == 'd4' and Y == 'i4') or (Y == 'd4' and X == 'i4'): return (x != y)

    #d5
    if (X == 'd5' and Y == 'd6') or (Y == 'd5' and X == 'd6'): return (x != y)
    if (X == 'd5' and Y == 'd7') or (Y == 'd5' and X == 'd7'): return (x != y)
    if (X == 'd5' and Y == 'd8') or (Y == 'd5' and X == 'd8'): return (x != y)
    if (X == 'd5' and Y == 'd9') or (Y == 'd5' and X == 'd9'): return (x != y)

    if (X == 'd5' and Y == 'e4') or (Y == 'd5' and X == 'e4'): return (x != y)
    if (X == 'd5' and Y == 'e5') or (Y == 'd5' and X == 'e5'): return (x != y)
    if (X == 'd5' and Y == 'e6') or (Y == 'd5' and X == 'e6'): return (x != y)
    if (X == 'd5' and Y == 'f4') or (Y == 'd5' and X == 'f4'): return (x != y)
    if (X == 'd5' and Y == 'f5') or (Y == 'd5' and X == 'f5'): return (x != y)
    if (X == 'd5' and Y == 'f6') or (Y == 'd5' and X == 'f6'): return (x != y)

    if (X == 'd5' and Y == 'g5') or (Y == 'd5' and X == 'g5'): return (x != y)
    if (X == 'd5' and Y == 'h5') or (Y == 'd5' and X == 'h5'): return (x != y)
    if (X == 'd5' and Y == 'i5') or (Y == 'd5' and X == 'i5'): return (x != y)

    #d6
    if (X == 'd6' and Y == 'd7') or (Y == 'd6' and X == 'd7'): return (x != y)
    if (X == 'd6' and Y == 'd8') or (Y == 'd6' and X == 'd8'): return (x != y)
    if (X == 'd6' and Y == 'd9') or (Y == 'd6' and X == 'd9'): return (x != y)

    if (X == 'd6' and Y == 'e4') or (Y == 'd6' and X == 'e4'): return (x != y)
    if (X == 'd6' and Y == 'e5') or (Y == 'd6' and X == 'e5'): return (x != y)
    if (X == 'd6' and Y == 'e6') or (Y == 'd6' and X == 'e6'): return (x != y)
    if (X == 'd6' and Y == 'f4') or (Y == 'd6' and X == 'f4'): return (x != y)
    if (X == 'd6' and Y == 'f5') or (Y == 'd6' and X == 'f5'): return (x != y)
    if (X == 'd6' and Y == 'f6') or (Y == 'd6' and X == 'f6'): return (x != y)

    if (X == 'd6' and Y == 'g6') or (Y == 'd6' and X == 'g6'): return (x != y)
    if (X == 'd6' and Y == 'h6') or (Y == 'd6' and X == 'h6'): return (x != y)
    if (X == 'd6' and Y == 'i6') or (Y == 'd6' and X == 'i6'): return (x != y)

    #d7
    if (X == 'd7' and Y == 'd8') or (Y == 'd7' and X == 'd8'): return (x != y)
    if (X == 'd7' and Y == 'd9') or (Y == 'd7' and X == 'd9'): return (x != y)

    if (X == 'd7' and Y == 'e7') or (Y == 'd7' and X == 'e7'): return (x != y)
    if (X == 'd7' and Y == 'e8') or (Y == 'd7' and X == 'e8'): return (x != y)
    if (X == 'd7' and Y == 'e9') or (Y == 'd7' and X == 'e9'): return (x != y)
    if (X == 'd7' and Y == 'f7') or (Y == 'd7' and X == 'f7'): return (x != y)
    if (X == 'd7' and Y == 'f8') or (Y == 'd7' and X == 'f8'): return (x != y)
    if (X == 'd7' and Y == 'f9') or (Y == 'd7' and X == 'f9'): return (x != y)

    if (X == 'd7' and Y == 'g7') or (Y == 'd7' and X == 'g7'): return (x != y)
    if (X == 'd7' and Y == 'h7') or (Y == 'd7' and X == 'h7'): return (x != y)
    if (X == 'd7' and Y == 'i7') or (Y == 'd7' and X == 'i7'): return (x != y)

    #d8
    if (X == 'd8' and Y == 'd9') or (Y == 'd8' and X == 'd9'): return (x != y)

    if (X == 'd8' and Y == 'e7') or (Y == 'd8' and X == 'e7'): return (x != y)
    if (X == 'd8' and Y == 'e8') or (Y == 'd8' and X == 'e8'): return (x != y)
    if (X == 'd8' and Y == 'e9') or (Y == 'd8' and X == 'e9'): return (x != y)
    if (X == 'd8' and Y == 'f7') or (Y == 'd8' and X == 'f7'): return (x != y)
    if (X == 'd8' and Y == 'f8') or (Y == 'd8' and X == 'f8'): return (x != y)
    if (X == 'd8' and Y == 'f9') or (Y == 'd8' and X == 'f9'): return (x != y)

    if (X == 'd8' and Y == 'g8') or (Y == 'd8' and X == 'g8'): return (x != y)
    if (X == 'd8' and Y == 'h8') or (Y == 'd8' and X == 'h8'): return (x != y)
    if (X == 'd8' and Y == 'i8') or (Y == 'd8' and X == 'i8'): return (x != y)

    #d9
    if (X == 'd9' and Y == 'e7') or (Y == 'd9' and X == 'e7'): return (x != y)
    if (X == 'd9' and Y == 'e8') or (Y == 'd9' and X == 'e8'): return (x != y)
    if (X == 'd9' and Y == 'e9') or (Y == 'd9' and X == 'e9'): return (x != y)
    if (X == 'd9' and Y == 'f7') or (Y == 'd9' and X == 'f7'): return (x != y)
    if (X == 'd9' and Y == 'f8') or (Y == 'd9' and X == 'f8'): return (x != y)
    if (X == 'd9' and Y == 'f9') or (Y == 'd9' and X == 'f9'): return (x != y)

    if (X == 'd9' and Y == 'g9') or (Y == 'd9' and X == 'g9'): return (x != y)
    if (X == 'd9' and Y == 'h9') or (Y == 'd9' and X == 'h9'): return (x != y)
    if (X == 'd9' and Y == 'i9') or (Y == 'd9' and X == 'i9'): return (x != y)

    #e1
    if (X == 'e1' and Y == 'e2') or (Y == 'e1' and X == 'e2'): return (x != y)
    if (X == 'e1' and Y == 'e3') or (Y == 'e1' and X == 'e3'): return (x != y)
    if (X == 'e1' and Y == 'e4') or (Y == 'e1' and X == 'e4'): return (x != y)
    if (X == 'e1' and Y == 'e5') or (Y == 'e1' and X == 'e5'): return (x != y)
    if (X == 'e1' and Y == 'e6') or (Y == 'e1' and X == 'e6'): return (x != y)
    if (X == 'e1' and Y == 'e7') or (Y == 'e1' and X == 'e7'): return (x != y)
    if (X == 'e1' and Y == 'e8') or (Y == 'e1' and X == 'e8'): return (x != y)
    if (X == 'e1' and Y == 'e9') or (Y == 'e1' and X == 'e9'): return (x != y)

    if (X == 'e1' and Y == 'f1') or (Y == 'e1' and X == 'f1'): return (x != y)
    if (X == 'e1' and Y == 'f2') or (Y == 'e1' and X == 'f2'): return (x != y)
    if (X == 'e1' and Y == 'f3') or (Y == 'e1' and X == 'f3'): return (x != y)

    if (X == 'e1' and Y == 'g1') or (Y == 'e1' and X == 'g1'): return (x != y)
    if (X == 'e1' and Y == 'h1') or (Y == 'e1' and X == 'h1'): return (x != y)
    if (X == 'e1' and Y == 'i1') or (Y == 'e1' and X == 'i1'): return (x != y)

    #e2
    if (X == 'e2' and Y == 'e3') or (Y == 'e2' and X == 'e3'): return (x != y)
    if (X == 'e2' and Y == 'e4') or (Y == 'e2' and X == 'e4'): return (x != y)
    if (X == 'e2' and Y == 'e5') or (Y == 'e2' and X == 'e5'): return (x != y)
    if (X == 'e2' and Y == 'e6') or (Y == 'e2' and X == 'e6'): return (x != y)
    if (X == 'e2' and Y == 'e7') or (Y == 'e2' and X == 'e7'): return (x != y)
    if (X == 'e2' and Y == 'e8') or (Y == 'e2' and X == 'e8'): return (x != y)
    if (X == 'e2' and Y == 'e9') or (Y == 'e2' and X == 'e9'): return (x != y)

    if (X == 'e2' and Y == 'f1') or (Y == 'e2' and X == 'f1'): return (x != y)
    if (X == 'e2' and Y == 'f2') or (Y == 'e2' and X == 'f2'): return (x != y)
    if (X == 'e2' and Y == 'f3') or (Y == 'e2' and X == 'f3'): return (x != y)

    if (X == 'e2' and Y == 'g2') or (Y == 'e2' and X == 'g2'): return (x != y)
    if (X == 'e2' and Y == 'h2') or (Y == 'e2' and X == 'h2'): return (x != y)
    if (X == 'e2' and Y == 'i2') or (Y == 'e2' and X == 'i2'): return (x != y)

    #e3
    if (X == 'e3' and Y == 'e4') or (Y == 'e3' and X == 'e4'): return (x != y)
    if (X == 'e3' and Y == 'e5') or (Y == 'e3' and X == 'e5'): return (x != y)
    if (X == 'e3' and Y == 'e6') or (Y == 'e3' and X == 'e6'): return (x != y)
    if (X == 'e3' and Y == 'e7') or (Y == 'e3' and X == 'e7'): return (x != y)
    if (X == 'e3' and Y == 'e8') or (Y == 'e3' and X == 'e8'): return (x != y)
    if (X == 'e3' and Y == 'e9') or (Y == 'e3' and X == 'e9'): return (x != y)

    if (X == 'e3' and Y == 'f1') or (Y == 'e3' and X == 'f1'): return (x != y)
    if (X == 'e3' and Y == 'f2') or (Y == 'e3' and X == 'f2'): return (x != y)
    if (X == 'e3' and Y == 'f3') or (Y == 'e3' and X == 'f3'): return (x != y)

    if (X == 'e3' and Y == 'g3') or (Y == 'e3' and X == 'g3'): return (x != y)
    if (X == 'e3' and Y == 'h3') or (Y == 'e3' and X == 'h3'): return (x != y)
    if (X == 'e3' and Y == 'i3') or (Y == 'e3' and X == 'i3'): return (x != y)

    #e4
    if (X == 'e4' and Y == 'e5') or (Y == 'e4' and X == 'e5'): return (x != y)
    if (X == 'e4' and Y == 'e6') or (Y == 'e4' and X == 'e6'): return (x != y)
    if (X == 'e4' and Y == 'e7') or (Y == 'e4' and X == 'e7'): return (x != y)
    if (X == 'e4' and Y == 'e8') or (Y == 'e4' and X == 'e8'): return (x != y)
    if (X == 'e4' and Y == 'e9') or (Y == 'e4' and X == 'e9'): return (x != y)

    if (X == 'e4' and Y == 'f4') or (Y == 'e4' and X == 'f4'): return (x != y)
    if (X == 'e4' and Y == 'f5') or (Y == 'e4' and X == 'f5'): return (x != y)
    if (X == 'e4' and Y == 'f6') or (Y == 'e4' and X == 'f6'): return (x != y)

    if (X == 'e4' and Y == 'g4') or (Y == 'e4' and X == 'g4'): return (x != y)
    if (X == 'e4' and Y == 'h4') or (Y == 'e4' and X == 'h4'): return (x != y)
    if (X == 'e4' and Y == 'i4') or (Y == 'e4' and X == 'i4'): return (x != y)

    #e5
    if (X == 'e5' and Y == 'e6') or (Y == 'e5' and X == 'e6'): return (x != y)
    if (X == 'e5' and Y == 'e7') or (Y == 'e5' and X == 'e7'): return (x != y)
    if (X == 'e5' and Y == 'e8') or (Y == 'e5' and X == 'e8'): return (x != y)
    if (X == 'e5' and Y == 'e9') or (Y == 'e5' and X == 'e9'): return (x != y)

    if (X == 'e5' and Y == 'f4') or (Y == 'e5' and X == 'f4'): return (x != y)
    if (X == 'e5' and Y == 'f5') or (Y == 'e5' and X == 'f5'): return (x != y)
    if (X == 'e5' and Y == 'f6') or (Y == 'e5' and X == 'f6'): return (x != y)

    if (X == 'e5' and Y == 'g5') or (Y == 'e5' and X == 'g5'): return (x != y)
    if (X == 'e5' and Y == 'h5') or (Y == 'e5' and X == 'h5'): return (x != y)
    if (X == 'e5' and Y == 'i5') or (Y == 'e5' and X == 'i5'): return (x != y)

    #e6
    if (X == 'e6' and Y == 'e7') or (Y == 'e6' and X == 'e7'): return (x != y)
    if (X == 'e6' and Y == 'e8') or (Y == 'e6' and X == 'e8'): return (x != y)
    if (X == 'e6' and Y == 'e9') or (Y == 'e6' and X == 'e9'): return (x != y)

    if (X == 'e6' and Y == 'f4') or (Y == 'e6' and X == 'f4'): return (x != y)
    if (X == 'e6' and Y == 'f5') or (Y == 'e6' and X == 'f5'): return (x != y)
    if (X == 'e6' and Y == 'f6') or (Y == 'e6' and X == 'f6'): return (x != y)

    if (X == 'e6' and Y == 'g6') or (Y == 'e6' and X == 'g6'): return (x != y)
    if (X == 'e6' and Y == 'h6') or (Y == 'e6' and X == 'h6'): return (x != y)
    if (X == 'e6' and Y == 'i6') or (Y == 'e6' and X == 'i6'): return (x != y)

    #e7
    if (X == 'e7' and Y == 'e8') or (Y == 'e7' and X == 'e8'): return (x != y)
    if (X == 'e7' and Y == 'e9') or (Y == 'e7' and X == 'e9'): return (x != y)

    if (X == 'e7' and Y == 'f7') or (Y == 'e7' and X == 'f7'): return (x != y)
    if (X == 'e7' and Y == 'f8') or (Y == 'e7' and X == 'f8'): return (x != y)
    if (X == 'e7' and Y == 'f9') or (Y == 'e7' and X == 'f9'): return (x != y)

    if (X == 'e7' and Y == 'g7') or (Y == 'e7' and X == 'g7'): return (x != y)
    if (X == 'e7' and Y == 'h7') or (Y == 'e7' and X == 'h7'): return (x != y)
    if (X == 'e7' and Y == 'i7') or (Y == 'e7' and X == 'i7'): return (x != y)

    #e8
    if (X == 'e8' and Y == 'e9') or (Y == 'e8' and X == 'e9'): return (x != y)

    if (X == 'e8' and Y == 'f7') or (Y == 'e8' and X == 'f7'): return (x != y)
    if (X == 'e8' and Y == 'f8') or (Y == 'e8' and X == 'f8'): return (x != y)
    if (X == 'e8' and Y == 'f9') or (Y == 'e8' and X == 'f9'): return (x != y)

    if (X == 'e8' and Y == 'g8') or (Y == 'e8' and X == 'g8'): return (x != y)
    if (X == 'e8' and Y == 'h8') or (Y == 'e8' and X == 'h8'): return (x != y)
    if (X == 'e8' and Y == 'i8') or (Y == 'e8' and X == 'i8'): return (x != y)

    #e9
    if (X == 'e9' and Y == 'f7') or (Y == 'e9' and X == 'f7'): return (x != y)
    if (X == 'e9' and Y == 'f8') or (Y == 'e9' and X == 'f8'): return (x != y)
    if (X == 'e9' and Y == 'f9') or (Y == 'e9' and X == 'f9'): return (x != y)

    if (X == 'e9' and Y == 'g9') or (Y == 'e9' and X == 'g9'): return (x != y)
    if (X == 'e9' and Y == 'h9') or (Y == 'e9' and X == 'h9'): return (x != y)
    if (X == 'e9' and Y == 'i9') or (Y == 'e9' and X == 'i9'): return (x != y)

    #f1
    if (X == 'f1' and Y == 'f2') or (Y == 'f1' and X == 'f2'): return (x != y)
    if (X == 'f1' and Y == 'f3') or (Y == 'f1' and X == 'f3'): return (x != y)
    if (X == 'f1' and Y == 'f4') or (Y == 'f1' and X == 'f4'): return (x != y)
    if (X == 'f1' and Y == 'f5') or (Y == 'f1' and X == 'f5'): return (x != y)
    if (X == 'f1' and Y == 'f6') or (Y == 'f1' and X == 'f6'): return (x != y)
    if (X == 'f1' and Y == 'f7') or (Y == 'f1' and X == 'f7'): return (x != y)
    if (X == 'f1' and Y == 'f8') or (Y == 'f1' and X == 'f8'): return (x != y)
    if (X == 'f1' and Y == 'f9') or (Y == 'f1' and X == 'f9'): return (x != y)

    if (X == 'f1' and Y == 'g1') or (Y == 'f1' and X == 'g1'): return (x != y)
    if (X == 'f1' and Y == 'h1') or (Y == 'f1' and X == 'h1'): return (x != y)
    if (X == 'f1' and Y == 'i1') or (Y == 'f1' and X == 'i1'): return (x != y)

    #f2
    if (X == 'f2' and Y == 'f3') or (Y == 'f2' and X == 'f3'): return (x != y)
    if (X == 'f2' and Y == 'f4') or (Y == 'f2' and X == 'f4'): return (x != y)
    if (X == 'f2' and Y == 'f5') or (Y == 'f2' and X == 'f5'): return (x != y)
    if (X == 'f2' and Y == 'f6') or (Y == 'f2' and X == 'f6'): return (x != y)
    if (X == 'f2' and Y == 'f7') or (Y == 'f2' and X == 'f7'): return (x != y)
    if (X == 'f2' and Y == 'f8') or (Y == 'f2' and X == 'f8'): return (x != y)
    if (X == 'f2' and Y == 'f9') or (Y == 'f2' and X == 'f9'): return (x != y)

    if (X == 'f2' and Y == 'g2') or (Y == 'f2' and X == 'g2'): return (x != y)
    if (X == 'f2' and Y == 'h2') or (Y == 'f2' and X == 'h2'): return (x != y)
    if (X == 'f2' and Y == 'i2') or (Y == 'f2' and X == 'i2'): return (x != y)

    #f3
    if (X == 'f3' and Y == 'f4') or (Y == 'f3' and X == 'f4'): return (x != y)
    if (X == 'f3' and Y == 'f5') or (Y == 'f3' and X == 'f5'): return (x != y)
    if (X == 'f3' and Y == 'f6') or (Y == 'f3' and X == 'f6'): return (x != y)
    if (X == 'f3' and Y == 'f7') or (Y == 'f3' and X == 'f7'): return (x != y)
    if (X == 'f3' and Y == 'f8') or (Y == 'f3' and X == 'f8'): return (x != y)
    if (X == 'f3' and Y == 'f9') or (Y == 'f3' and X == 'f9'): return (x != y)

    if (X == 'f3' and Y == 'g3') or (Y == 'f3' and X == 'g3'): return (x != y)
    if (X == 'f3' and Y == 'h3') or (Y == 'f3' and X == 'h3'): return (x != y)
    if (X == 'f3' and Y == 'i3') or (Y == 'f3' and X == 'i3'): return (x != y)

    #f4
    if (X == 'f4' and Y == 'f5') or (Y == 'f4' and X == 'f5'): return (x != y)
    if (X == 'f4' and Y == 'f6') or (Y == 'f4' and X == 'f6'): return (x != y)
    if (X == 'f4' and Y == 'f7') or (Y == 'f4' and X == 'f7'): return (x != y)
    if (X == 'f4' and Y == 'f8') or (Y == 'f4' and X == 'f8'): return (x != y)
    if (X == 'f4' and Y == 'f9') or (Y == 'f4' and X == 'f9'): return (x != y)

    if (X == 'f4' and Y == 'g4') or (Y == 'f4' and X == 'g4'): return (x != y)
    if (X == 'f4' and Y == 'h4') or (Y == 'f4' and X == 'h4'): return (x != y)
    if (X == 'f4' and Y == 'i4') or (Y == 'f4' and X == 'i4'): return (x != y)

    #f5
    if (X == 'f5' and Y == 'f6') or (Y == 'f5' and X == 'f6'): return (x != y)
    if (X == 'f5' and Y == 'f7') or (Y == 'f5' and X == 'f7'): return (x != y)
    if (X == 'f5' and Y == 'f8') or (Y == 'f5' and X == 'f8'): return (x != y)
    if (X == 'f5' and Y == 'f9') or (Y == 'f5' and X == 'f9'): return (x != y)

    if (X == 'f5' and Y == 'g5') or (Y == 'f5' and X == 'g5'): return (x != y)
    if (X == 'f5' and Y == 'h5') or (Y == 'f5' and X == 'h5'): return (x != y)
    if (X == 'f5' and Y == 'i5') or (Y == 'f5' and X == 'i5'): return (x != y)

    #f6
    if (X == 'f6' and Y == 'f7') or (Y == 'f6' and X == 'f7'): return (x != y)
    if (X == 'f6' and Y == 'f8') or (Y == 'f6' and X == 'f8'): return (x != y)
    if (X == 'f6' and Y == 'f9') or (Y == 'f6' and X == 'f9'): return (x != y)

    if (X == 'f6' and Y == 'g6') or (Y == 'f6' and X == 'g6'): return (x != y)
    if (X == 'f6' and Y == 'h6') or (Y == 'f6' and X == 'h6'): return (x != y)
    if (X == 'f6' and Y == 'i6') or (Y == 'f6' and X == 'i6'): return (x != y)

    #f7
    if (X == 'f7' and Y == 'f8') or (Y == 'f7' and X == 'f8'): return (x != y)
    if (X == 'f7' and Y == 'f9') or (Y == 'f7' and X == 'f9'): return (x != y)

    if (X == 'f7' and Y == 'g7') or (Y == 'f7' and X == 'g7'): return (x != y)
    if (X == 'f7' and Y == 'h7') or (Y == 'f7' and X == 'h7'): return (x != y)
    if (X == 'f7' and Y == 'i7') or (Y == 'f7' and X == 'i7'): return (x != y)

    #f8
    if (X == 'f8' and Y == 'f9') or (Y == 'f8' and X == 'f9'): return (x != y)

    if (X == 'f8' and Y == 'g8') or (Y == 'f8' and X == 'g8'): return (x != y)
    if (X == 'f8' and Y == 'h8') or (Y == 'f8' and X == 'h8'): return (x != y)
    if (X == 'f8' and Y == 'i8') or (Y == 'f8' and X == 'i8'): return (x != y)

    #f9
    if (X == 'f9' and Y == 'g9') or (Y == 'f9' and X == 'g9'): return (x != y)
    if (X == 'f9' and Y == 'h9') or (Y == 'f9' and X == 'h9'): return (x != y)
    if (X == 'f9' and Y == 'i9') or (Y == 'f9' and X == 'i9'): return (x != y)

    #g1
    if (X == 'g1' and Y == 'g2') or (Y == 'g1' and X == 'g2'): return (x != y)
    if (X == 'g1' and Y == 'g3') or (Y == 'g1' and X == 'g3'): return (x != y)
    if (X == 'g1' and Y == 'g4') or (Y == 'g1' and X == 'g4'): return (x != y)
    if (X == 'g1' and Y == 'g5') or (Y == 'g1' and X == 'g5'): return (x != y)
    if (X == 'g1' and Y == 'g6') or (Y == 'g1' and X == 'g6'): return (x != y)
    if (X == 'g1' and Y == 'g7') or (Y == 'g1' and X == 'g7'): return (x != y)
    if (X == 'g1' and Y == 'g8') or (Y == 'g1' and X == 'g8'): return (x != y)
    if (X == 'g1' and Y == 'g9') or (Y == 'g1' and X == 'g9'): return (x != y)

    if (X == 'g1' and Y == 'h1') or (Y == 'g1' and X == 'h1'): return (x != y)
    if (X == 'g1' and Y == 'h2') or (Y == 'g1' and X == 'h2'): return (x != y)
    if (X == 'g1' and Y == 'h3') or (Y == 'g1' and X == 'h3'): return (x != y)
    if (X == 'g1' and Y == 'i1') or (Y == 'g1' and X == 'i1'): return (x != y)
    if (X == 'g1' and Y == 'i2') or (Y == 'g1' and X == 'i2'): return (x != y)
    if (X == 'g1' and Y == 'i3') or (Y == 'g1' and X == 'i3'): return (x != y)

    #g2
    if (X == 'g2' and Y == 'g3') or (Y == 'g2' and X == 'g3'): return (x != y)
    if (X == 'g2' and Y == 'g4') or (Y == 'g2' and X == 'g4'): return (x != y)
    if (X == 'g2' and Y == 'g5') or (Y == 'g2' and X == 'g5'): return (x != y)
    if (X == 'g2' and Y == 'g6') or (Y == 'g2' and X == 'g6'): return (x != y)
    if (X == 'g2' and Y == 'g7') or (Y == 'g2' and X == 'g7'): return (x != y)
    if (X == 'g2' and Y == 'g8') or (Y == 'g2' and X == 'g8'): return (x != y)
    if (X == 'g2' and Y == 'g9') or (Y == 'g2' and X == 'g9'): return (x != y)

    if (X == 'g2' and Y == 'h1') or (Y == 'g2' and X == 'h1'): return (x != y)
    if (X == 'g2' and Y == 'h2') or (Y == 'g2' and X == 'h2'): return (x != y)
    if (X == 'g2' and Y == 'h3') or (Y == 'g2' and X == 'h3'): return (x != y)
    if (X == 'g2' and Y == 'i1') or (Y == 'g2' and X == 'i1'): return (x != y)
    if (X == 'g2' and Y == 'i2') or (Y == 'g2' and X == 'i2'): return (x != y)
    if (X == 'g2' and Y == 'i3') or (Y == 'g2' and X == 'i3'): return (x != y)

    #g3
    if (X == 'g3' and Y == 'g4') or (Y == 'g3' and X == 'g4'): return (x != y)
    if (X == 'g3' and Y == 'g5') or (Y == 'g3' and X == 'g5'): return (x != y)
    if (X == 'g3' and Y == 'g6') or (Y == 'g3' and X == 'g6'): return (x != y)
    if (X == 'g3' and Y == 'g7') or (Y == 'g3' and X == 'g7'): return (x != y)
    if (X == 'g3' and Y == 'g8') or (Y == 'g3' and X == 'g8'): return (x != y)
    if (X == 'g3' and Y == 'g9') or (Y == 'g3' and X == 'g9'): return (x != y)

    if (X == 'g3' and Y == 'h1') or (Y == 'g3' and X == 'h1'): return (x != y)
    if (X == 'g3' and Y == 'h2') or (Y == 'g3' and X == 'h2'): return (x != y)
    if (X == 'g3' and Y == 'h3') or (Y == 'g3' and X == 'h3'): return (x != y)
    if (X == 'g3' and Y == 'i1') or (Y == 'g3' and X == 'i1'): return (x != y)
    if (X == 'g3' and Y == 'i2') or (Y == 'g3' and X == 'i2'): return (x != y)
    if (X == 'g3' and Y == 'i3') or (Y == 'g3' and X == 'i3'): return (x != y)

    #g4
    if (X == 'g4' and Y == 'g5') or (Y == 'g4' and X == 'g5'): return (x != y)
    if (X == 'g4' and Y == 'g6') or (Y == 'g4' and X == 'g6'): return (x != y)
    if (X == 'g4' and Y == 'g7') or (Y == 'g4' and X == 'g7'): return (x != y)
    if (X == 'g4' and Y == 'g8') or (Y == 'g4' and X == 'g8'): return (x != y)
    if (X == 'g4' and Y == 'g9') or (Y == 'g4' and X == 'g9'): return (x != y)

    if (X == 'g4' and Y == 'h4') or (Y == 'g4' and X == 'h4'): return (x != y)
    if (X == 'g4' and Y == 'h5') or (Y == 'g4' and X == 'h5'): return (x != y)
    if (X == 'g4' and Y == 'h6') or (Y == 'g4' and X == 'h6'): return (x != y)
    if (X == 'g4' and Y == 'i4') or (Y == 'g4' and X == 'i4'): return (x != y)
    if (X == 'g4' and Y == 'i5') or (Y == 'g4' and X == 'i5'): return (x != y)
    if (X == 'g4' and Y == 'i6') or (Y == 'g4' and X == 'i6'): return (x != y)

    #g5
    if (X == 'g5' and Y == 'g6') or (Y == 'g5' and X == 'g6'): return (x != y)
    if (X == 'g5' and Y == 'g7') or (Y == 'g5' and X == 'g7'): return (x != y)
    if (X == 'g5' and Y == 'g8') or (Y == 'g5' and X == 'g8'): return (x != y)
    if (X == 'g5' and Y == 'g9') or (Y == 'g5' and X == 'g9'): return (x != y)

    if (X == 'g5' and Y == 'h4') or (Y == 'g5' and X == 'h4'): return (x != y)
    if (X == 'g5' and Y == 'h5') or (Y == 'g5' and X == 'h5'): return (x != y)
    if (X == 'g5' and Y == 'h6') or (Y == 'g5' and X == 'h6'): return (x != y)
    if (X == 'g5' and Y == 'i4') or (Y == 'g5' and X == 'i4'): return (x != y)
    if (X == 'g5' and Y == 'i5') or (Y == 'g5' and X == 'i5'): return (x != y)
    if (X == 'g5' and Y == 'i6') or (Y == 'g5' and X == 'i6'): return (x != y)

    #g6
    if (X == 'g6' and Y == 'g7') or (Y == 'g6' and X == 'g7'): return (x != y)
    if (X == 'g6' and Y == 'g8') or (Y == 'g6' and X == 'g8'): return (x != y)
    if (X == 'g6' and Y == 'g9') or (Y == 'g6' and X == 'g9'): return (x != y)

    if (X == 'g6' and Y == 'h4') or (Y == 'g6' and X == 'h4'): return (x != y)
    if (X == 'g6' and Y == 'h5') or (Y == 'g6' and X == 'h5'): return (x != y)
    if (X == 'g6' and Y == 'h6') or (Y == 'g6' and X == 'h6'): return (x != y)
    if (X == 'g6' and Y == 'i4') or (Y == 'g6' and X == 'i4'): return (x != y)
    if (X == 'g6' and Y == 'i5') or (Y == 'g6' and X == 'i5'): return (x != y)
    if (X == 'g6' and Y == 'i6') or (Y == 'g6' and X == 'i6'): return (x != y)

    #g7
    if (X == 'g7' and Y == 'g8') or (Y == 'g7' and X == 'g8'): return (x != y)
    if (X == 'g7' and Y == 'g9') or (Y == 'g7' and X == 'g9'): return (x != y)

    if (X == 'g7' and Y == 'h7') or (Y == 'g7' and X == 'h7'): return (x != y)
    if (X == 'g7' and Y == 'h8') or (Y == 'g7' and X == 'h8'): return (x != y)
    if (X == 'g7' and Y == 'h9') or (Y == 'g7' and X == 'h9'): return (x != y)
    if (X == 'g7' and Y == 'i7') or (Y == 'g7' and X == 'i7'): return (x != y)
    if (X == 'g7' and Y == 'i8') or (Y == 'g7' and X == 'i8'): return (x != y)
    if (X == 'g7' and Y == 'i9') or (Y == 'g7' and X == 'i9'): return (x != y)

    #g8
    if (X == 'g8' and Y == 'g9') or (Y == 'g8' and X == 'g9'): return (x != y)

    if (X == 'g8' and Y == 'h7') or (Y == 'g8' and X == 'h7'): return (x != y)
    if (X == 'g8' and Y == 'h8') or (Y == 'g8' and X == 'h8'): return (x != y)
    if (X == 'g8' and Y == 'h9') or (Y == 'g8' and X == 'h9'): return (x != y)
    if (X == 'g8' and Y == 'i7') or (Y == 'g8' and X == 'i7'): return (x != y)
    if (X == 'g8' and Y == 'i8') or (Y == 'g8' and X == 'i8'): return (x != y)
    if (X == 'g8' and Y == 'i9') or (Y == 'g8' and X == 'i9'): return (x != y)

    #g9
    if (X == 'g9' and Y == 'h7') or (Y == 'g9' and X == 'h7'): return (x != y)
    if (X == 'g9' and Y == 'h8') or (Y == 'g9' and X == 'h8'): return (x != y)
    if (X == 'g9' and Y == 'h9') or (Y == 'g9' and X == 'h9'): return (x != y)
    if (X == 'g9' and Y == 'i7') or (Y == 'g9' and X == 'i7'): return (x != y)
    if (X == 'g9' and Y == 'i8') or (Y == 'g9' and X == 'i8'): return (x != y)
    if (X == 'g9' and Y == 'i9') or (Y == 'g9' and X == 'i9'): return (x != y)

    #h1
    if (X == 'h1' and Y == 'h2') or (Y == 'h1' and X == 'h2'): return (x != y)
    if (X == 'h1' and Y == 'h3') or (Y == 'h1' and X == 'h3'): return (x != y)
    if (X == 'h1' and Y == 'h4') or (Y == 'h1' and X == 'h4'): return (x != y)
    if (X == 'h1' and Y == 'h5') or (Y == 'h1' and X == 'h5'): return (x != y)
    if (X == 'h1' and Y == 'h6') or (Y == 'h1' and X == 'h6'): return (x != y)
    if (X == 'h1' and Y == 'h7') or (Y == 'h1' and X == 'h7'): return (x != y)
    if (X == 'h1' and Y == 'h8') or (Y == 'h1' and X == 'h8'): return (x != y)
    if (X == 'h1' and Y == 'h9') or (Y == 'h1' and X == 'h9'): return (x != y)

    if (X == 'h1' and Y == 'i1') or (Y == 'h1' and X == 'i1'): return (x != y)
    if (X == 'h1' and Y == 'i2') or (Y == 'h1' and X == 'i2'): return (x != y)
    if (X == 'h1' and Y == 'i3') or (Y == 'h1' and X == 'i3'): return (x != y)

    #h2
    if (X == 'h2' and Y == 'h3') or (Y == 'h2' and X == 'h3'): return (x != y)
    if (X == 'h2' and Y == 'h4') or (Y == 'h2' and X == 'h4'): return (x != y)
    if (X == 'h2' and Y == 'h5') or (Y == 'h2' and X == 'h5'): return (x != y)
    if (X == 'h2' and Y == 'h6') or (Y == 'h2' and X == 'h6'): return (x != y)
    if (X == 'h2' and Y == 'h7') or (Y == 'h2' and X == 'h7'): return (x != y)
    if (X == 'h2' and Y == 'h8') or (Y == 'h2' and X == 'h8'): return (x != y)
    if (X == 'h2' and Y == 'h9') or (Y == 'h2' and X == 'h9'): return (x != y)

    if (X == 'h2' and Y == 'i1') or (Y == 'h2' and X == 'i1'): return (x != y)
    if (X == 'h2' and Y == 'i2') or (Y == 'h2' and X == 'i2'): return (x != y)
    if (X == 'h2' and Y == 'i3') or (Y == 'h2' and X == 'i3'): return (x != y)

    #h3
    if (X == 'h3' and Y == 'h4') or (Y == 'h3' and X == 'h4'): return (x != y)
    if (X == 'h3' and Y == 'h5') or (Y == 'h3' and X == 'h5'): return (x != y)
    if (X == 'h3' and Y == 'h6') or (Y == 'h3' and X == 'h6'): return (x != y)
    if (X == 'h3' and Y == 'h7') or (Y == 'h3' and X == 'h7'): return (x != y)
    if (X == 'h3' and Y == 'h8') or (Y == 'h3' and X == 'h8'): return (x != y)
    if (X == 'h3' and Y == 'h9') or (Y == 'h3' and X == 'h9'): return (x != y)

    if (X == 'h3' and Y == 'i1') or (Y == 'h3' and X == 'i1'): return (x != y)
    if (X == 'h3' and Y == 'i2') or (Y == 'h3' and X == 'i2'): return (x != y)
    if (X == 'h3' and Y == 'i3') or (Y == 'h3' and X == 'i3'): return (x != y)

    #h4
    if (X == 'h4' and Y == 'h5') or (Y == 'h4' and X == 'h5'): return (x != y)
    if (X == 'h4' and Y == 'h6') or (Y == 'h4' and X == 'h6'): return (x != y)
    if (X == 'h4' and Y == 'h7') or (Y == 'h4' and X == 'h7'): return (x != y)
    if (X == 'h4' and Y == 'h8') or (Y == 'h4' and X == 'h8'): return (x != y)
    if (X == 'h4' and Y == 'h9') or (Y == 'h4' and X == 'h9'): return (x != y)

    if (X == 'h4' and Y == 'i4') or (Y == 'h4' and X == 'i4'): return (x != y)
    if (X == 'h4' and Y == 'i5') or (Y == 'h4' and X == 'i5'): return (x != y)
    if (X == 'h4' and Y == 'i6') or (Y == 'h4' and X == 'i6'): return (x != y)

    #h5
    if (X == 'h5' and Y == 'h6') or (Y == 'h5' and X == 'h6'): return (x != y)
    if (X == 'h5' and Y == 'h7') or (Y == 'h5' and X == 'h7'): return (x != y)
    if (X == 'h5' and Y == 'h8') or (Y == 'h5' and X == 'h8'): return (x != y)
    if (X == 'h5' and Y == 'h9') or (Y == 'h5' and X == 'h9'): return (x != y)

    if (X == 'h5' and Y == 'i4') or (Y == 'h5' and X == 'i4'): return (x != y)
    if (X == 'h5' and Y == 'i5') or (Y == 'h5' and X == 'i5'): return (x != y)
    if (X == 'h5' and Y == 'i6') or (Y == 'h5' and X == 'i6'): return (x != y)

    #h6
    if (X == 'h6' and Y == 'h7') or (Y == 'h6' and X == 'h7'): return (x != y)
    if (X == 'h6' and Y == 'h8') or (Y == 'h6' and X == 'h8'): return (x != y)
    if (X == 'h6' and Y == 'h9') or (Y == 'h6' and X == 'h9'): return (x != y)

    if (X == 'h6' and Y == 'i4') or (Y == 'h6' and X == 'i4'): return (x != y)
    if (X == 'h6' and Y == 'i5') or (Y == 'h6' and X == 'i5'): return (x != y)
    if (X == 'h6' and Y == 'i6') or (Y == 'h6' and X == 'i6'): return (x != y)

    #h7
    if (X == 'h7' and Y == 'h8') or (Y == 'h7' and X == 'h8'): return (x != y)
    if (X == 'h7' and Y == 'h9') or (Y == 'h7' and X == 'h9'): return (x != y)

    if (X == 'h7' and Y == 'i7') or (Y == 'h7' and X == 'i7'): return (x != y)
    if (X == 'h7' and Y == 'i8') or (Y == 'h7' and X == 'i8'): return (x != y)
    if (X == 'h7' and Y == 'i9') or (Y == 'h7' and X == 'i9'): return (x != y)

    #h8
    if (X == 'h8' and Y == 'h9') or (Y == 'h8' and X == 'h9'): return (x != y)

    if (X == 'h8' and Y == 'i7') or (Y == 'h8' and X == 'i7'): return (x != y)
    if (X == 'h8' and Y == 'i8') or (Y == 'h8' and X == 'i8'): return (x != y)
    if (X == 'h8' and Y == 'i9') or (Y == 'h8' and X == 'i9'): return (x != y)

    #h9
    if (X == 'h9' and Y == 'i7') or (Y == 'h9' and X == 'i7'): return (x != y)
    if (X == 'h9' and Y == 'i8') or (Y == 'h9' and X == 'i8'): return (x != y)
    if (X == 'h9' and Y == 'i9') or (Y == 'h9' and X == 'i9'): return (x != y)

    #i1
    if (X == 'i1' and Y == 'i2') or (Y == 'i1' and X == 'i2'): return (x != y)
    if (X == 'i1' and Y == 'i3') or (Y == 'i1' and X == 'i3'): return (x != y)
    if (X == 'i1' and Y == 'i4') or (Y == 'i1' and X == 'i4'): return (x != y)
    if (X == 'i1' and Y == 'i5') or (Y == 'i1' and X == 'i5'): return (x != y)
    if (X == 'i1' and Y == 'i6') or (Y == 'i1' and X == 'i6'): return (x != y)
    if (X == 'i1' and Y == 'i7') or (Y == 'i1' and X == 'i7'): return (x != y)
    if (X == 'i1' and Y == 'i8') or (Y == 'i1' and X == 'i8'): return (x != y)
    if (X == 'i1' and Y == 'i9') or (Y == 'i1' and X == 'i9'): return (x != y)

    #i2
    if (X == 'i2' and Y == 'i3') or (Y == 'i2' and X == 'i3'): return (x != y)
    if (X == 'i2' and Y == 'i4') or (Y == 'i2' and X == 'i4'): return (x != y)
    if (X == 'i2' and Y == 'i5') or (Y == 'i2' and X == 'i5'): return (x != y)
    if (X == 'i2' and Y == 'i6') or (Y == 'i2' and X == 'i6'): return (x != y)
    if (X == 'i2' and Y == 'i7') or (Y == 'i2' and X == 'i7'): return (x != y)
    if (X == 'i2' and Y == 'i8') or (Y == 'i2' and X == 'i8'): return (x != y)
    if (X == 'i2' and Y == 'i9') or (Y == 'i2' and X == 'i9'): return (x != y)

    #i3
    if (X == 'i3' and Y == 'i4') or (Y == 'i3' and X == 'i4'): return (x != y)
    if (X == 'i3' and Y == 'i5') or (Y == 'i3' and X == 'i5'): return (x != y)
    if (X == 'i3' and Y == 'i6') or (Y == 'i3' and X == 'i6'): return (x != y)
    if (X == 'i3' and Y == 'i7') or (Y == 'i3' and X == 'i7'): return (x != y)
    if (X == 'i3' and Y == 'i8') or (Y == 'i3' and X == 'i8'): return (x != y)
    if (X == 'i3' and Y == 'i9') or (Y == 'i3' and X == 'i9'): return (x != y)

    #i4
    if (X == 'i4' and Y == 'i5') or (Y == 'i4' and X == 'i5'): return (x != y)
    if (X == 'i4' and Y == 'i6') or (Y == 'i4' and X == 'i6'): return (x != y)
    if (X == 'i4' and Y == 'i7') or (Y == 'i4' and X == 'i7'): return (x != y)
    if (X == 'i4' and Y == 'i8') or (Y == 'i4' and X == 'i8'): return (x != y)
    if (X == 'i4' and Y == 'i9') or (Y == 'i4' and X == 'i9'): return (x != y)

    #i5
    if (X == 'i5' and Y == 'i6') or (Y == 'i5' and X == 'i6'): return (x != y)
    if (X == 'i5' and Y == 'i7') or (Y == 'i5' and X == 'i7'): return (x != y)
    if (X == 'i5' and Y == 'i8') or (Y == 'i5' and X == 'i8'): return (x != y)
    if (X == 'i5' and Y == 'i9') or (Y == 'i5' and X == 'i9'): return (x != y)

    #i6
    if (X == 'i6' and Y == 'i7') or (Y == 'i6' and X == 'i7'): return (x != y)
    if (X == 'i6' and Y == 'i8') or (Y == 'i6' and X == 'i8'): return (x != y)
    if (X == 'i6' and Y == 'i9') or (Y == 'i6' and X == 'i9'): return (x != y)

    #i7
    if (X == 'i7' and Y == 'i8') or (Y == 'i7' and X == 'i8'): return (x != y)
    if (X == 'i7' and Y == 'i9') or (Y == 'i7' and X == 'i9'): return (x != y)

    #i8
    if (X == 'i8' and Y == 'i9') or (Y == 'i8' and X == 'i9'): return (x != y)


# neighbors of all variables
neighbors = 'a1: a2 a3 a4 a5 a6 a7 a8 a9 b1 b2 b3 c1 c2 c3 d1 e1 f1 g1 h1 i1;' \
            'a2: a1 a3 a4 a5 a6 a7 a8 a9 b1 b2 b3 c1 c2 c3 d2 e2 f2 g2 h2 i2;' \
            'a3: a1 a2 a4 a5 a6 a7 a8 a9 b1 b2 b3 c1 c2 c3 d3 e3 f3 g3 h3 i3;' \
            'a4: a1 a2 a3 a5 a6 a7 a8 a9 b4 b5 b6 c4 c5 c6 d4 e4 f4 g4 h4 i4;' \
            'a5: a1 a2 a3 a4 a6 a7 a8 a9 b4 b5 b6 c4 c5 c6 d5 e5 f5 g5 h5 i5;' \
            'a6: a1 a2 a3 a4 a5 a7 a8 a9 b4 b5 b6 c4 c5 c6 d6 e6 f6 g6 h6 i6;' \
            'a7: a1 a2 a3 a4 a5 a6 a8 a9 b7 b8 b9 c7 c8 c9 d7 e7 f7 g7 h7 i7;' \
            'a8: a1 a2 a3 a4 a5 a6 a7 a9 b7 b8 b9 c7 c8 c9 d8 e8 f8 g8 h8 i8;' \
            'a9: a1 a2 a3 a4 a5 a6 a7 a8 b7 b8 b9 c7 c8 c9 d9 e9 f9 g9 h9 i9;' \
            'b1: b2 b3 b4 b5 b6 b7 b8 b9 a1 a2 a3 c1 c2 c3 d1 e1 f1 g1 h1 i1;' \
            'b2: b1 b3 b4 b5 b6 b7 b8 b9 a1 a2 a3 c1 c2 c3 d2 e2 f2 g2 h2 i2;' \
            'b3: b1 b2 b4 b5 b6 b7 b8 b9 a1 a2 a3 c1 c2 c3 d3 e3 f3 g3 h3 i3;' \
            'b4: b1 b2 b3 b5 b6 b7 b8 b9 a4 a5 a6 c4 c5 c6 d4 e4 f4 g4 h4 i4;' \
            'b5: b1 b2 b3 b4 b6 b7 b8 b9 a4 a5 a6 c4 c5 c6 d5 e5 f5 g5 h5 i5;' \
            'b6: b1 b2 b3 b4 b5 b7 b8 b9 a4 a5 a6 c4 c5 c6 d6 e6 f6 g6 h6 i6;' \
            'b7: b1 b2 b3 b4 b5 b6 b8 b9 a7 a8 a9 c7 c8 c9 d7 e7 f7 g7 h7 i7;' \
            'b8: b1 b2 b3 b4 b5 b6 b7 b9 a7 a8 a9 c7 c8 c9 d8 e8 f8 g8 h8 i8;' \
            'b9: b1 b2 b3 b4 b5 b6 b7 b8 a7 a8 a9 c7 c8 c9 d9 e9 f9 g9 h9 i9;' \
            'c1: c2 c3 c4 c5 c6 c7 c8 c9 a1 a2 a3 b1 b2 b3 d1 e1 f1 g1 h1 i1;' \
            'c2: c1 c3 c4 c5 c6 c7 c8 c9 a1 a2 a3 b1 b2 b3 d2 e2 f2 g2 h2 i2;' \
            'c3: c1 c2 c4 c5 c6 c7 c8 c9 a1 a2 a3 b1 b2 b3 d3 e3 f3 g3 h3 i3;' \
            'c4: c1 c2 c3 c5 c6 c7 c8 c9 a4 a5 a6 b4 b5 b6 d4 e4 f4 g4 h4 i4;' \
            'c5: c1 c2 c3 c4 c6 c7 c8 c9 a4 a5 a6 b4 b5 b6 d5 e5 f5 g5 h5 i5;' \
            'c6: c1 c2 c3 c4 c5 c7 c8 c9 a4 a5 a6 b4 b5 b6 d6 e6 f6 g6 h6 i6;' \
            'c7: c1 c2 c3 c4 c5 c6 c8 c9 a7 a8 a9 b7 b8 b9 d7 e7 f7 g7 h7 i7;' \
            'c8: c1 c2 c3 c4 c5 c6 c7 c9 a7 a8 a9 b7 b8 b9 d8 e8 f8 g8 h8 i8;' \
            'c9: c1 c2 c3 c4 c5 c6 c7 c8 a7 a8 a9 b7 b8 b9 d9 e9 f9 g9 h9 i9;' \
            'd1: d2 d3 d4 d5 d6 d7 d8 d9 e1 e2 e3 f1 f2 f3 a1 b1 c1 g1 h1 i1;' \
            'd2: d1 d3 d4 d5 d6 d7 d8 d9 e1 e2 e3 f1 f2 f3 a2 b2 c2 g2 h2 i2;' \
            'd3: d1 d2 d4 d5 d6 d7 d8 d9 e1 e2 e3 f1 f2 f3 a3 b3 c3 g3 h3 i3;' \
            'd4: d1 d2 d3 d5 d6 d7 d8 d9 e4 e5 e6 f4 f5 f6 a4 b4 c4 g4 h4 i4;' \
            'd5: d1 d2 d3 d4 d6 d7 d8 d9 e4 e5 e6 f4 f5 f6 a5 b5 c5 g5 h5 i5;' \
            'd6: d1 d2 d3 d4 d5 d7 d8 d9 e4 e5 e6 f4 f5 f6 a6 b6 c6 g6 h6 i6;' \
            'd7: d1 d2 d3 d4 d5 d6 d8 d9 e7 e8 e9 f7 f8 f9 a7 b7 c7 g7 h7 i7;' \
            'd8: d1 d2 d3 d4 d5 d6 d7 d9 e7 e8 e9 f7 f8 f9 a8 b8 c8 g8 h8 i8;' \
            'd9: d1 d2 d3 d4 d5 d6 d7 d8 e7 e8 e9 f7 f8 f9 a9 b9 c9 g9 h9 i9;' \
            'e1: e2 e3 e4 e5 e6 e7 e8 e9 d1 d2 d3 f1 f2 f3 a1 b1 c1 g1 h1 i1;' \
            'e2: e1 e3 e4 e5 e6 e7 e8 e9 d1 d2 d3 f1 f2 f3 a2 b2 c2 g2 h2 i2;' \
            'e3: e1 e2 e4 e5 e6 e7 e8 e9 d1 d2 d3 f1 f2 f3 a3 b3 c3 g3 h3 i3;' \
            'e4: e1 e2 e3 e5 e6 e7 e8 e9 d4 d5 d6 f4 f5 f6 a4 b4 c4 g4 h4 i4;' \
            'e5: e1 e2 e3 e4 e6 e7 e8 e9 d4 d5 d6 f4 f5 f6 a5 b5 c5 g5 h5 i5;' \
            'e6: e1 e2 e3 e4 e5 e7 e8 e9 d4 d5 d6 f4 f5 f6 a6 b6 c6 g6 h6 i6;' \
            'e7: e1 e2 e3 e4 e5 e6 e8 e9 d7 d8 d9 f7 f8 f9 a7 b7 c7 g7 h7 i7;' \
            'e8: e1 e2 e3 e4 e5 e6 e7 e9 d7 d8 d9 f7 f8 f9 a8 b8 c8 g8 h8 i8;' \
            'e9: e1 e2 e3 e4 e5 e6 e7 e8 d7 d8 d9 f7 f8 f9 a9 b9 c9 g9 h9 i9;' \
            'f1: f2 f3 f4 f5 f6 f7 f8 f9 d1 d2 d3 e1 e2 e3 a1 b1 c1 g1 h1 i1;' \
            'f2: f1 f3 f4 f5 f6 f7 f8 f9 d1 d2 d3 e1 e2 e3 a2 b2 c2 g2 h2 i2;' \
            'f3: f1 f2 f4 f5 f6 f7 f8 f9 d1 d2 d3 e1 e2 e3 a3 b3 c3 g3 h3 i3;' \
            'f4: f1 f2 f3 f5 f6 f7 f8 f9 d4 d5 d6 e4 e5 e6 a4 b4 c4 g4 h4 i4;' \
            'f5: f1 f2 f3 f4 f6 f7 f8 f9 d4 d5 d6 e4 e5 e6 a5 b5 c5 g5 h5 i5;' \
            'f6: f1 f2 f3 f4 f5 f7 f8 f9 d4 d5 d6 e4 e5 e6 a6 b6 c6 g6 h6 i6;' \
            'f7: f1 f2 f3 f4 f5 f6 f8 f9 d7 d8 d9 e7 e8 e9 a7 b7 c7 g7 h7 i7;' \
            'f8: f1 f2 f3 f4 f5 f6 f7 f9 d7 d8 d9 e7 e8 e9 a8 b8 c8 g8 h8 i8;' \
            'f9: f1 f2 f3 f4 f5 f6 f7 f8 d7 d8 d9 e7 e8 e9 a9 b9 c9 g9 h9 i9;' \
            'g1: g2 g3 g4 g5 g6 g7 g8 g9 h1 h2 h3 i1 i2 i3 a1 b1 c1 d1 e1 f1;' \
            'g2: g1 g3 g4 g5 g6 g7 g8 g9 h1 h2 h3 i1 i2 i3 a2 b2 c2 d2 e2 f2;' \
            'g3: g1 g2 g4 g5 g6 g7 g8 g9 h1 h2 h3 i1 i2 i3 a3 b3 c3 d3 e3 f3;' \
            'g4: g1 g2 g3 g5 g6 g7 g8 g9 h4 h5 h6 i4 i5 i6 a4 b4 c4 d4 e4 f4;' \
            'g5: g1 g2 g3 g4 g6 g7 g8 g9 h4 h5 h6 i4 i5 i6 a5 b5 c5 d5 e5 f5;' \
            'g6: g1 g2 g3 g4 g5 g7 g8 g9 h4 h5 h6 i4 i5 i6 a6 b6 c6 d6 e6 f6;' \
            'g7: g1 g2 g3 g4 g5 g6 g8 g9 h7 h8 h9 i7 i8 i9 a7 b7 c7 d7 e7 f7;' \
            'g8: g1 g2 g3 g4 g5 g6 g7 g9 h7 h8 h9 i7 i8 i9 a8 b8 c8 d8 e8 f8;' \
            'g9: g1 g2 g3 g4 g5 g6 g7 g8 h7 h8 h9 i7 i8 i9 a9 b9 c9 d9 e9 f9;' \
            'h1: h2 h3 h4 h5 h6 h7 h8 h9 g1 g2 g3 i1 i2 i3 a1 b1 c1 d1 e1 f1;' \
            'h2: h1 h3 h4 h5 h6 h7 h8 h9 g1 g2 g3 i1 i2 i3 a2 b2 c2 d2 e2 f2;' \
            'h3: h1 h2 h4 h5 h6 h7 h8 h9 g1 g2 g3 i1 i2 i3 a3 b3 c3 d3 e3 f3;' \
            'h4: h1 h2 h3 h5 h6 h7 h8 h9 g4 g5 g6 i4 i5 i6 a4 b4 c4 d4 e4 f4;' \
            'h5: h1 h2 h3 h4 h6 h7 h8 h9 g4 g5 g6 i4 i5 i6 a5 b5 c5 d5 e5 f5;' \
            'h6: h1 h2 h3 h4 h5 h7 h8 h9 g4 g5 g6 i4 i5 i6 a6 b6 c6 d6 e6 f6;' \
            'h7: h1 h2 h3 h4 h5 h6 h8 h9 g7 g8 g9 i7 i8 i9 a7 b7 c7 d7 e7 f7;' \
            'h8: h1 h2 h3 h4 h5 h6 h7 h9 g7 g8 g9 i7 i8 i9 a8 b8 c8 d8 e8 f8;' \
            'h9: h1 h2 h3 h4 h5 h6 h7 h8 g7 g8 g9 i7 i8 i9 a9 b9 c9 d9 e9 f9;' \
            'i1: i2 i3 i4 i5 i6 i7 i8 i9 g1 g2 g3 h1 h2 h3 a1 b1 c1 d1 e1 f1;' \
            'i2: i1 i3 i4 i5 i6 i7 i8 i9 g1 g2 g3 h1 h2 h3 a2 b2 c2 d2 e2 f2;' \
            'i3: i1 i2 i4 i5 i6 i7 i8 i9 g1 g2 g3 h1 h2 h3 a3 b3 c3 d3 e3 f3;' \
            'i4: i1 i2 i3 i5 i6 i7 i8 i9 g4 g5 g6 h4 h5 h6 a4 b4 c4 d4 e4 f4;' \
            'i5: i1 i2 i3 i4 i6 i7 i8 i9 g4 g5 g6 h4 h5 h6 a5 b5 c5 d5 e5 f5;' \
            'i6: i1 i2 i3 i4 i5 i7 i8 i9 g4 g5 g6 h4 h5 h6 a6 b6 c6 d6 e6 f6;' \
            'i7: i1 i2 i3 i4 i5 i6 i8 i9 g7 g8 g9 h7 h8 h9 a7 b7 c7 d7 e7 f7;' \
            'i8: i1 i2 i3 i4 i5 i6 i7 i9 g7 g8 g9 h7 h8 h9 a8 b8 c8 d8 e8 f8;' \
            'i9: i1 i2 i3 i4 i5 i6 i7 i8 g7 g8 g9 h7 h8 h9 a9 b9 c9 d9 e9 f9'

D = {var: [] for var in vars}
all_neighbor = [spec.split(':') for spec in neighbors.split(';')]
for (var, var_neighbors) in all_neighbor:
    var = var.strip();
    D[var] = var_neighbors.split()

# formulate sudoku as CSP problem
Sudoku = CSP(vars, domains, D, constraints)


# to determine whether AC3 can solve the sudoku
def solved(AC3, csp):
    inf = AC3(csp)
    for k, val in (csp.new_domains).items():
        if len(val) > 1:
            inf = False
            break
    return inf


# writing output into a file and also determining whether sudoku can be solved by AC3 algorithm alone or not
file1 = open('output.txt', 'w')
if solved(AC3, Sudoku):
    result_ac3 = ''
    for k, v in (Sudoku.new_domains).items():
        result_ac3 = result_ac3 + str(v[0])
    file1.write(result_ac3 + ' ' + 'AC3')
else:
    result_bts = ''
    assignment = backtracking_search(Sudoku)
    for k, v in assignment.items():
        result_bts = result_bts + str(v[0])
    file1.write(result_bts + ' ' + 'BTS')

file1.close()