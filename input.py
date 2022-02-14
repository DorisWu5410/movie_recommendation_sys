# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pymysql
import urllib.request


headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
           'apiKey':'22f0aa365f634230b87894f7d5858fd5'}

datapath = {'links': 'http://doriswu.georgetown.domains/movie/links.csv', 
            'movies':'http://doriswu.georgetown.domains/movie/movies.csv',
            'ratings':'http://doriswu.georgetown.domains/movie/ratings.csv',
            'tags':'http://doriswu.georgetown.domains/movie/tags.csv',
            'simi_movie_svd':'http://doriswu.georgetown.domains/movie/simi_movie_svd.csv',
            'recomd_result_svd':'http://doriswu.georgetown.domains/movie/recomd_result_svd.csv',
            'simi_movie_als':'http://doriswu.georgetown.domains/movie/simi_movie_als.csv',
            'recomd_result_als':'http://doriswu.georgetown.domains/movie/recomd_result_als.csv',
            'online_recomd':'http://doriswu.georgetown.domains/movie/online_recomd.csv'}




def DfToSql(table, content):
    try:
        conn = pymysql.connect(host='localhost',
                             user='root',
                             password='Westlife890@',
                             database='movie_recomd')
        cur = conn.cursor()
        
        # create table
        cur.execute("drop table if exists " + table + ';')
        colname = str(content[0]).split(",")
        colname[0] = colname[0].strip("b'")
        colname[len(colname)-1]=colname[len(colname)-1].strip("\\r\\n'")
        for i in range(0,len(colname)):
            colname[i] = colname[i].strip('"')
        query_create = "CREATE TABLE " + table +'('+ " TEXT,".join(colname) + " TEXT);"      
        cur.execute(query_create)
        
        for i in range(1,len(content)):
            line = str(content[i]).split(",")
            if len(line) >= len(colname):
                line = line[0:len(colname)]
                line[0] = line[0].strip("b'")
                line[len(line)-1] = line[len(line)-1].strip("\\r\\n'")
                for j in range(0,len(line)):
                    line[j] = line[j].strip('"')
                query_insert = "INSERT INTO " + table + ' VALUES (" ' + '" , "'.join(line) + '");'
                cur.execute(query_insert)
        conn.commit()
        cur.close()
    except ConnectionError as e:
        print(e)





def getdata(table):
    url = datapath[table]
    req = urllib.request.Request(url = url , headers = headers)    
    response = urllib.request.urlopen(req)
    content =response.readlines()
    DfToSql(table,content)
    #return(content)

getdata('links')
getdata('movies')
getdata('ratings')
getdata('tags')
getdata('simi_movie_svd')
getdata('recomd_result_svd')
getdata('simi_movie_als')
getdata('recomd_result_als')
getdata('online_recomd')

# create movie average rated table
def get_avg_rate():
    conn = pymysql.connect(host='localhost',
                         user='root',
                         password='Westlife890@',
                         database='movie_recomd')
    cur = conn.cursor()
    query = 'create table movie_avg_rating select movieId, avg(rating) as score, count(*) as times from ratings group by movieId;'
    cur.execute(query)
    conn.commit() 
    
#get_avg_rate()    
    
    
    
    


