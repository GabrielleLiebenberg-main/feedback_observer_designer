# -*- coding: utf-8 -*-
"""
A module for calculating a discrete feedback controller and observer

The results module initialises a GUI that calculates and displays the discrete 
feedback controller and observer of a system using a given discrete model, 
closed loop poles and sample time.

REQUIRED MODULES:
    value_exchange
    
EXAMPLE:
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)

    tab_results = ttk.Frame(tabControl)
    tabControl.add(tab_results, text ='Results')    
    
    initValueExchange()
    setupModel(tab_results)
    
Created on Thu Mar  2 10:03:08 2023

@author: 22546723
"""
import numpy as np
import sympy as sp				
from tkinter import ttk

import value_exchange as ve


def calcK(F, poles, U, dim):
    """
    Calculates the discrete feedback controller.
    
    Uses the discrete model, poles dimension and controllability matrix of a
    discrete system to calculate the feedback controller

    Parameters
    ----------
    F : array of double, size [dim][dim]
        Discrete system matrix
    poles : list of double
        System poles in z-plane
    U : array of double, size [dim][dim]
        Controllability matrix
    dim : int
        System matrix dimension

    Returns
    -------
    k : array of double, size [1][dim]
        Feedback gain
    k_c : array of double, size [1][dim]
        Control canonical feedback gain
    P : array of double, size [dim][dim]
        Transformation matrix

    """
    
    #set values from inputs
    z_sigma = poles[0]
    z_wd = poles[1]
    
    #initialize matrices
    k_c = np.zeros(shape=(1, dim))
    k = np.zeros(shape=(1, dim))
    P = np.zeros(shape=(dim, dim))
    U_c = np.zeros(shape=(dim, dim))
    
    #NOTE: alpha is a symbolic array
    a = sp.zeros(dim)
    alpha = sp.zeros(dim)    
    
    #get open loop equation
    #NOTE: this gives a symbolic equation
    z = sp.Symbol('z')
    F_sym = sp.Matrix(F)
    Id = sp.eye(dim)
    temp = z*Id - F_sym
    ol_eqn = temp.det()
    
    #get closed loop equation
    cl_eqn = (z - z_sigma - sp.I*z_wd)*(z - z_sigma + sp.I*z_wd)
    cl_eqn = cl_eqn.as_poly()
    cl_eqn = cl_eqn.as_expr()
        
    #get the coefficients and k_c from the open and closed loop equations
    for i in range(0, dim):
        a[dim-1- i] = cl_eqn.coeff(z,i)
        alpha[dim-1- i] = ol_eqn.coeff(z,i)
        k_c[0, i] = a[0,dim-1- i] - alpha[0,dim-1- i]
 
    #change array type from a symbolic array to a numpy array
    alpha = np.array(alpha).astype(np.float64) 
    
    #calculate U_c^(-1)
    for i in range(0, dim):
        for j in range(0,dim):
            if j<(dim-i-1):
                U_c[i,j] = alpha[0,dim-2-j-i]
            if j == dim-i-1:
                U_c[i,j] = 1
    
    #calculate P and use it to get k
    P = np.matmul(U, U_c)
    k = np.matmul(k_c,np.linalg.inv(P))
    
    return k, k_c, P
    
def checkContr(model, poles, dim):
    """
    Checks the system for controllability. If it is controllable, calculates the 
    feedback gain.

    Parameters
    ----------
    model : list containing arrays of type double
        List containing the discrete matrices of the system [F, g, c, d]
    poles : list of double
        System poles in the z-plane [sigma, wd]
    dim : int
        Maximum dimension of the system model matrices

    Returns
    -------
    k : array of double, size [1][dim]
        Feedback gain
    k_c : array of double, size [1][dim]
        Control canonical feedback gain
    P : array of double, size [dim][dim]
        Transformation matrix
    detU : double
        Determinant of the controllability matrix

    """
    #set values from input
    F = model[0]
    g = model[1]
      
    #initialize controllability matrix
    U = np.zeros(shape=(dim, dim))
    
    #set first row of U
    for j in range(0, dim):
        U[j, 0] = g[j, 0]    
        
    #set the remaining rows of U
    for i in range(1, dim):
        #get F^i 
        F_new = F      
        for j in range(1,i):
            F_new = np.matmul(F_new, F)
            
        #set U
        temp = np.matmul(F_new, g)
        for j in range(0, dim):
            U[j, i] = temp[j, 0]
            
    #determine controllability and calculate feedback controller if possible        
    detU = np.linalg.det(U)
    
    if not (detU==0):
        [k, k_c, P] = calcK(F, poles, U, dim)        
    else:
        print("system not controlable")
        [k, k_c, P] = [0, 0, 0]
        
    return k, k_c, P, detU
        
def calcM(model, poles, V):
    """
    Calculates the observer.
    
    Uses the discrete model, poles dimension and observability matrix of a
    discrete system to calculate the observer.

    Parameters
    ----------
    model : list containing arrays of type double
        List containing the discrete matrices of the system [F, g, c, d]
    poles : list of double
        System poles in the z-plane [sigma, wd]
    V : array of double, size [dim][dim]
        Observability matrix

    Returns
    -------
    m_c : array of double, size [dim][1]
        Current observer
    m_p : array of double, size [dim][1]
        Prediction observer

    """
    # TODO: finish the observer calclations
    F = model[0]
    g = model[1]
    c = model[2]
    d = model[3]
    
    z_sigma = poles[0]
    z_wd = poles[1]
    
    print("function not yet implemented")
    m_c = np.array([[1], [1]])
    m_p = np.array([[2], [2]])
    return m_c, m_p

