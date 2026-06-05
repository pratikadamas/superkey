def parse_fd(fd_input):
    fds = []
    for fd in fd_input.split(','):
        left, right = fd.split('->')
        fds.append((set(left.strip()), set(right.strip())))
    return fds

def closure(attributes, fds):
    closure_set = set(attributes)

    while True:
        updated = False
        for left, right in fds:
            if left.issubset(closure_set) and not right.issubset(closure_set):
                closure_set |= right
                updated = True
        if not updated:
            break

    return closure_set

from itertools import combinations

def get_superkeys(attributes, fds):
    all_attrs = set(attributes)
    superkeys = []

    for i in range(1, len(attributes) + 1):
        for subset in combinations(attributes, i):
            subset_set = set(subset)
            if closure(subset_set, fds) == all_attrs:
                superkeys.append(subset_set)

    return superkeys

def get_candidate_keys(superkeys):
    candidate_keys = []

    for key in superkeys:
        is_minimal = True
        for other in superkeys:
            if other < key:  # proper subset
                is_minimal = False
                break
        if is_minimal:
            candidate_keys.append(key)

    return candidate_keys