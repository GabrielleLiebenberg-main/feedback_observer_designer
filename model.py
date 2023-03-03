# -*- coding: utf-8 -*-
"""
A module for entering and calculating a state space model

The model module initialises a GUI that allows the user to enter a 
continuous or discrete state space model. If a continuous model is added, the 
discrete mdel is calculated and displayed.

REQUIRED MODULES:
    value_exchange
    
EXAMPLE:
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)

    tab_model = ttk.Frame(tabControl)
    tabControl.add(tab_model, text ='Model')    
    
    initValueExchange()
    setupModel(tab_model)
    
Created on Thu Mar  2 09:36:51 2023

@author: 22546723
"""
import numpy as np
import tkinter as tk					
from tkinter import ttk

import value_exchange as ve

def writeDisc(disc_val, dim, disc_entries):
    """
    Diplays the discrete model

    Parameters
    ----------
    disc_val : list containing arrays of type double
        List containing the discrete matrices to be shown [F, g, c, d]
    dim : int
        Dimension of the F/A matrices
    disc_entries : list of ttk.Entry
        List containing the discrete entry fields [e_F, e_g, e_c, e_d]

    Returns
    -------
    None.

    """
    #set entries from input
    e_F = disc_entries[0]
    e_g = disc_entries[1]
    
    #set values from input
    F = disc_val[0]
    g = disc_val[1]
    
    #run through both value arrays and display the values
    for r in range(0,dim):
        e_g[r,0].delete(0, tk.END)
        e_g[r,0].insert(0,g[r,0])         
        for col in range(0,dim):
            e_F[r,col].delete(0, tk.END)
            e_F[r,col].insert(0,F[r,col])


def readCont(cont_entries, dim):
    """
    Read the values of the continuous model input matrices

    Parameters
    ----------
    cont_entries : list of ttk.Entry
        List containing the continuous entry fields [e_A, e_b, e_c, e_d]
    dim :int
        Dimension of the F/A matrices

    Returns
    -------
    A : array of double, size [dim][dim]
        Continuous system matrix
    b : array of double, size [dim][1]
        Continuous input matrix
    c : array of double, size [1][dim]
        Continuous output matrix
    d : double
        Direct feedthrough term

    """
    #set entries from input
    e_A = cont_entries[0]
    e_b = cont_entries[1]
    e_c = cont_entries[2]
    e_d = cont_entries[3]
    
    #set values from input
    A = np.empty(shape=(dim,dim))
    b = np.empty(shape=(dim,1))
    c = np.empty(shape=(1,dim))    
    d = float(e_d.get())
    
    #loop through the entered matrices and store the values
    for r in range(0,dim):
        b[r,0] = float(e_b[r,0].get())
        c[0,r] = float(e_c[0,r].get())
        for col in range(0,dim):
            A[r,col] = float(e_A[r,col].get())        
        
    return A, b, c, d

def calcDisc(cont_val, T, dim):
    """
    Calculate the discrete model from the continouos one

    Parameters
    ----------
    cont_val : list containing arrays of type double
        List containing the continuous matrices [A, b, c, d]
    T : double
        Sample time
    dim : int
        Dimension of the F/A matrices

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
    #assign values from input
    A = cont_val[0]
    b = cont_val[1]
    c = cont_val[2]
    d = cont_val[3]
    
    #calculate F matrix
    Im = np.identity(dim)
    F = Im + A*T + 0.5*np.matmul(A*T, A*T)
    
    #calculate psi matrix
    psi = Im + 0.5*A*T + (1/6)*np.matmul(A*T, A*T)
    
    #calculate g matrix
    g = T*np.matmul(psi,b)
    
    return F, g, c, d
    
    
def readDisc(disc_entries, dim):   
    """
    Reads and returns the entered discrete matrices

    Parameters
    ----------
    disc_entries : list of ttk.Entry
        List containing the discrete entry fields [e_F, e_g, e_c, e_d]
    dim : int
        Dimension of the F/A matrices

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
    #assign entries from input
    e_F = disc_entries[0]
    e_g = disc_entries[1]
    e_c = disc_entries[3]
    e_d = disc_entries[0]
    
    #initialise discrete values
    F = np.empty(shape=(dim,dim))
    g = np.empty(shape=(dim,1))
    c = np.empty(shape=(1,dim))
    d = float(e_d.get())
    
    #loop through the inputs and assign values
    for r in range(0,dim):
        g[r,0] = float(e_g[r,0].get())
        c[0,r] = float(e_c[0,r].get())
        for col in range(0,dim):
            F[r,col] = float(e_F[r,col].get())         
        
    return F, g, c, d
    
    
