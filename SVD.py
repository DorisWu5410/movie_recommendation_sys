#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 02:43:43 2022

@author: jiahuiwu
"""

from rating_matrix import user_movie_Fill0
from rating_matrix import user_movie_df
import numpy as np
import pandas as pd
from operator import itemgetter
from math import isnan

# apply SVD
U, sigma, Vt = np.linalg.svd(user_movie_Fill0)

#select implict feature that counts for over 0.9 info about the matrix
# subsum = 0
# all_sum = sum([i**2 for i in sigma])
# for k in range(len(sigma)):
#     subsum += sigma[k]**2
#     if subsum/all_sum >= 0.9:
#         print(k)
#         break

#dimension reduction on user 
reduced_mat = (U[:,:5].dot(np.eye(5)*sigma[:5])).T.dot(np.matrix(user_movie_Fill0))

#normalization
std_mat = ((reduced_mat.T - reduced_mat.T.mean(axis=0))/reduced_mat.T.std(axis=0)).T


#compute cos similarity matrix
up = std_mat.T.dot(std_mat)#numerator
down = (np.linalg.norm(std_mat,axis=0).reshape(-1,1)).dot(np.linalg.norm(std_mat,axis=0).reshape(1,-1)) #denominator
cosSim = (up/down + 1)/2 #adjust value to be within 0-1
np.fill_diagonal(cosSim, 0)
cosSim = pd.DataFrame(cosSim)
# cosSim[cosSim<0.8] = 0
# for i in range(cosSim.shape[0]):
#     similist = np.array(cosSim[i,:][cosSim[i,:]>0.88])[0]
#     if len(similist)>50:
#         idx = np.array(np.argsort(cosSim[i,:])).tolist()[0][::-1]
#         idx = idx[50:]
#         print(len(idx))
#         cosSim[idx] = 0
        

#delete diagnaol similarity


#predict rate based on SVD similarity
# def pred_rate(user, movie):
#     rated_movie_idx = user_movie_Fill0.iloc[user, :] > 0
#     movie_idx = list(user_movie_Fill0.columns).index(movie)
#     Simtotal = sum(np.array(cosSim[movie_idx])[0][rated_movie_idx]) 
#     rateSimtotal = np.inner(user_movie_Fill0.iloc[user,:], np.array(cosSim[movie_idx])[0])
#     if Simtotal == 0:
#         return(0)
#     else:
#         return(rateSimtotal/Simtotal)
    
    
    
#given user, recommend movie from his unrated movie list by predicting his rating
def recommend(user_idx):
    #find unrate movies and thir index
    unrate = np.isnan(user_movie_df.values[user_idx,:])
    unrated_movie = user_movie_Fill0.columns[unrate]
    rated = ~unrate   
    
    #predict rate
    pred_list = np.array((cosSim[unrate,:][:,rated]).dot(user_movie_df.values[user_idx,:][rated]))[0] / np.array(np.sum(cosSim[unrate,:][:,rated],axis=1)).T[0]
    pred_dict = dict(zip(unrated_movie, pred_list))
    pred_dict = {k:v for k, v in pred_dict.items() if not isnan(v)}
    #get top50 rated 
    recomd_dict = dict(sorted(pred_dict.items(), key=itemgetter(1), reverse=True)[:50])
    return(recomd_dict)
    
    



recommend_result = {}
for user in user_movie_Fill0.index.values.tolist():
    recomd_dict = recommend(user-1)
    
    recommend_result['user'] = recommend_result.get('user',[])
    recommend_result['user'].extend([user]*len(recomd_dict))
    
    recommend_result['movie'] = recommend_result.get('movie',[])
    recommend_result['movie'].extend(recomd_dict.keys())
    
    recommend_result['pred_rate'] = recommend_result.get('pred_rate',[])
    recommend_result['pred_rate'].extend(recomd_dict.values())
   
# pd.DataFrame(recommend_result).to_csv('recom_result_svd.csv')
    
    




