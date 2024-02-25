#!/usr/bin/env python
# coding: utf-8

# In[126]:

from django.db import connection
import pandas as pd
import numpy as np
import psycopg2


# Establishing the connection with database. 

# In[127]:

'''
dbname = 'EventSafari'
user = 'mytest'
password = '999999'
host = '127.0.0.1'
port = '5432'

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
'''
def load_event_data():
    # Replace these values with your PostgreSQL database connection details
    db_params = {
        'host': '127.0.0.1',
        'database': 'EventSafari',
        'user': 'mytest',
        'password': '999999',
        'port': '5432',
    }

    # Create a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    # Create a cursor object for executing SQL queries
    cursor = conn.cursor()

    # Query to fetch all data from the events table (adjust the table name accordingly)
    query = 'SELECT * FROM main_event'
    #query2 = 'SELECT * FROM main_category'
    cursor.execute(query)

    # Read the query result into a DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[col.name for col in cursor.description])

    # Close the database connection
    conn.close()

    return df


# Imported the dataset of event from the database.

# In[128]:


# Create a cursor object for executing SQL queries
#cursor = conn.cursor()



# Fetch data using the psycopg2 cursor
#query = 'SELECT * FROM main_event'
#cursor.execute(query)

# Read the result into a pandas DataFrame
#data = pd.DataFrame(cursor.fetchall(), columns=[col.name for col in cursor.description])
df = load_event_data() 
df_original = df 

# In[129]:


df.head()


# Checking if there is any null value in data.

# In[130]:


df.isnull().sum()


# Dropping the null value and reseting the index.

# In[131]:


df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)


# Checking for duplicate data.

# In[132]:


df.duplicated().sum()


# In[133]:


df.shape


# Converting the data into list format.

# In[134]:


df["event_description"] = df["event_description"].apply(lambda x:x.split())
df['venue']=df['venue'].apply(lambda x:x.split())




# In[135]:


df.head()


# In[136]:


df.sample(6)


# Creating the tag from those list.

# In[137]:


df['tag']=df['venue']+df["event_description"]
df


# Creating new dataframe.

# In[138]:


df = df[["event_id","title","image","venue","tag"]]
df


# Removing the " , " between the tags.

# In[139]:


#df['tag']=df['tag'].apply(lambda x:" ".join(x))

df.loc[:, 'tag'] = df['tag'].apply(lambda x: " ".join(x))


# In[140]:


df['tag'][0]


# In[141]:


#pip install nltk


# In[142]:


import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# Stemming the data to obtain the root form.

# In[143]:


def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)


# In[144]:


df['tag'].apply(stem)


# Text vectorization.

# Taking 5000 words from the tags concatenated from each events removing the words like a, the.

# In[147]:


#pip install scikit-learn


# In[148]:


import sklearn
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000 , stop_words="english")


# Converting numpy value into array.

# In[149]:


vectors = cv.fit_transform(df['tag']).toarray()


# In[150]:


vectors


# In[151]:


vectors.shape


# The 'cv' object contains the 5000 most frequently occurring vectors derived from the 'tag' column.

# In[152]:


cv.get_feature_names_out()


# In[153]:


len(cv.get_feature_names_out())


# In[154]:


from sklearn.metrics.pairwise import cosine_similarity


# Calculating cosine similarity between events.

# In[155]:


similarity = cosine_similarity(vectors)


# The event itself have 1 and other gives the correlation with each event.

# In[156]:


similarity 


# In[157]:


cosine_similarity(vectors).shape


# In[158]:


similarity [0]


# Sorting on basis of similarity(i.e cosine distance)

# In[159]:


sorted(similarity [0],reverse=True) [1:6]  


# In list format with index sorted acc to similarity not index.

# In[160]:


sorted(list(enumerate(similarity[0])),reverse=True , key=lambda x:x[1])[1:6]


# In[162]:

'''
def recommend(event):
    index=df[df['title']== event].index[0]
    event_list=sorted(list(enumerate(similarity[index])),reverse=True , key=lambda x:x[1])[1:6]
    
    for i in event_list:
        print(df.iloc[i[0]].title)
        
'''
def recommend(event, df):
    filtered_df = df[df['title'] == event]
    
    if not filtered_df.empty:
        index = filtered_df.index[0]
        event_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_events = [df.iloc[i[0]].title for i in event_list]
    else:
        # Handle the case where the event is not found in the DataFrame
        index = None
        recommended_events = []  # or any default value
    
    return recommended_events


# In[164]:


recommend('Comics at Cubbon',df)


# In[ ]:


#get_ipython().system('jupyter nbconvert --to script Recommendation_system.ipynb')


# In[ ]:
import pickle

# Save the trained model
'''
with open('recommendation_model.pkl', 'wb') as model_file:
    pickle.dump({
        'cv': cv,
        'similarity': similarity,
        'df': df
    }, model_file)
'''
pickle.dump(df_original,open('event_list.pkl','wb'))
#pickle.dump(similarity,open('similarity.pkl','wb')) 


# %%
