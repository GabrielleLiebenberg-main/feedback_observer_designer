# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:25:25 2023

@author: 22546723
"""
import tkinter as tk					
from tkinter import ttk

#import value_exchange
from requirements import setupRequirements
from poles import setupPoles
#from value_exchange import initValueExchange
from model import setupModel
from results import setupResults


root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab_requirements = ttk.Frame(tabControl)
tab_poles = ttk.Frame(tabControl)
tab_model = ttk.Frame(tabControl)
tab_results = ttk.Frame(tabControl)

tabControl.add(tab_requirements, text ='Set desired parameters')
tabControl.add(tab_poles, text ='Closed-loop poles')
tabControl.add(tab_model, text ='Setup state space model')
tabControl.add(tab_results, text ='Observer and feedback controller')
tabControl.pack(expand = 1, fill ="both")

setupRequirements(tab_requirements)
setupPoles(tab_poles)
setupModel(tab_model)
setupResults(tab_results)

root.mainloop()
