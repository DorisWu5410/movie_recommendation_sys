#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 23:28:06 2022

@author: jiahuiwu
"""
import pymysql
import pandas as pd
import numpy as np
from SVD import cosSim
conn = pymysql.connect(host='localhost',
                     user='root',
                     password='Westlife890@',
                     database='movie_recomd')

# select top predicted rated movie from svd and als for each user
def get_recomd_conbine():
    query = 'select * from recomd_result_svd;'
    cur = conn.cursor()
    cur.execute(query)
    content = cur.fetchall()
    svd_recomd = pd.DataFrame(content)
    svd_recomd = svd_recomd.set_axis(['user', 'movie', 'pred_rate'], axis=1, inplace = False)
    
    query = 'select * from recomd_result_als;'
    cur.execute(query)
    content = cur.fetchall()
    als_recomd = pd.DataFrame(content)
    als_recomd = als_recomd.set_axis(['user', 'movie', 'pred_rate'], axis = 1, inplace= False)
    
    #merge two data  
    combine = pd.concat([svd_recomd, als_recomd])
    combine = combine.sort_values(by = ['user','pred_rate'], ascending = [True, False])
    #delete duplicated recomend movie for a user
    combine = combine.loc[~combine.duplicated(subset = ['user', 'movie']), :]
    
    #pick top 50 from combine for each user
    userID = svd_recomd.user.unique()
    combine_recomd = pd.DataFrame()
    for user in userID:
        recomd = combine.loc[combine.user == user, :].sort_values(by = 'pred_rate', ascending = False)[:50]
        combine_recomd = pd.concat([combine_recomd, recomd])
    online_recomd = pd.DataFrame(combine_recomd)
    online_recomd.to_csv('online_recomd.csv', index=False)
    return(online_recomd)    


#when old user rate a new movie, upated online_recomd result
cur = conn.cursor()
query = 'select movieId from ratings'
cur.execute(query)
movie_list = list(set([int(s[0]) for s in cur.fetchall()]))
cosSim.index = movie_list
cosSim.columns = movie_list 


def update(user, new_rate_movie_id):
    #fetch previous recommend result
    cur = conn.cursor()
    query = 'select movie from online_recomd where user = {}'.format(user)
    cur.execute(query)
    old_recomd = [s[0] for s in cur.fetchall()]
    old_recomd = list(map(int, old_recomd))
    
    #fetch similar movie to the new_rated movie
    query = 'select simiID from simi_movie_svd where movieID = {}'.format(new_rate_movie_id)
    cur.execute(query)
    simi_list = [int(s[0]) for s in cur.fetchall()]
    simi_list = list(map(int, simi_list))
    
    #fetch previous rating results
    query = 'select * from ratings where userId = {}'.format(user)
    cur.execute(query)
    old_rate = cur.fetchall()
    old_rate = np.array(pd.DataFrame([eval(s[0]), int(s[1]), eval(s[2]), eval(s[3])] for s in old_rate))
    
    #union previous rating movies with movies similar to the new rated movie, discard previously rated movies
    mix = set(old_recomd) | set(simi_list)
    mix = np.array(list(set(mix) - set(old_rate[:,1])))
    
    #find 10 most recently rated movie, refresh predicted rate of movie in the mix list with similarity to these 10 movies
    recent = old_rate[np.argsort(old_rate[:,-1])[::-1][:10]]
    
    
    pred_rate1 = cosSim.loc[mix, recent[:,1]].values.dot(recent[:,2]) / np.sum(cosSim.loc[mix, recent[:,1]].values, axis = 1)
    
    #adjustment with low rated movie
    low_rate_idx = recent[:,2] < 3
    high_rate_idx = recent[:,2] >= 3.5
    pred_rate_high = np.log(np.sum((cosSim.loc[mix, recent[:, 1]].values > 0.8) * high_rate_idx, axis=1) + 1)
    pred_rate_low = np.log(np.sum((cosSim.loc[mix, recent[:, 1]].values > 0.8) * low_rate_idx, axis=1) + 1)
    
    pred_rate = pred_rate1 + pred_rate_high - pred_rate_low
    
    #select new recomd movie 
    new_recomd = mix[np.argsort(pred_rate)[::-1][:50]]
    user_id = [user]*len(new_recomd)
    new_recomd_rate = ','.join([*zip(user_id, new_recomd)])
    
    query = 'delete from online_recomd where user = {}'.format(user)
    cur.execute(query)
    
    query = 'insert into online_recomd values {}'.format(new_recomd_rate)
    cur.execute(query)
    
    return(pred_rate_low)



#when new user create an account, insert a new line to online_recomd, initiated with top 50 movies
def insert_new(user):
    cur = conn.cursor()
    query = 'insert into online_recomd select {}, movieId order by times desc limit 50;'.format(user)
    cur.execute(query)
    conn.commit()
    
    
    





    


    