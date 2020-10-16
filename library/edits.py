from library.ext_ASCII_conv_table import ext_ascii_trans

import re
import unicodedata


def delete_blanks(s: str) -> str:
    """
    Deletes whitespace in a string
    """
    return re.sub(r'\s+', '', s)


def sanitize(m: re.Match) -> str:
    """
    Correct the special characters in the match
    """
    delim_left = m.group(0)[0]
    delim_right = m.group(0)[-1]
    s = m.group(0)[1:-1]
    s = unicodedata.normalize('NFKC', s).translate(ext_ascii_trans)
    return delim_left + '_'.join(m.group(0) for m in re.finditer(r'[A-Za-z0-9]+', s)) + delim_right


def clean_tree(s: str) -> str:
    if re.search(r'\[&', s):
        regex = re.compile(r'\([^([]+\[|,[^,[]+\[')
    elif re.search(r':\d', s):
        regex = re.compile(r'\([^(:]+:|,[^,:]+:')
    else:
        regex = re.compile(r'\([^(,]+,|,[^,]+,|,[^,)]\)')
    return regex.sub(sanitize, s)
