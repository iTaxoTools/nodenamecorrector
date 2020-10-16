from library.reader import Reader
from library.edits import delete_blanks, clean_tree
from typing import Iterator, TextIO
import sys
import os.path


def clean_newick(file: TextIO) -> Iterator[str]:
    file_w = Reader(file)
    while (tree := file_w.read_until(';\n')):
        yield clean_tree(delete_blanks(tree))


def clean_wrapper(filename: str) -> None:
    base, ext = os.path.splitext(filename)
    outfile = base + '_corr' + ext
    with open(filename) as file, open(outfile) as output:
        if file.readline().startswith('#NEXUS'):
            raise NotImplementedError("Nexus is not supported yet")
        else:
            file.seek(0, 0)
            for tree in clean_newick(file):
                print(tree, file=output)


def main() -> None:
    try:
        filename = sys.argv[1]
    except IndexError:
        pass
    else:
        clean_wrapper(filename)


if __name__ == "__main__":
    main()
