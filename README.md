# movie_recommendation_sys

• Offline recommendation for old user based on their previous rating records: dimension deduction with SVD and ALS algorithms, calculated and stored cosine similarity matrix of movies. Predicted score for unrated movie for each user. Selected the top 20 movies with highest predicted rating. 

• Online recommendation for old user with their newly rated movie taken into consideration: refresh predicted result with old similarity matrix of movie and new rating records.

• Cold-start of new users: initialize with top 50 highest average rated movies.
