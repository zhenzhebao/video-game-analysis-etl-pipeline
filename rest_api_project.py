import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import time

apikey=apikey
parent_platforms_PC=None
store_Steam=None
parent_platforms_base_url='https://api.rawg.io/api/platforms/lists/parents'
store_base_url='https://api.rawg.io/api/stores'
game_base_url='https://api.rawg.io/api/games'

"""### Retriece the value for Parent platforms (PC)"""

params={'page':1,'key':apikey}
parent_platforms_raw_response=requests.get(parent_platforms_base_url,params=params)

parent_platforms_response=parent_platforms_raw_response.json()

for item in parent_platforms_response['results']:
  if item['name']=='PC':
    #print(item)
    #print(item['name'])
    parent_platforms_PC=item['id']
    break
if parent_platforms_PC is None:
  print('ID for PC platform is not available')

"""### Retriece the value for Parent platforms (PC) and Store (Steam)"""

params={'key':apikey,'page':1,'page_size':2}
store_raw_response=requests.get(store_base_url,params=params)
store_response=store_raw_response.json()

for item in store_response['results']:
  if item['name']=='Steam':
    #print(item)
    store_Steam=item['id']
    break
if store_Steam is None:
  print('ID for Steam Store is not available')

"""### Retrieve a list of games"""

params={'key':apikey,'page':1,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
        'dates':'2025-01-01,2025-12-31','page_size':1}
total_count=requests.get(game_base_url,params=params)
total_count=total_count.json()

return_data=[]
next_url=None

dates=['2025-01-01,2025-03-31','2025-04-01,2025-06-30','2025-07-01,2025-09-30','2025-10-01,2025-12-31']
for date in dates:
  params={'key':apikey,'page':1,'page_size':40,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
            'dates':date}
  list_of_games_raw_response=requests.get(game_base_url,params=params)

  list_of_games_response=list_of_games_raw_response.json()
  return_data.extend(list_of_games_response['results'])
  next_url=list_of_games_response['next']

  while next_url is not None:
    response=requests.get(next_url)
    response_dict=response.json()
    return_data.extend(response_dict['results'])
    next_url=response_dict['next']
    print(len(return_data))
    if len(return_data)<10000:
        time.sleep(1)
    else:
        time.sleep(2)

if total_count['count']==len(return_data):
  print('Data is complete')
else:
  print('Data is incomplete')

"""## Drop irrelevant columns"""

df=pd.DataFrame(return_data)
df.columns

skip_columns=['community_rating','slug','platforms', 'stores','tba','background_image','ratings_count','reviews_text_count',
              'added','metacritic','suggestions_count','score', 'clip','tags','esrb_rating','user_game', 'reviews_count',
              'saturated_color','dominant_color','short_screenshots','parent_platforms']

data=df.drop(columns=skip_columns)
data.head()

"""## Creating Game Table"""

game=data[['id','name','playtime','released','updated','rating','rating_top']]
game.to_csv('game_table.csv')
game

"""### Creating Game_added_Status Table"""

columns=[]
for item in return_data:
  if item['added_by_status'] is not None:
    for i in item['added_by_status'].keys():
      columns.append(i)
    break
  else:
    continue
print(columns)

for item in return_data:
  if item['added_by_status'] is not None:
    #print(item['added_by_status'])
    for i in item['added_by_status'].keys():
      #print(i)
      if i not in columns:
        print(item['added_by_status'].keys())
        columns.append(i)
print('done')

empty_value=[]
count=1
while count<=len(columns):
  empty_value.append(None)
  count=count+1
rows=[]

for item in return_data:
  row=[]
  if item['added_by_status'] is None:
    #print(item['id'])
    row.append(item['id'])
    row.extend(empty_value)
    rows.append(row)
  else:
    #print('+++++++++++++++++++++++++')
    #print(item['added_by_status'])
    row.append(item['id'])
    for i in columns:
     try:
      #print(i)
      #print(item['added_by_status'][i])
      row.append(item['added_by_status'][i])
     except KeyError:
      #print('No key')
      row.append(None)
    rows.append(row)

game_added_status_column=['id']
game_added_status_column.extend(columns)
print(game_added_status_column)
game_added_status=pd.DataFrame(rows,columns=game_added_status_column)

game_added_status.to_csv('game_added_status.csv')
game_added_status

"""### Creating Game rating Category Table"""

rating_category=[]
for item in return_data:
  if len(item['ratings'])>0:
   for i in item['ratings']:
    #print(i)
    #print(i['title'])
    if i['title'] not in rating_category:
      rating_category.append(i['title'])
    else:
      continue
print(rating_category)

rows=[]
empty_value={}
for i in rating_category:
  empty_value.update({i:None})

for item in return_data:
  if len(item['ratings'])==0:
    #print(item['id'])
     row=empty_value.copy()
     row.update({'id':item['id']})
     rows.append(row)
  else:
    row={}
    row.update({'id':item['id']})
    for i in item['ratings']:
      #print(i['title'],i['count'])
      row.update({i['title']:i['count']})
    for i in rating_category:
      if i not in row.keys():
        row.update({i:None})
    rows.append(row)

rating_category=pd.DataFrame(rows)
rating_category.to_csv('game_rating_category.csv')
rating_category

"""### Create Game Genres Table"""

genres=[]
for item in return_data:
  #print(item)
  if len(item['genres'])>0:
    for i in item['genres']:
      #print(i)
      #print(i['name'])
      if i['name'] not in genres:
        genres.append(i['name'])
      else:
        continue
  else:
    continue

print(genres)
rows=[]
empty_genres={}
for i in genres:
  empty_genres.update({i:None})

for item in return_data:
  if len(item['genres'])==0:
    row=empty_genres.copy()
    row.update({'id':item['id']})
    rows.append(row)
  else:
    row={}
    row.update({'id':item['id']})
    for i in (item['genres']):
      #print(i)
      row.update({i['name']:'Yes'})
    for i in genres:
      if i not in row.keys():
        row.update({i:None})
    rows.append(row)

game_genres=pd.DataFrame(rows)
game_genres.to_csv('game_genres.csv')
game_genres

"""### Retrieve detailed information for one game"""

params={'key':apikey,'page':1,'page_size':1,'parent_platforms':parent_platforms_PC,'stores':store_Steam,
        'dates':'2015-01-01,2025-12-31'}
game=requests.get('https://api.rawg.io/api/games/3439',params=params)

for i in game.json().keys():
  print(i)
  print(game.json()[i])