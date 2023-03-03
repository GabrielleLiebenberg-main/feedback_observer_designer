# -*- coding: utf-8 -*-
"""
A module for entering and calculating desired closed loop poles.

The poles module initialises a GUI that has entry fields for sample time, 
s-poles and z-poles. The z-poles can be calculated from entered s-poles and 
sampling time or entered maunually and set.

REQUIRED MODULES:
    value_exchange
    
EXAMPLE:
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)

    tab_poles = ttk.Frame(tabControl)
    tabControl.add(tab_poles, text ='Closed-loop poles')    
    
    initValueExchange()
    setupPoles(tab_poles)

Created on Thu Mar  2 09:13:01 2023

@author: 22546723
"""

import numpy as np
import tkinter as tk					
from tkinter import ttk

import value_exchange as ve

def calcPoles(s_sigma, s_wd, T):
    """
    Calculates the z-poles from the s-poles and sample time

    Parameters
    ----------
    s_sigma : double
        S-poles sigma value
    s_wd : double
        S-poles w_d value
    T : double
        Sample time

    Returns
    -------
    z_sigma : double
        Calculated sigma value
    z_wd : double
        Calculated w_d value

    """
    #calculate z-poles
    z_sigma = np.exp(s_sigma*T) * np.cos(s_wd*T)
    z_wd = np.exp(s_sigma*T) * np.sin(s_wd*T)
    
    return z_sigma, z_wd

def readZPoles(z_entries, e_T):
    """
    Read the z-poles and sample time from the entry fields and sets the poles 
    in the value_exchange

    Parameters
    ----------
    z_entries : list of ttk.Entry
        List containing the z-pole entries [z_sigma, z_wd]
    e_T : ttk.Entry
        Sample time entry

    Returns
    -------
    None.

    """
    #read
    z_sigma = z_entries[0].get()
    z_wd = z_entries[1].get()
    T = e_T.get()
    
    #set poles in value_exchange
    ve.valueExchange.setPoles(z_sigma, z_wd, T)

def clearPoles(z_entries, T): 
    """
    Clear the z-pole entries and setthe value_exchange poles to zero

    Parameters
    ----------
    z_entries : list of ttk.Entry
        List containing the z-pole entries [z_sigma, z_wd]
    T : double
        Sample time

    Returns
    -------
    None.

    """
    #set entry field values
    z_entries[0].delete(0, tk.END)
    z_entries[1].delete(0, tk.END) 
    
    #set poles in value exchange
    ve.valueExchange.setPoles(0, 0, T)

def readPolesFromReq(s_entries):
    """
    Calculates the s-poles from the time domain requirements through the 
    value_exchange and displays them in the entry fields.

    Parameters
    ----------
    s_entries : list of ttk.Entry
        List containing the s-pole entries [s_sigma, s_wd]

    Returns
    -------
    None.

    """
    #get poles
    [s_sigma, s_wd] = ve.valueExchange.getRequirements()
    
    s_sigma = -s_sigma
    
    #display poles
    s_entries[0].insert(0, s_sigma)
    s_entries[1].insert(0, s_wd)
    
    
def readPoles(s_entries, e_T):
    """
    Read the s-pole and sample time values from the entry fields

    Parameters
    ----------
    s_entries : list of ttk.Entry
        List containing the s-pole entries [s_sigma, s_wd]
    e_T : ttk.Entry
        Sample time entry

    Returns
    -------
    s_sigma :double
        Read sigma value
    s_wd : double
        Read w_d value
    T : double
        Read sample time value

    """
    #read values
    s_sigma = float(s_entries[0].get())
    s_wd = float(s_entries[1].get())
    T = float(e_T.get())
    
    return s_sigma, s_wd, T

def processPoles(z_entries, s_entries, e_T):
    """
    Reads s-poles and sample time, calculates and displays z-poles. Also sets
    the value_exchange poles.

    Parameters
    ----------
    z_entries : list of ttk.Entry
        List containing the z-pole entries [z_sigma, z_wd]
    s_entries : list of ttk.Entry
        List containing the s-pole entries [s_sigma, s_wd]
    e_T : ttk.Entry[]
        Sample time entry

    Returns
    -------
    None.

    """
    #read s-poles and sample time
    [s_sigma, s_wd, T] = readPoles(s_entries, e_T)
    
    #clear z-pole entries
    clearPoles(z_entries, T)
    
    #calculate z-poles
    [z_sigma, z_wd] = calcPoles(s_sigma, s_wd, T)
    
    #display z-poles
    z_entries[0].insert(0, z_sigma)
    z_entries[1].insert(0, z_wd)    
    
    #set value_exchange poles
    ve.valueExchange.setPoles(z_sigma, z_wd, T)

def setupPoles(frame):
    """
    Initialises the poles GUI.
    
    This is the only function that needs to be called to use the module. 
    It initialises the GUI and sets the button commands to import, read and 
    calculate the poles.   

    Parameters
    ----------
    frame : ttk.Frame
        The frame the GUI should be built in

    Returns
    -------
    None.

    """
    #setup labels
    l_T = ttk.Label(frame, text = "T:")
    l_T_s = ttk.Label(frame, text = "s")
    l_T.grid(row = 0, column = 0, pady = 2)
    l_T_s.grid(row = 0, column = 2, pady = 2)

    l_s_poles = ttk.Label(frame, text = "s:")
    l_z_poles = ttk.Label(frame, text = "z:")
    l_s_poles.grid(row = 1, column = 0, pady = 2)
    l_z_poles.grid(row = 2, column = 0, pady = 2)    

    l_s_sign = ttk.Label(frame, text = "+/- j")
    l_z_sign = ttk.Label(frame, text = "+/- j")
    l_s_sign.grid(row = 1, column = 2, pady = 2)
    l_z_sign.grid(row = 2, column = 2, pady = 2)

    #setup entries
    e_T = ttk.Entry(frame)
    e_T.grid(row = 0, column = 1, pady = 2)

    e_s_sigma = ttk.Entry(frame)
    e_s_wd = ttk.Entry(frame)
    e_z_sigma = ttk.Entry(frame)
    e_z_wd = ttk.Entry(frame)

    e_s_sigma.grid(row = 1, column = 1, pady = 2)
    e_s_wd.grid(row = 1, column = 3, pady = 2)
    e_z_sigma.grid(row = 2, column = 1, pady = 2)
    e_z_wd.grid(row = 2, column = 3, pady = 2)
      

    s_entries = [e_s_sigma, e_s_wd]
    z_entries = [e_z_sigma, e_z_wd]
    
    #setup buttons
    b_poles_read = ttk.Button(frame, text = "Read z-poles", command=lambda: readZPoles(z_entries, e_T))
    b_poles_req = ttk.Button(frame, text = "Get poles from parameters", command=lambda: readPolesFromReq(s_entries))
    b_poles_calc = ttk.Button(frame, text = "Calculate z poles", command=lambda: processPoles(z_entries, s_entries, e_T))
    b_poles_read.grid(row = 3, column = 2, pady = 5)
    b_poles_req.grid(row = 3, column = 0, pady = 5)
    b_poles_calc.grid(row = 3, column = 1, pady = 5)
