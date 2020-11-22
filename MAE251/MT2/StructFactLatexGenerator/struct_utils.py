import math
import numpy as np
from fractions import Fraction as Fra


class fractObj():
    def __init__(self, n, d):
        self.n = n
        self.d = d

    @property
    def numerator(self):
        return self.n

    @property
    def denominator(self):
        return self.d


def Fraction(x):
    buff = Fra(x).limit_denominator(100000)
    n, d = buff.numerator, buff.denominator
    if n > 1e2:
        return fractObj(round(x, 8), 1)
    else:
        return fractObj(n, d)

def exponentTermLatex(coords, indicies=["h", "k", "l"], simple=False):
    """ exp term e^(2 pi i (h*a + k *b + l * c))
    Fully Expanded
    coords = tuple/array of size 3
    """
    buff = ""
    for i in range(3):
        coor = coords[i]
        miller_idc = indicies[i]
        if coor == 0:
            if simple:
                term = ""
            else:
                term = "0"
        elif coor == 1:
            term = str(miller_idc)
        elif coor%1 == 0:
            term = f"{coor} \cdot {miller_idc}"
        else:
            coor = Fraction(coor)
            if coor.numerator == 1:
                term = f"\\frac{{{miller_idc}}}{{{coor.denominator}}}"
            else:
                term = f"\\frac{{{coor.numerator} \cdot {miller_idc}}}{{{coor.denominator}}}"
        if buff == "":
            buff = term
        elif term != "" :
            buff += " + " + term
    if buff == "":
        buff = "0"
    exp_term = f"e^{{2 \\pi i({buff})}}"
    return exp_term


def create_term(name, coords, indicies=["h", "k", "l"], simple=False):
    """
    Generates term for overal list
    coords is a list of coordinate, name should be element"""
    term = f""
    cnt = 0
    for i in range(len(coords)):
        c = coords[i]
        exp_term = exponentTermLatex(c, indicies=indicies, simple=simple)
        if cnt == 4:
            cnt = 0
            term += "\\\\ \n & \\hspace{0.2cm} "
        if i == 0:
            term = exp_term
        else:
            term += " + " + exp_term
        cnt += 1
    return f"f_{{{name}}} ({term})"


def create_full_eq(data,indicies=["h", "k", "l"]):
    """
    Creates the full term with just variable names;
    data should be a dictionary with key = element name and value = coordinates
    """
    new_line = " \\\\ \n & + "
    eq = f"F_{{{''.join([str(i) for i in indicies])}}} =& \\hspace{{0.2cm}} "
    eq_s = "=& \\hspace{0.2cm} " # Simplified term
    for k, v in data.items():
        eq += create_term(k, v, indicies=indicies) + " \\\\ \n & + "
        eq_s += create_term(k, v, indicies=indicies, simple=True) + " \\\\ \n & + "
    eq  = eq.strip(new_line)  + "\\\\"
    eq_s = eq_s.strip(new_line) + "\\\\"
    return eq + eq_s


def tuple_dot(v1, v2):
    tot = 0
    for a, b in zip(v1, v2):
        tot += a * b
    return tot


def compute_exp(x):
    """
    computes e^(2 pi i (x))
    """
    real = np.cos(2 * np.pi * x)
    imag = np.sin(2 * np.pi * x)
    if abs(real) < 1e-10:
        real = 0
    if abs(imag) < 1e-10:
        imag = 0
    return real, imag


