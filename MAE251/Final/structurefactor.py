def structureFactor(x, data): 
    """
    :param x: (h, k, l, f_C, f_O, f_N) where f_{} is the scattering factor
    :param data: coordinates of the data in dictionary keyed on element name, value list of tuples 
    
    
    data = {'C': [(-0.0529, 0.0035, 0.0),
              (0.047, 0.0032, 0.0697),
              (-0.0366, -0.0025, 0.1456),
              (0.0592, 0.004, 0.2149),
              (0.0692, 0.0046, 0.3544),
              (-0.0307, -0.002, 0.4242), (0.4471, -0.0035, 0.49),
              (0.547, 0.0032, 0.4202),
              (0.4634, -0.0025, 0.3444),
              (0.5592, 0.004, 0.2751),
              (0.5692, 0.0046, 0.1355),
              (0.4693, -0.002, 0.0658),
              (-0.0529, 0.4965, 0.2144),
              (0.047, 0.5031, 0.2841),
              (-0.0366, 0.4976, 0.36),
              (0.0592, 0.504, 0.4293),
              (0.0692, 0.5046, 0.5688),
              (-0.0307, 0.4979, 0.6385),
              (0.4471, 0.4965, 0.7043),
              (0.547, 0.5031, 0.6346),
              (0.4634, 0.4976, 0.5587),
              (0.5592, 0.504, 0.4894),
              (0.5692, 0.5046, 0.3499),
              (0.4693, 0.4979, 0.2802)
              ],
             'N': [(-0.0082, -0.0006, 0.2813), (0.4918, -0.0006, 0.2087), (-0.0082, 0.4994, 0.4956), (0.4918, 0.4994, 0.4231)],
             'O': [(0.1893, 0.0127, 0.2087), (0.689, 0.0127, 0.2813), (0.1893, 0.512, 0.423), (0.6893, 0.512, 0.4956)]
             }
    """
    def expTerm(coords, h, k, l): 
        """
        (exp(first coords) + exp (second coord) .... exp(last term ))
        
        :param coords: [(x, y, z), (x, y, z) .... (x, y, z)] for given element  
        :param h, k, l: (int)
        """
        tot = 0
        # Iterates over elements coords and computes the exponent term, adds to total
        for coord in coords: 
            a,b,c = coord
            tot += np.exp(2 * np.pi * 1j * (a *h + b * k + c * l))
            
        # Checking if one term is just super small
        tot = complex(tot)
        if abs(tot.imag) <= 1e-10: 
            tot = tot.real
        if abs(tot.real) <= 1e-10: 
            tot = tot.imag
        return tot
    h, k, l, f_c, f_o, f_n = x 

    # Multiplies Scattering Factor by the exponent term 
    # f_{element} = (exp(first coords) + exp (second coord) .... exp(last term ))
    cBuff = f_c * expTerm(data["C"], h, k, l) 
    oBuff = f_o * expTerm(data["O"], h, k, l)
    nBuff = f_n * expTerm(data["N"], h, k, l)
    return cBuff + oBuff + nBuff
