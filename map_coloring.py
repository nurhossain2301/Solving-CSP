class CSP:
    def __init__(self, vars, domains, neighbors, constraints):
        "Construct a CSP problem. If vars is empty, it becomes domains.keys()."
        self.vars = vars
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.new_domains = {}


vars = 'WA NT Q NSW  V SA T'.split()
domains = {}
for var in vars:
    domains[var] = [1, 2, 3]


def constraints(X, x, Y, y):
    return x !=y


neighbors = 'SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: '

Dict = {var: [] for var in vars}
specs = [spec.split(':') for spec in neighbors.split(';')]
for (A, Aneighbors) in specs:
    A = A.strip();
    for B in Aneighbors.split():
        Dict[A].append(B)
        Dict[B].append(A)

australia = CSP(vars, domains, Dict, constraints)

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


backtracking_search(australia)
print(australia.new_domains)