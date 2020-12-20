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