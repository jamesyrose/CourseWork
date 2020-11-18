import os
from struct_utils import *


def create_latex_file(data, reflections, name="temp.txt"):
    horiz_line ="\\noindent\\rule{8cm}{0.4pt} \n"
    master_string = """
    \\documentclass{article}
    \\usepackage{changepage, amsmath,mathpazo,tikz}
    \\begin{document}
        \\begin{align*} 
        Coordinates \\\\
    """
    for k, v in data.items():
        master_string += f"{k} :& \\hspace{{0.2cm}} {create_tuple_list(v)} \\\\ \n"
    master_string += f"Reflections :& \\hspace{{0.2cm}} {create_tuple_list(reflections)} \\\\ \n"
    master_string += """ \\end{align*} 
        \\noindent\\rule{8cm}{0.4pt}
        \\begin{align*} 
    """
    default_eq = create_full_eq(data) # The general eq w/o reflections
    master_string += default_eq + "\n \\end{align*} \n" + horiz_line
    for r in reflections:
        master_string += "\\begin{align*} \n"
        expanded = create_full_eq(data, r)
        s1, s2, s3 = create_simplified_eq(data, r)

        master_string += expanded + s1 + s2 + s3
        master_string += "\n \\end{align*} \n" + horiz_line
    master_string +=  "\n \\end{document}"
    with open(name, "w") as f:
        f.writelines(master_string)
        f.close()
    os.system(f"pdflatex {name}")

if __name__ == "__main__":
    # Test
    data = {"Ag": [(0, 0, 0), (0, 1 / 2, 1 / 4), (1 / 2, 0, 3 / 4), (1 / 2, 1 / 2, 1 / 2)],
            "Al": [(1 / 2, 1 / 2, 0), (1 / 2, 0, 1 / 4), (0, 0, 1 / 2), (0, 1 / 2, 3 / 4)],
            "Te": [(1 / 4, 1 / 4, 1 / 8), (3 / 4, 3 / 4, 1 / 8), (3 / 4, 1 / 4, 3 / 8), (1 / 4, 3 / 4, 3 / 8),
                   (3 / 4, 3 / 4, 5 / 8), (1 / 4, 1 / 4, 5 / 8), (3 / 4, 1 / 4, 7 / 8), (1 / 4, 3 / 4, 7 / 8)]}
    reflections = [(0, 0, 2), (0, 1, 1), (1, 1, 0), (1, 1, 2), (0, 1, 3), (0, 2, 0), (0, 0, 4), (0, 2, 2), (2, 1, 1),
                   (1, 1, 4), (1, 2, 3), (2, 2, 0),
                   (0, 1, 5), (0, 2, 4), (2, 2, 2), (0, 3, 1), (3, 1, 0), (3, 1, 2), (1, 2, 5), (3, 2, 1), (1, 3, 4),
                   (2, 3, 3), (0, 4, 0), (0, 4, 2),
                   (4, 1, 1), (3, 3, 2), (4, 1, 3), (4, 2, 0), (2, 3, 5), (3, 3, 4), (1, 4, 5), (2, 4, 4), (4, 3, 1),
                   (0, 5, 1), (5, 1, 0), (5, 1, 2),
                   (0, 0, 0)]
    create_latex_file(data, reflections, name="test.txt")