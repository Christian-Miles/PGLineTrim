from airfoil import Airfoil
import numpy as np
import scipy as sp


class Rib:
    """A standard paragliding rib containing an airfoil and port holes to allow for """
    def __init__(self, position=None, rotation=None, airfoil: Airfoil = None) -> None:
        self.airfoil: Airfoil | None = airfoil
        self.position = position
        self.rotation = rotation
        self.cross_ports = []

    def insert_crossport(self, position, shape):
        raise NotImplementedError()
        
    

class HRib:
    # To Do
    raise NotImplementedError()

class VRib:
    # To Do
    raise NotImplementedError()