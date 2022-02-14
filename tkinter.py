#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 00:07:58 2022

@author: jiahuiwu
"""

import tkinter as tk
window = tk.Tk()
w = tk.Label(window, text="Hello, world!")
w.mainloop()


def merge_dict(dict1,dict2):
    x = dict1.copy() 
    for i in list(dict2.keys()):
        x[i] = x.get(i, 0)
        x[i] += dict2[i]
    return(x)

def merge_all(dict_list, head, end):
    if head == end:
        return(dict_list[head])
    else:
        d1 = merge_all(dict_list, head, (head+end)//2)
        d2 = merge_all(dict_list, (head+end)//2+1, end)
        return(merge_dict(d1, d2))
    
test_dict_list = [{'a':1}, {'b':1}, {'a':1, 'b':1}, {'c':1, 'b':3}]    

merge_all(test_dict_list, 0, len(test_dict_list)-1)

merge_dict( {'a': 1, 'b':1}, {'c':1, 'b':3})
