import pandas as pd
import numpy as np


class XRD:
    def __init__(self, coords=dict, reflections=list):
        self.coords = coords
        self.reflections = reflections
        self.elements = coords.keys()
        self.df = self.build_base_frame()


    def build_base_frame(self):
        self







