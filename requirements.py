# -*- coding: utf-8 -*-
"""
A module for entering and processing time domain requirements

The requirements module initialises a GUI that has entry fieds for the 
following time domain values: w_n, zeta, t_s(2%), t_r, t_p, w_d, sigma.
It uses entered values to calculate the requirements not entered and displays 
them in the relevant entry fields.

REQUIRED MODULES:
    value_exchange
    
EXAMPLE:
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)

    tab_requirements = ttk.Frame(tabControl)
    tabControl.add(tab_requirements, text ='Set desired parameters')
    
    initValueExchange()
    setupRequirements(tab_requirements)

Created on Thu Mar  2 09:05:21 2023

@author: 22546723
"""
import numpy as np
import tkinter as tk					
from tkinter import ttk

import value_exchange as ve

def calcRequirements(requirements):
    """
    Calculate the time domain requirements.
    
    The function uses the given time domain requirements (unentered values are 
    passed as zero) and calculates the unentered time domain requirements.

    Parameters
    ----------
    requirements : list of double
        List containing the following time domain requirements: 
            [w_n, zeta, t_s(2%), t_r, t_p, w_d, sigma]

    Returns
    -------
    wn : double
        Calculated w_n value
    zeta : double
        Calculated zeta value
    ts : double
        Calculated 2% t_s value
    tr : double
        Calculated t_r value
    tp : double
        Calculated t_p value
    wd : double
        Calculated w_d value
    sigma : double
        Calculated sigma value

    """
    #set individual requirements from array
    wn=requirements[0]
    zeta=requirements[1]
    ts=requirements[2]
    tr=requirements[3]
    tp=requirements[4]
    wd=requirements[5]
    sigma=requirements[6]
        
    #calculate missing values
    if  (not (ts == 0)) and (sigma == 0):
        sigma = 4/ts    
        
    if  (not (tp == 0)) and (wd == 0):
        wd = np.pi/tp
        
    if (wn == 0):
        if not(sigma == 0):
            wn = sigma/zeta
        
    if (zeta == 0):
        if not(sigma == 0):
            zeta = sigma/wn
            
    if (not(wn == 0)) and (not(zeta == 0)):
        sigma = zeta*wn
        wd = wn*np.sqrt(1-np.square(zeta))
        ts = 4/sigma
        tp = np.pi/wd
        tr = 1.8/wn
        
    return wn, zeta, ts, tr, tp, wd, sigma

def readRequirements(entries):
    """
    Read parameter values from entry fields.

    Parameters
    ----------
    entries : list of ttk.Entry
        List containing all the requirement entry fields

    Returns
    -------
    wn : double
        Read w_n value
    zeta : double
        Read zeta value
    ts : double
        Read 2% t_s value
    tr : double
        Read t_r value
    tp : double
        Read t_p value
    wd : double
        Read w_d value
    sigma : double
        Read sigma value

    """
    #set individual entries from array
    e_wn = entries[0]
    e_zeta = entries[1]
    e_ts = entries[2]
    e_tr = entries[3]
    e_tp = entries[4]
    e_wd = entries[5]
    e_sigma  = entries[6]   
    
    #set initial values (unentered values can't be blank)
    wn=0
    zeta=0
    ts=0
    tr=0
    tp=0
    wd=0
    sigma=0
    
    #read entry values
    if e_tr.get():
        tr = float(e_tr.get()) 
    if e_wn.get():
        wn = float(e_wn.get()) 
    if e_zeta.get():
        zeta = float(e_zeta.get())   
    if e_ts.get():
        ts = float(e_ts.get())
    if e_tp.get():
        tp = float(e_tp.get())
    if e_wd.get():
        wd = float(e_wd.get()) 
    if e_sigma.get():
        sigma = float(e_sigma.get())
        
    return wn, zeta, ts, tr, tp, wd, sigma 

