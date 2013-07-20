import json
'''
mongoimport --db movie_db --collection movies --type json --file movie_data_new.json --jsonArray}
'''
movie_dict = json.load(open('movie_data.json', 'r'))
list_of_json = []

for key in movie_dict:
    temp_dict = {'title' : key,
                 'rt_link' : movie_dict[key]['rt_link'],
                 'audience_score' : movie_dict[key]['audience_score'],
                 'genres' : movie_dict[key]['genres'],
                 'critics_score' : movie_dict[key]['critics_score'],
                 'actors' : movie_dict[key]['actors'],
                 'similar' : movie_dict[key]['similar'],
                 'id' : movie_dict[key]['id']
                }
    list_of_json.append(temp_dict)

out_file = open('movie_data_new.json', 'w')
out_file.write('[\n')
for x, obj in enumerate(list_of_json):
    sep = ','
    if x+1 == len(list_of_json):
        sep = ''
    line = json.dumps(obj) + sep + '\n'
    out_file.write(line)
out_file.write(']')