def calcModel(v, cont_entries, disc_entries, dim): 
    """
    Calculates and displays the discrete model from the continuous matrices or read it from 
    the entries. Also sets the value_exchange model

    Parameters
    ----------
    v : tk.IntVar
        Variable indicating the radio group selection
    cont_entries : list of ttk.Entry
        List containing the continuous entry fields [e_A, e_b, e_c, e_d]
    disc_entries : list of ttk.Entry
        List containing the discrete entry fields [e_F, e_g, e_c, e_d]
    dim : int
        Dimension of the F/A matrices

    Returns
    -------
    None.

    """
    #read the radio group
    if v.get()==2:
        #calculate and display the discrete matrices
        T = ve.valueExchange.getPoles()[2]
        cont_val = readCont(cont_entries, dim)
        disc_val = calcDisc(cont_val, T, dim)
        writeDisc(disc_val, dim, disc_entries)
    if v.get()==1:
        #read the discrete matrix
        disc_val = readDisc(disc_entries, dim)
        
    #get the matrices from the read/calculated values
    F = disc_val[0]
    g = disc_val[1] 
    c = disc_val[2]
    d = disc_val[3]
        
    #set the value_exchange model
    ve.valueExchange.setModel(F, g, c, d)

def spaceLabels(labels, dim):
    """
    Display the labels with the correct spacing

    Parameters
    ----------
    labels : list of ttk.Label
        List containing the labels 
    dim : int
        Dimension of the F/A matrices

    Returns
    -------
    None.

    """
    #assign labels from the input
    l_F = labels[0]
    l_g = labels[1]
    l_A = labels[2]
    l_b = labels[3]
    l_c = labels[4]
    l_d = labels[5]
    l_gap  = labels[6]   

    #display and pace the labels
    l_F.grid(row=2, column=0, pady=2)
    l_g.grid(row=2, column=dim+1, pady=2)
    l_c.grid(row=dim+4, column=0, pady=2)
    l_d.grid(row=dim+4, column=dim+1, pady=2)

    l_A.grid(row=2, column=dim+3, pady=2)
    l_b.grid(row=2, column=2*dim+5, pady=2) 
    
    l_gap.grid(row=dim+3, column=0, pady=2) 