def writeRequirements(requirements, entries):
    """
    Writes the given requirements to the entry fields

    Parameters
    ----------
    requirements : list of double
        List containing the following time domain requirements: 
            [w_n, zeta, t_s(2%), t_r, t_p, w_d, sigma]           
    entries : list of ttk.Entry
        List containing all the requirement entry fields

    Returns
    -------
    None.

    """
    #set individual entries from array
    e_wn = entries[0]
    e_zeta = entries[1]
    e_ts = entries[2]
    e_tr = entries[3]
    e_tp = entries[4]
    e_wd = entries[5]
    e_sigma  = entries[6] 
    
    #set individual requirements from array
    wn=requirements[0]
    zeta=requirements[1]
    ts=requirements[2]
    tr=requirements[3]
    tp=requirements[4]
    wd=requirements[5]
    sigma=requirements[6]    
    
    #write values to entries
    e_wn.insert(0, wn)
    e_zeta.insert(0, zeta)
    e_ts.insert(0, ts)
    e_tr.insert(0, tr)
    e_tp.insert(0, tp)
    e_wd.insert(0, wd)
    e_sigma.insert(0, sigma)
    

def clearRequirements(entries):
    """
    Clears the entrys and sets the value_exchange requirements to zero.

    Parameters
    ----------
    entries : list of ttk.Entry
        List containing all the requirement entry fields
        
    Returns
    -------
    None.

    """
    #loops through the entries and clears them
    for i in range(0, len(entries)):
        entries[i].delete(0, tk.END)
        
    #set the value_exchange requirements to zero
    ve.valueExchange.setRequirements(0, 0)
    
def processRequirements(entries):
    """
    Calculate and display the time domain values.
    
    Calls readRequirements, calcRequirements and writeRequirements to read, 
    calculate and display the time domain requirements. Also sets the 
    value_exchange requirements.

    Parameters
    ----------
    entries : list of ttk.Entry
        List containing all the requirement entry fields

    Returns
    -------
    None.

    """
    #calls other functions to read, alculate and write the requirements
    requirements = readRequirements(entries)
    requirements = calcRequirements(requirements)
    writeRequirements(requirements, entries)
    
    #set the value_exchange requirements
    ve.valueExchange.setRequirements(requirements[6], requirements[5])

def setupRequirements(frame): 
    """
    Initialises the requirements GUI.
    
    This is the only function that needs to be called to use the module. 
    It initialises the GUI and sets the button commands to calculate or clear
    the time domain requirements.

    Parameters
    ----------
    frame_in : ttk.Frame
        The frame the GUI should be built in

    Returns
    -------
    None.

    """
    #setup the labels
    l_wn = ttk.Label(frame, text = "w_n")
    l_zeta = ttk.Label(frame, text = "zeta")
    l_ts = ttk.Label(frame, text = "t_s (2%)")
    l_tr = ttk.Label(frame, text = "t_r")
    l_tp = ttk.Label(frame, text = "t_p")
    l_wd = ttk.Label(frame, text = "w_d")
    l_sigma = ttk.Label(frame, text = "sigma")
    
    l_wn.grid(row = 0, column = 0, pady = 2)
    l_zeta.grid(row = 1, column = 0, pady = 2)
    l_ts.grid(row = 2, column = 0, pady = 2)
    l_tr.grid(row = 3, column = 0, pady = 2)
    l_tp.grid(row = 4, column = 0, pady = 2)
    l_wd.grid(row = 5, column = 0, pady = 2)
    l_sigma.grid(row = 6, column = 0, pady = 2)

    #setup the entries
    e_wn = ttk.Entry(frame)
    e_zeta = ttk.Entry(frame)
    e_ts = ttk.Entry(frame)
    e_tr = ttk.Entry(frame)
    e_tp = ttk.Entry(frame)
    e_wd = ttk.Entry(frame)
    e_sigma = ttk.Entry(frame)

    e_wn.grid(row = 0, column = 1, pady = 2)
    e_zeta.grid(row = 1, column = 1, pady = 2)
    e_ts.grid(row = 2, column = 1, pady = 2)
    e_tr.grid(row = 3, column = 1, pady = 2)
    e_tp.grid(row = 4, column = 1, pady = 2)
    e_wd.grid(row = 5, column = 1, pady = 2)
    e_sigma.grid(row = 6, column = 1, pady = 2)
    
    entries = [e_wn, e_zeta, e_ts, e_tr, e_tp, e_wd, e_sigma]
    
    #button setup
    b_calculate_req = ttk.Button(frame, text = "calculate", command =lambda: processRequirements(entries))
    b_clear_req = ttk.Button(frame, text = "clear", command=lambda: clearRequirements(entries))

    b_calculate_req.grid(row = 7, column = 1, pady = 5)
    b_clear_req.grid(row = 7, column = 0, pady = 5) 
