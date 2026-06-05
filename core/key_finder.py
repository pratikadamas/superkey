"""
Candidate-key / super-key finder logic.
All functions below are the ORIGINAL algorithm — moved here for modularity.
"""

import re
from itertools import combinations


def _split_attr_token(token: str, all_single_letters: bool) -> set[str]:
    """
    If all known attributes are single letters, break 'BC' into {'B','C'}.
    Otherwise keep token as a whole attribute name.
    """
    if all_single_letters and len(token) > 1:
        return set(token.upper())       # each character is an attribute
    return {token.upper()}


def parse_attributes(attr_str: str) -> list[str]:
    """Extract unique attributes from a comma/space separated string."""
    raw = re.findall(r'\w+', attr_str)
    return sorted({a.upper() for a in raw})


def parse_fds(fd_str: str, user_attrs: list[str]) -> list[tuple[set[str], set[str]]]:
    """
    Convert a string like "A->BC, D->A" or "A → B,C → D" into a list of
    (lhs_set, rhs_set). Normalises Unicode arrows to '->'.
    """
    # 1. Normalise all common arrow symbols to '->
    fd_str = fd_str.replace('→', '->').replace('⇒', '->').replace('→', '->')
    fd_str = fd_str.replace('=>', '->').replace('-->', '->')

    # 2. Determine if all user attributes are single letters
    all_single = all(len(a) == 1 for a in user_attrs)

    fds = []
    items = fd_str.split(',')
    for item in items:
        item = item.strip()
        if not item or '->' not in item:
            continue
        lhs_str, rhs_str = item.split('->', 1)

        lhs_tokens = re.findall(r'\w+', lhs_str)
        rhs_tokens = re.findall(r'\w+', rhs_str)

        lhs_set = set()
        for t in lhs_tokens:
            lhs_set.update(_split_attr_token(t, all_single))

        rhs_set = set()
        for t in rhs_tokens:
            rhs_set.update(_split_attr_token(t, all_single))

        if lhs_set and rhs_set:
            fds.append((lhs_set, rhs_set))
    return fds


def closure(attrs: set[str], fds: list[tuple[set[str], set[str]]]) -> set[str]:
    """Standard attribute closure."""
    result = set(attrs)
    while True:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(result) and not rhs.issubset(result):
                result.update(rhs)
                changed = True
        if not changed:
            break
    return result


def find_keys(U: set[str], fds: list[tuple[set[str], set[str]]]):
    """
    Returns:
        candidate_keys (list[set]),
        prime attributes (set),
        non‑prime attributes (set),
        all superkeys (list[set])
    """
    all_subsets = []
    for r in range(len(U) + 1):
        for comb in combinations(U, r):
            all_subsets.append(set(comb))

    candidate_keys = []
    superkeys = []

    for X in all_subsets:           # processed in increasing size
        if closure(X, fds) == U:    # X is a superkey
            superkeys.append(X)
            if not any(ck < X for ck in candidate_keys):
                candidate_keys.append(X)

    prime = set().union(*candidate_keys) if candidate_keys else set()
    nonprime = U - prime
    return candidate_keys, prime, nonprime, superkeys


def format_set(s: set) -> str:
    if not s:
        return '∅'
    return ', '.join(sorted(s)) if s else '∅'