def spaceInputs(frame, dim, v):
    """
    Display the entry fields and calculate button with the correct spacing

    Parameters
    ----------
    frame : ttk.Frame
        Frame the entries should be added to
    dim : int
        Dimension of the F/A matrices
    v : tk.IntVar
        Variable indicating the radio group selection

    Returns
    -------
    None.

    """
    #initialize the entry field matrices
    e_F = np.empty(shape=(dim,dim), dtype=ttk.Entry)
    e_g = np.empty(shape=(dim,1), dtype=ttk.Entry)
    e_A = np.empty(shape=(dim,dim), dtype=ttk.Entry)
    e_b = np.empty(shape=(dim,1), dtype=ttk.Entry)
    e_c = np.empty(shape=(1,dim), dtype=ttk.Entry)
    e_d = ttk.Entry(frame)
    
    #populate and display the F matrix entries
    for r in range(2,dim+2):
        for col in range(1,dim+1):
            ent = ttk.Entry(frame)
            ent.grid(row=r, column=col, padx=2, pady=2)
            e_F[r-2,col-1] = ent
    
    #populate and display the g matrix entries
    for r in range(2,dim+2):
        ent = ttk.Entry(frame)
        ent.grid(row=r, column=dim+2, padx=2, pady=2)
        e_g[r-2,0] = ent    

    #populate and display the A matrix entries
    for r in range(2,dim+2):
        for col in range(dim+4,2*dim+4):
            ent = ttk.Entry(frame)
            ent.grid(row=r, column=col, padx=2, pady=2)
            e_A[r-2,col-(dim+4)] = ent

    #populate and display the b matrix entries
    for r in range(2,dim+2):
        ent = ttk.Entry(frame)
        ent.grid(row=r, column=2*dim+6, padx=2, pady=2)
        e_b[r-2,0] = ent 

    #populate and display the c matrix entries
    for col in range(1,dim+1):
        ent = ttk.Entry(frame)
        ent.grid(row=dim+4, column=col, padx=2, pady=2)
        e_c[0,col-1] = ent   
 
    #display the d entry field
    e_d.grid(row=dim+4, column=dim+2, padx=2, pady=2)
    
    #group entry matrices
    cont_entries = [e_A, e_b, e_c, e_d]
    disc_entries = [e_F, e_g, e_c, e_d]
    
    #add calculate button
    b_calc_disc = ttk.Button(frame, text="Set discrete model", command=lambda: calcModel(v, cont_entries, disc_entries, dim))    
    b_calc_disc.grid(row=dim+7, column=0, pady=2)


def setDim(frame, e_dim, labels, v): 
    """
    Reads the matrix dimension entry field, spaces the labels and the entries.
    Also sets the dimension in value_exchange

    Parameters
    ----------
    frame : ttk.Frame
        Frame the entries should be added to
    e_dim : ttk.Entry
        Entry the dimension should be read from
    labels : list of ttk.Label
        List containing the labels 
    v : tk.IntVar
        Variable indicating the radio group selection

    Returns
    -------
    None.

    """
    #read dimension
    dim=int(e_dim.get()) 
    
    #space the labels and entries
    spaceLabels(labels, dim)
    spaceInputs(frame, dim, v)
    
    #set the dimension in value_exchange
    ve.valueExchange.setSize(dim)
        
def setupModel(frame):
    """
    Initialises the model GUI.
    
    This is the only function that needs to be called to use the module. 
    It initialises the GUI and sets the 'set dimensions' button command.  

    Parameters
    ----------
    frame : ttk.Frame
        Frame the GUI should be built on

    Returns
    -------
    None.

    """
    #radio group setup
    v = tk.IntVar(frame, 1)
    values = {"Set discrete" : 1,
            "Set continuous" : 2}
    for (text, value) in values.items():
        rb_dc = ttk.Radiobutton(frame, text = text, variable = v,
            value = value)
        rb_dc.grid(row=0, column=value-1, pady=2)
    
    #dimension label setup
    l_dim = ttk.Label(frame, text="A/F dimensions:")
    l_dim.grid(row=1, column=0, pady=2)
    
    #dimension entry setup
    e_dim = ttk.Entry(frame, text="1")
    e_dim.grid(row=1, column=1, pady=2)

    #discrete/continuous label setup
    l_F = ttk.Label(frame, text="F:")
    l_g = ttk.Label(frame, text="g:")
    l_c = ttk.Label(frame, text="c:")
    l_d = ttk.Label(frame, text="d:")
    l_A = ttk.Label(frame, text="A:")
    l_b = ttk.Label(frame, text="b:")

    #add a blank label for formatting
    l_gap = ttk.Label(frame, text=" ")
    
    #group labels
    labels = [l_F, l_g, l_A, l_b, l_c, l_d, l_gap]
    
    #set dimension button setup
    b_set_dim = ttk.Button(frame, text="set dimensions", command=lambda: setDim(frame, e_dim, labels, v))
    b_set_dim.grid(row=1, column=2, pady=2, padx=10)
    
    #initial label spacing
    dim = 1
    spaceLabels(labels, dim)