def create_simplified_term(name, coords, reflection):
    """
    name = element
    coords = list of element coords
    reflection = reflection (tuple)
    """
    buff = ""
    buff_computed = ""
    real, imag = 0, 0
    cnt = 0
    cnt_imag = 0
    for c in coords:
        exp_term = tuple_dot(c, reflection)
        # // Less simplified
        if exp_term % 1 == 0:
            term = f"e^{{2  \pi i({int(exp_term)})}}"
        else:
            buff_frac = Fraction(exp_term)
            n, d = buff_frac.numerator, buff_frac.denominator
            term = f"e^{{2 \pi i (\\frac{{{n}}}{{{d}}})}}"
        # More Simplified term  (compute exponents to complex)
        r, i = compute_exp(exp_term)
        real += r  # adding for the final results
        imag += i  # adding for the final results
        if cnt_imag >= 2:
            cnt_imag = 0
            buff_computed += "\\\\ \n & \\hspace{0.2cm}"
        if r == 0 and i == 0:
            computed_term = "0"
        elif r == 0 and i != 0:
            if i % 1 == 0:
                computed_term = f"{int(i)}i"
            else:
                computed_term = f"{round(i, 5)}i"
                cnt_imag += .5

        elif r != 0 and i == 0:
            if r % 1 == 0:
                computed_term = f"{int(r)}"
            else:
                computed_term = f"{round(r, 5)}"
                cnt_imag += .5
        else:
            computed_term = f"[{round(r, 5)} + ({round(i, 5)})i]"

            cnt_imag += 1
        if buff_computed == "":
            buff_computed = computed_term
        else:
            buff_computed += " + " + computed_term

        if cnt == 4:
            cnt = 0
            buff += "\\\\\n&"
        if buff == "":
            buff = term
        else:
            buff += " + " + term + ""
        cnt += 1

    # Final form
    if abs(real) < 1e-10:
        real = 0
    if abs(imag) < 1e-10:
        imag = 0
    if real == 0 and imag == 0:
        simplified_computed = ""
    elif real == 0 and imag != 0:
        if imag % 1 == 0:
            simplified_computed = f"{abs(int(imag))}i f_{{{name}}}"
            if imag > 0:
                simplified_computed = "+ " + simplified_computed
            else:
                simplified_computed = "- " + simplified_computed
        else:
            simplified_computed = f"{abs(imag)}if_{{{name}}}"
            if imag > 0:
                simplified_computed = "+ " + simplified_computed
            else:
                simplified_computed = "- " + simplified_computed
    elif real != 0 and imag == 0:
        if real % 1 == 0:
            simplified_computed = f"{abs(int(real))}f_{{{name}}}"
            if real > 0:
                simplified_computed = "+ " + simplified_computed
            else:
                simplified_computed = "- " + simplified_computed
        else:
            simplified_computed = f"{abs(real)}f_{{{name}}}"
            if real > 0:
                simplified_computed = "+ " + simplified_computed
            else:
                simplified_computed = "- " + simplified_computed
    else:
        simplified_computed = f"+ ({round(real, 5)} + {round(imag, 5)}i)f_{{{name}}}"

    main = f"f_{{{name}}}({buff})"
    computed = f"f_{{{name}}}({buff_computed})"

    return main, computed, simplified_computed


def create_simplified_eq(data, reflection):
    main_func = ""
    comp = ""
    simp_comp = ""
    for k, v in data.items():
        main, computed, simplified_computed = create_simplified_term(k, v, reflection)
        if main_func == "":
            main_func = main
        else:
            main_func += "\\\\\n& + \\hspace{0.2cm}" + main
        if comp == "":
            comp = computed
        else:
            comp += "\\\\\n& + \\hspace{0.2cm}" + computed
        if simp_comp == "":
            simp_comp = simplified_computed.strip("+")
        else:
            if simplified_computed.strip() != "":
                simp_comp += simplified_computed
    if simp_comp.strip() == "":
        simp_comp = "0 (Forbidden Reflection) \\\\"

    main_func = f"=& \\hspace{{0.2cm}}{main_func} \\\\"
    comp = f"=& \\hspace{{0.2cm}}{comp} \\\\"

    simp_comp = f"=& \\hspace{{0.2cm}}{simp_comp} \\\\"
    return main_func, comp, simp_comp


def tuple_to_latex(t):
    final = ""
    for i in t:
        if i%1 != 0:
            i = Fraction(i)
            if i.denominator == 1:
                buff = f"{i.numerator}"
            else:
                buff = f"\\frac{{{i.numerator}}}{{{i.denominator}}}"
        else:
            buff = str(int(i))
        if final == "" :
            final = buff
        else:
            final += "," + buff
    return f"({final})"


def create_tuple_list(l):
    s = "["
    cnt = 0
    for t in l:

        t_latex = tuple_to_latex(t)
        if s == "[":
            s = t_latex
        else:
            if cnt == 6:
                cnt = 0
                s += ",\\\\ & \\hspace{0.2cm}"
            else:
                s += ","
            s += t_latex
        cnt += 1
    return s

def hkl_gen(x):
    """ x is range"""
    ref = []
    for h in range( x + 1):
        for k in range(x  + 1):
            for l in range(x + 1):
                ref.append((h, k,l))
    return ref
