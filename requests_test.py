import requests
import json

Person_id = 3
List = 'found'
AddpersonURL = 'http://localhost:8000/Addperson/'+ List
addPhotoURL = 'http://localhost:8000/addPhoto/'+str(Person_id)+'/'+List
get_similar_peopleURL = 'http://localhost:8000/get_similar_people/'+str(Person_id)+'/'+List

data = {"name": "nameX",
        "birth_year":"2001" ,
        "lost_found_date":"22-6-2019",
        "sketch":0,
        "found_lost_place":"place",
        "contact_number":"01298459844",
        "gender":"M",
        "notes":"any Notes",
        "photo_count":"1",
        "image_path":"C:/Users/Haya/Desktop/test/1.JPG"}
data2 = {"image_path":"C:/Users/Haya/Desktop/test/1 (2).JPG"}
print(requests.post(AddpersonURL, data=data).text)
