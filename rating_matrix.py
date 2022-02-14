#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 21:38:27 2022

@author: jiahuiwu
"""
import pymysql
import pandas as pd


conn = pymysql.connect(host='localhost',
                     user='root',
                     password='Westlife890@',
                     database='movie_recomd')
cur = conn.cursor()

query = 'select userId, movieId, rating from ratings'
cur.execute(query)
content = cur.fetchall()

user_rate_dict = {}
for i in range(1, len(content)):
    user = eval(content[i][0])
    movie = eval(content[i][1])
    rate = eval(content[i][2])
    if user in user_rate_dict:
        user_rate_dict[user][movie] = rate
    else:
        user_rate_dict[user] = {movie:rate}
        
user_movie_df = pd.DataFrame(user_rate_dict).T
user_movie_Fill0 = user_movie_df.fillna(0)



ratings = {}
ratings['userId'] = [eval(content[i][0]) for i in range(1,len(content))]
ratings['movieId'] = [eval(content[i][1]) for i in range(1,len(content))]
ratings['rating'] = [eval(content[i][2]) for i in range(1,len(content))]
ratings = pd.DataFrame(ratings)










# from surprise import SVD
# from surprise import Dataset, Reader
# from surprise.model_selection import cross_validate, train_test_split

# reader = Reader(rating_scale = (1,5))
# rating_matrix = Dataset.load_from_df(ratings, reader)
# trainset, testset = train_test_split(rating_matrix, test_size=0.2)

# svd_model = SVD(n_factors=100)
# svd_model.fit(trainset)


# svd_model.test(testset)

# svd_model.predict(1, 3)

