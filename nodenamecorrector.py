#!/usr/bin/env python3
from library.reader import Reader
from library.edits import delete_blanks, clean_tree, clean_nexus_part
from typing import Iterator, TextIO
import warnings
import tkinter.messagebox as tkmessagebox
import sys
import os
from library.gui_utils import *


def clean_newick(file: TextIO) -> Iterator[str]:
    file_w = Reader(file)
    while True:
        tree = file_w.read_until(';\n')
        if not tree:
            break
        yield clean_tree(delete_blanks(tree)) + ';'


def clean_nexus(file: TextIO) -> Iterator[str]:
    file_w = Reader(file)
    while True:
        part = file_w.read_until(';\n').rstrip()
        if not part:
            break
        yield clean_nexus_part(part) + ';'


def clean_wrapper(filename: str) -> None:
    base, ext = os.path.splitext(filename)
    outfile = base + '_corr' + ext
    with open(filename) as file, open(outfile, mode='w') as output:
        if file.readline().startswith('#NEXUS'):
            print('#NEXUS', file=output)
            for part in clean_nexus(file):
                print(part, file=output)
        else:
            file.seek(0, 0)
            for tree in clean_newick(file):
                print(tree, file=output)


def launch_gui() -> None:
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    mainframe = ttk.Frame(root)
    mainframe.rowconfigure(0, weight=1)
    mainframe.columnconfigure(0, weight=1)

    file_chooser = FileChooser(mainframe, label="Input file", mode="open")
    file_chooser.grid(row=0, column=0, sticky='nsew')

    def process() -> None:
        filename = file_chooser.file_var.get()
        try:
            with warnings.catch_warnings(record=True) as warns:
                clean_wrapper(filename)
                for w in warns:
                    tkmessagebox.showwarning(
                        title="Warning", message=str(w.message))
        except Exception as ex:
            tkmessagebox.showerror(title="Error", message=str(ex))

    correct_btn = ttk.Button(mainframe, text="convert", command=process)
    correct_btn.grid(row=1, column=0)

    mainframe.grid(row=0, column=0, sticky='nsew')

    root.mainloop()


def main() -> None:
    try:
        filename = sys.argv[1]
    except IndexError:
        launch_gui()
    else:
        clean_wrapper(filename)


if __name__ == "__main__":
    main()
