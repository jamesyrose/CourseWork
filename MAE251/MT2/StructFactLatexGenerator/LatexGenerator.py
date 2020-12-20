import os
from struct_utils import *


def create_latex_file(data, reflections, name="temp.txt"):
    horiz_line ="\\noindent\\rule{8cm}{0.4pt} \n"
    master_string = """
    \\documentclass{article}
    \\usepackage{changepage, amsmath,mathpazo,tikz}
    \\usepackage{pdflscape}
    \\usepackage%
    [%
    a4paper
    ]{geometry}
    \\begin{document}
    \\begin{landscape}
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
        master_string += "\n \\end{align*} \n \\newpage \n " + horiz_line
    master_string +=  "\n\\end{landscape}\n \\end{document}"
    with open(name, "w") as f:
        f.writelines(master_string)
        f.close()
    os.system(f"pdflatex {name}")

if __name__ == "__main__":
    # Test
    data = {"Co": [(1/3, 2/3, 1/6), (1,1,1/2), (2/3, 1/3, 5/6)],
            "O": [(0, 0, 0.23958700), (2/3,1/3, 0.09374633), (2/3, 1/3, 0.57292033), (1/3, 2/3, 0.42707967), #[(0, 0, 23959/100000), (2/3,1/3, 9375/100000), (2/3, 1/3, 57292/100000), (1/3, 2/3, 42708/100000),
                  (1/3, 2/3, 0.90625367), (0,0,0.76041300)],# (1/3, 2/3, 90625/100000), (0,0,76041/100000)],
            "Li": [(0,0,0), (2/3, 1/3, 1/3), (1/3,2/3, 2/3)]}
    reflections = [(1,0,1), (-1,0,1), (1,0,-1), (0,1,1), (0,-1,1),(0,1,-1),(0,-1,-1),(-1,1,1),(0,-1,1),(-1,1,-1),(1,-1,-1),(-1,-1,-1)]


# [ (1,0,1), (0,1,1), (1,0,2),(0,1,2)] # (-2, 1,0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3),
                   # (2, 1, 0), (1, 1, 1), (1, 1, 2), (1, 1, 3), (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 0, 3),
                   # (2, 1, 0), (2, 1, 1), (2, 1, 2), (2, 1, 3), (3, 0, 0), (3, 0, 1), (3, 0, 2)]


    # reflections = hkl_gen(5)
    create_latex_file(data, reflections, name="FullLiCoO2_104.txt")