def checkObs(model, poles, dim):
    """
    Checks the system for observability. If it is observable, calculates the 
    prediction and current observers   

    Parameters
    ----------
    model : list containing arrays of type double
        List containing the discrete matrices of the system [F, g, c, d]
    poles : list of double
        System poles in the z-plane [sigma, wd]
    dim : int
        Maximum dimension of the system model matrices

    Returns
    -------
    m_c : array of double, size [dim][1]
        Current observer
    m_p : array of double, size [dim][1]
        Prediction observer
    detV : double
        Determinant of the observability matrix

    """
    #set values from input
    F = model[0]
    c = model[2]
    
    #initialize observability matrix
    V = np.zeros(shape=(dim, dim))
    
    #set first column of V
    for j in range(0, dim):
        V[0, j] = c[0,j]    
        
    #set the rest of V
    for i in range(1, dim):
        #calculate F^i
        F_new = F
        for j in range(1,i):
            F_new = np.matmul(F_new, F)
            
        #set V
        temp = np.matmul(c, F_new)
        for j in range(0, dim):
            V[i, j] = temp[0,j]
            
    #determine observability and calculate observers if possible       
    detV = np.linalg.det(V)
    
    if not (detV==0):
        [mc, mp] = calcM(model, poles, V)       
    else:
        print("system not observable")
        [mc, mp] = [0, 0, 0]
        
    return mc, mp, detV
    

def setLayout(feedback, observer, b_calc_res, dim, frame):
    """
    Displays the results as labels.

    Parameters
    ----------
    feedback : list containing arrays of type double
        Feedback controller values [k, k_c, P, detU]
    observer : list containing arrays of type double
        Observer values [m_c, m_p, detV]
    b_calc_res : ttk.Button
        Calculate button
    dim : int
        Maximum dimension of the system model matrices
    frame : ttk.Frame
        Frame the results should be added to

    Returns
    -------
    None.

    """
    #set values from inputs
    k = feedback[0]
    k_c = feedback[1]
    P = feedback[2]
    detU = feedback[3]
    
    m_c = observer[0]
    m_p = observer[1]
    detV = observer[2]
    
    #construct strings
    str_du = "|U|: \n" + str(detU)
    str_dv = "|V|: \n" + str(detV)
    str_k = "k: \n" + np.array2string(k)
    str_k_c = "k_c: \n" + np.array2string(k_c)
    str_m_c = "m_c: \n" + np.array2string(m_c)
    str_m_p = "m_p: \n" + np.array2string(m_p)
    str_p = "P: \n" + np.array2string(P)
    
    #initialize labels
    l_du = ttk.Label(frame, text=str_du)
    l_dv = ttk.Label(frame, text=str_dv)
    l_k = ttk.Label(frame, text=str_k)
    l_kc = ttk.Label(frame, text=str_k_c)
    l_p = ttk.Label(frame, text=str_p)
    l_mc = ttk.Label(frame, text=str_m_c)
    l_mp = ttk.Label(frame, text=str_m_p) 
    
    #display labels
    l_du.grid(row=0, column=0, pady=2, padx=10)
    l_dv.grid(row=0, column=1, pady=2, padx=10)
    l_k.grid(row=1, column=0, pady=2, padx=10)
    l_kc.grid(row=2, column=0, pady=2, padx=10)
    l_p.grid(row=3, column=0, pady=2, padx=10)
    l_mc.grid(row=1, column=1, pady=2, padx=10)
    l_mp.grid(row=2, column=1, pady=2, padx=10)
    
    #set button position
    b_calc_res.grid(row=2*dim+2, column=0, pady=2, padx=10)
    
    
def calcRes(b_calc_res, frame):
    """
    Gets and displays the results using the other functions.
    
    Gets the system matrices, their dimensions and poles from value_exchange. 
    Then calls checkContr and checkObs to calculate the feedback controller and 
    observer. Also calls the setLayout function to display the results.

    Parameters
    ----------
    b_calc_res : ttk.Button
        Calculate button
    frame : ttk.Frame
        Frame the results should be added to

    Returns
    -------
    None.

    """
    #get dimensions, poles and model from value_exchange
    dim = ve.valueExchange.getSize()    
    model = ve.valueExchange.getModel()    
    [sigma, wd, T] = ve.valueExchange.getPoles()   
    poles = [sigma, wd]
    
    #calculate the feedback controller and observer
    feedback = checkContr(model, poles, dim)
    observer = checkObs(model, poles, dim)  

    #display the results
    setLayout(feedback, observer, b_calc_res, dim, frame)    
    
def setupResults(frame):
    """
    Initialises the results GUI.
    
    This is the only function that needs to be called to use the module. 
    It initialises the GUI and sets the calcuate button command. 

    Parameters
    ----------
    frame : ttk.Frame
        Frame the GUI should be built on

    Returns
    -------
    None.

    """
    #setup calculate button
    b_calc_res = ttk.Button(frame, text="calculate", command=lambda: calcRes(b_calc_res, frame))
    b_calc_res.grid(row=0, column=0, pady=2, padx=10)
