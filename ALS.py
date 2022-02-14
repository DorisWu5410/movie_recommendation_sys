#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 16:12:12 2022

@author: jiahuiwu
"""

from rating_matrix import user_movie_Fill0
from rating_matrix import user_movie_df
import numpy as np
import pandas as pd
from operator import itemgetter
from math import isnan


def ALS_mat_factorize(mat, lambda_=0.005, max_iter=100, k=5, alpha=0.1):
    X = np.random.rand(mat.shape[0], k)
    Y = np.random.rand(mat.shape[1], k)
   
    YtY = Y.T.dot(Y) + lambda_ * np.eye(k)
    for user in mat.index.values:
        x = X[user-1]
        r = -YtY.dot(x)
        for item in mat.columns:
            item_idx = mat.columns.tolist().index(item)
            confidence = 1 + alpha * mat.iloc[user-1,item_idx]
            r += (confidence - (confidence -1) * Y[item_idx].dot(x) * Y[item_idx])
            
        p = r.copy()
        
        r_old = r.dot(r)
        if r_old < 0.00001:
            continue
        
        for _ in range(max_iter):
            Ap = YtY.dot(p)
            for item in mat.columns:
                item_idx = mat.columns.tolist().index(item)
                confidence = 1 + alpha * mat.iloc[user-1,item_idx]
                Ap += (confidence - 1) * Y[item_idx].dot(p) * Y[item_idx]
                
            alpha = r_old / p.dot(Ap)
            x += alpha * p
            r -= alpha * Ap
            r_new = r.dot(r)
            if r_new < 0.00001:
                break
            p = r + (r_new / r_old) * p
            r_old = r_new
            
        X[user-1] = x
        
    
    XtX = X.T.dot(X) + lambda_ * np.eye(k)
    for item in mat.columns:
        item_idx = mat.columns.tolist().index(item)
        y = Y[item_idx]
        r = -XtX.dot(y)
        for user in mat.index.values:
            confidence = 1 + alpha * mat.iloc[user-1,item_idx]
            r += (confidence - (confidence -1) * X[user-1].dot(y) * X[user-1])
            
        p = r.copy()
        
        r_old = r.dot(r)
        if r_old < 0.00001:
            continue
        
        for _ in range(max_iter):
            Ap = XtX.dot(p)
            for user in mat.index.values:
                confidence = 1 + alpha * mat.iloc[user-1,item_idx]
                Ap += (confidence - 1) * X[user-1].dot(p) * X[user-1]
                
            alpha = r_old / p.dot(Ap)
            y += alpha * p
            r -= alpha * Ap
            r_new = r.dot(r)
            if r_new < 0.00001:
                break
            p = r + (r_new / r_old) * p
            r_old = r_new
            
        Y[item_idx] = y
    return([X, Y])
    
        
        
def ALS(mat, lambda_=0.005, max_iter=100, k=5, alpha=0.1):  
    X = np.random.rand(mat.shape[0], k)
    Y = np.random.rand(mat.shape[1], k)
       
    YtY = Y.T.dot(Y)    
    XtX = X.T.dot(X)
            
    for i in range(max_iter):
        print(i)
        for user in mat.index.values:
            A = YtY + lambda_ * np.eye(k)
            b = np.zeros(k)
            for item in mat.columns:
                item_idx = mat.columns.tolist().index(item)
                factor = Y[item_idx]
                confidence = 1 + alpha * mat.iloc[user-1,item_idx]
                A += (confidence - 1) * np.outer(factor, factor)
                b += confidence * factor
            X[user-1] = np.linalg.solve(A, b)
        
        for item in mat.columns:
            A = XtX + lambda_ * np.eye(k)
            b = np.zeros(k)
            item_idx = mat.columns.tolist().index(item)
            for user in mat.index.values:
                factor = X[user-1]
                confidence = 1 + alpha * mat.iloc[user-1,item_idx]
                A += (confidence - 1) * np.outer(factor, factor)
                b += confidence * factor
            Y[item_idx] = np.linalg.solve(A,b)
        
        cost = 0
        pred_mat = np.dot(X,Y.T)
        cost += np.sum((mat - pred_mat * (mat!=0))**2)
        cost += lambda_ * (np.sum(X**2)+np.sum(Y**2))
    
        if cost < 0.001:
            break
    
    return([X, Y, cost])
            
factorization  = ALS_mat_factorize(user_movie_Fill0)

fact = ALS(user_movie_Fill0)

item_reduce_mat = factorization[1]
std_item_mat = ((item_reduce_mat.T - item_reduce_mat.mean(axis=1))/item_reduce_mat.std(axis=1))

up = std_item_mat.dot(std_item_mat.T)#numerator
down = (np.linalg.norm(std_item_mat,axis=1).reshape(-1,1)).dot(np.linalg.norm(std_item_mat,axis=1).reshape(1,-1)) #denominator
cosSim = (up/down + 1)/2 #adjust value to be within 0-1
np.fill_diagonal(cosSim, 0)




            
            
            
                
            