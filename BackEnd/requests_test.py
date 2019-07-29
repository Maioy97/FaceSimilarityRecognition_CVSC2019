import requests
import json
import base64

Person_id = 0
img_id='1_0'
List = 'found'
AddpersonURL = 'http://localhost:5021/Addperson/'+ List
addPhotoURL = 'http://localhost:5021/addPhoto/'+str(Person_id)+'/'+List
get_similar_peopleURL = 'http://localhost:5021/get_similar_people/'+str(Person_id)+'/'+List
get_infoURL = 'http://localhost:5021/get_info/'+ List+'/'+img_id

with open("C:/Users/Haya/Desktop/test/1.JPG", "rb") as imageFile:
    Img_str = base64.b64encode(imageFile.read())

data = {"name": "nameX",
        "birth_year":"2001" ,
        "lost_found_date":"22-6-2019",
        "sketch":0,
        "found_lost_place":"place",
        "contact_number":"01298459844",
        "gender":"M",
        "notes":"any Notes",
        "photo_count":"1",
        "image":Img_str,
        "image_ext":"jpg"}
data2 = {"image":Img_str,
        "image_ext":"jpg"}
print(requests.post(get_infoURL).text)

