from library.ext_ASCII_conv_table import ext_ascii_trans

import re
import unicodedata


def delete_blanks(s: str) -> str:
    """
    Deletes whitespace in a string
    """
    return re.sub(r'\s+', '', s)


def sanitize_match(m: re.Match) -> str:
    """
    Correct the special characters in the match
    """
    delim_left = m.group(0)[0]
    delim_right = m.group(0)[-1]
    s = m.group(0)[1:-1]
    return delim_left + sanitize(re.compile(r'[A-Za-z0-9]+'), s) + delim_right


def sanitize(allowed: re.Pattern, s: str) -> str:
    s = unicodedata.normalize('NFKC', s).translate(ext_ascii_trans)
    return '_'.join(m.group(0) for m in re.finditer(allowed, s))


def clean_tree(s: str) -> str:
    if re.search(r'\[&', s):
        regex = re.compile(r'\([^([]+\[|,[^,[]+\[')
    elif re.search(r':\d', s):
        regex = re.compile(r'\([^(:]+:|,[^,:]+:')
    else:
        regex = re.compile(r'\([^(,]+,|,[^,]+,|,[^,)]\)')
    return regex.sub(sanitize_match, s)


def find_tree_start(s: str) -> int:
    """
    finds index of the start of a tree
    """
    tree_end = s.rindex(')')
    closing = 1
    for i, c in enumerate(reversed(s[0:tree_end])):
        if c == ')':
            closing += 1
        elif c == '(':
            closing -= 1
        if closing == 0:
            return i
    else:
        return 0


def clean_nexus_part(s: str) -> str:
    if re.match(r'\s*Taxlabes', s):
        return sanitize(re.compile(r'[A-Za-z0-9\s]+'), s)
    elif re.match(r'\s*Translate', s):
        return sanitize(re.compile(r'[A-Za-z0-9,\s]+'), s)
    elif re.match(r'\s*tree', s):
        tree_start = find_tree_start(s)
        return s[0:tree_start] + clean_tree(s[tree_start:])
    else:
        return s
