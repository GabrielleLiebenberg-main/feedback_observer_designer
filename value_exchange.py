# -*- coding: utf-8 -*-
"""
Central module that handles the variables needed for controller/observer 
calculations across modules.

The class ValueExchange is used to store the necessary variables as attributes, 
allowing them to be accessed by any module that imports this one.

REQUIRED MODULES:
    NONE
    
EXAMPLE:
    import value_exchange as ve
    
    ve.valueExchange.setPoles(z_sigma, z_wd, T)
    [sigma, wd, T] = ve.valueExchange.getPoles() 

Created on Thu Mar  2 09:17:59 2023

@author: 22546723
"""
import numpy as np

class ValueExchange:    
    
    def __init__(self, sigma, wd, z_sigma, z_wd, T, F, g, c, d, dim):
        """
        Initializes the ValueExchange class and assigns the initial parameter
        values

        Parameters
        ----------
        sigma : double
            Time domain sigma value
        wd : double
            Time domain w_d value
        z_sigma : double
            Discrete sigma value
        z_wd : double
            Discrete w_d value
        T : double
            Sample time
        F : array of double, size [dim][dim]
            Discrete system matrix
        g : array of double, size [dim][1]
            Discrete input matrix
        c : array of double, size [1][dim]
            Discrete output matrix
        d : double
            Direct feedthrough term
        dim : int
            Maximum dimension of the system model matrices

        Returns
        -------
        None.

        """
        self.sigma = sigma
        self.wd = wd
        self.z_sigma = z_sigma
        self.z_wd = z_wd
        self.T = T
        self.F = F
        self.g = g
        self.c = c
        self.d = d
        self.dim = dim
        
    def setRequirements(self, sigma, wd):
        """
        Sets instance requirements.

        Parameters
        ----------
        sigma : double
            Time domain sigma value
        wd : double
            Time domain w_d value

        Returns
        -------
        None.

        """
        self.sigma = sigma
        self.wd = wd
        
    def getRequirements(self):
        """
        Returns instance requirements

        Returns
        -------
        sigma : double
            Time domain sigma value
        wd : double
            Time domain w_d value

        """
        sigma = self.sigma
        wd = self.wd
        return sigma, wd

    def setPoles(self, z_sigma, z_wd, T):
        """
        Sets instance poles.

        Parameters
        ----------
        z_sigma : double
            Discrete sigma value
        z_wd : double
            Discrete w_d value
        T : double
            Sample time

        Returns
        -------
        None.

        """
        self.z_sigma = z_sigma
        self.z_wd = z_wd
        self.T = T
        
    def getPoles(self):
        """
        Returns instance poles.

        Returns
        -------
        z_sigma : double
            Discrete sigma value
        z_wd : double
            Discrete w_d value
        T : double
            Sample time

        """
        z_sigma = self.z_sigma
        z_wd = self.z_wd
        T = self.T
        return z_sigma, z_wd, T

    def setModel(self, F, g, c, d):
        """
        Sets instance model.

        Parameters
        ----------
        F : array of double, size [dim][dim]
            Discrete system matrix
        g : array of double, size [dim][1]
            Discrete input matrix
        c : array of double, size [1][dim]
            Discrete output matrix
        d : double
            Direct feedthrough term

        Returns
        -------
        None.

        """
        self.F = F
        self.g = g
        self.c = c
        self.d = d
        
    def getModel(self):
        """
        Returns instance model.

        Returns
        -------
        F : array of double, size [dim][dim]
            Discrete system matrix
        g : array of double, size [dim][1]
            Discrete input matrix
        c : array of double, size [1][dim]
            Discrete output matrix
        d : double
            Direct feedthrough term

        """
        F = self.F
        g = self.g
        c = self.c
        d = self.d
        return F, g, c, d

    def setSize(self, dim):
        """
        Sets instance dimension.

        Parameters
        ----------
        dim : int
            Maximum dimension of the system model matrices

        Returns
        -------
        None.

        """
        self.dim = dim
        
    def getSize(self):
        """
        Returns instance dimension.

        Returns
        -------
        dim : int
            Maximum dimension of the system model matrices

        """
        dim = self.dim
        return dim

#initialize class
dim = 1
F = np.empty(shape=(dim,dim))
g = np.empty(shape=(dim,1))
c = np.empty(shape=(1,dim))
valueExchange = ValueExchange(0, 0, 0, 0, 0, F, g, c, 0, dim)
