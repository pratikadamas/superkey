"""
Main routes blueprint — handles the index page (GET/POST).
"""

from flask import Blueprint, render_template, request
from core.key_finder import parse_attributes, parse_fds, find_keys, format_set

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        attr_str = request.form.get('attributes', '')
        fd_str = request.form.get('dependencies', '')

        # 1) Parse user attributes
        attrs_user = parse_attributes(attr_str)

        # 2) Parse FDs, using the list of user attributes for splitting logic
        fds = parse_fds(fd_str, attrs_user)

        # 3) Collect all attributes that appear in FDs (after correct splitting)
        fd_attrs = set()
        for lhs, rhs in fds:
            fd_attrs.update(lhs, rhs)

        # 4) Universe = user attributes + any extra attributes from FDs
        U = set(attrs_user) | fd_attrs

        if not U:
            error = 'Please provide at least one attribute (or FD).'
            return render_template('index.html', error=error)

        cand_keys, prime, nonprime, superkeys = find_keys(U, fds)

        result['candidate_keys'] = [format_set(ck) for ck in cand_keys]
        result['superkeys'] = [format_set(sk) for sk in superkeys]
        result['prime'] = format_set(prime)
        result['nonprime'] = format_set(nonprime)
        result['num_candidate'] = len(cand_keys)
        result['num_superkeys'] = len(superkeys)
        result['U'] = format_set(U)
        result['attributes_input'] = attr_str
        result['dependencies_input'] = fd_str

        if len(U) > 15:
            result['warning'] = (
                'Note: the attribute set is large – enumeration of all '
                'superkeys may be extensive but has been completed.'
            )

    return render_template('index.html', **result)
