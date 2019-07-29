from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import json
from PIL import Image
from tensorflow.compat.v1.keras.models import load_model
from mtcnn.mtcnn import MTCNN
from shutil import copyfile
import Facenet_compare
from PIL import ExifTags
import traceback
import sys
import os
import base64

app = Flask(__name__)
api = Api(app)

# info is a dictionary containing all information about the person including (name, birth date, lost/found date,
# sketch or not(T/F), found/lost place, contact number, M/F, any aditional notes free string)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('birth_year')
parser.add_argument('lost_found_date')
parser.add_argument('sketch',type=bool)
parser.add_argument('found_lost_place', type=str)
parser.add_argument('contact_number', type=str)
parser.add_argument('gender', type=str)
parser.add_argument('image', type=str)
parser.add_argument('image_ext', type=str)
parser.add_argument('notes', type=str)

# Todo
# add photo to an existing person givin its id and list
class addPhoto(Resource):
    def post(self, person_id, List):
        args = parser.parse_args()
        t=people[List]
        print(t)
        if int(person_id) in t:
            t1=t[int(person_id)]
            t1['photo_count'] = str(int(people[List][int(person_id)]['photo_count']) + 1)
            t[int(person_id)]=t1
            people[List]=t
            
            #copy image, get vector, save vector
            fh = open("temp."+args['image_ext'], "wb")
            fh.write(base64.b64decode(args['image']))
            fh.close()
            
            new_image_path = List+'/'+str(person_id)+'_'+str(int(people[List][int(person_id)]['photo_count']) - 1)+'.jpg'

            if args['image_ext'].lower() !='jpg':
                image = Image.open("temp."+args['image_ext']).convert('RGB')
                image.save(new_image_path , 'JPEG')
            else:
                os.rename("temp."+args['image_ext'],new_image_path)

            vector = Facenet_compare.crop_face(new_image_path,faceDetection, facenet_model)
            Facenet_compare.vector_to_csv(vector,new_image_path)

            with open('sample.json', 'w') as f:
                json.dump(people, f)

            return int(person_id)
        else:
            return "Id is wrong, please correct it"


# lets you POST to add new person given its list
class Addperson(Resource):
    def post(self, List):
        #parse arguments and add the info to json file 
        args = parser.parse_args()
        if people[List] =={}:
            person_id=0
        else:
            person_id = int(max(people[List].keys())) + 1
        print(people[List].keys())
        print(person_id)
        list = people[List]
        list[int(person_id)] = {'name': args['name'],'birth_year': args['birth_year'],
        'lost_found_date': args['lost_found_date'],
        'sketch': args['sketch'],'found_lost_place': args['found_lost_place'],
        'contact_number': args['contact_number'],'gender': args['gender'],
        'notes': args['notes'],'photo_count':1 }
        people[List]=list
        #copy image, get vector, save vector
        fh = open("temp."+args['image_ext'], "wb")
        fh.write(base64.b64decode(args['image']))
        fh.close()
        new_image_path = List+'/'+str(person_id)+'_'+str(people[List][person_id]['photo_count']-1)+'.jpg'

        if args['image_ext'].lower() !='jpg':
            image = Image.open("temp."+args['image_ext']).convert('RGB')
            image.save(new_image_path , 'JPEG')
        else:
            os.rename("temp."+args['image_ext'],new_image_path)

        vector = Facenet_compare.crop_face(new_image_path,faceDetection, facenet_model)
        Facenet_compare.vector_to_csv(vector,new_image_path)

        with open('sample.json', 'w') as f:
            json.dump(people, f)

        return person_id

class get_similar_people(Resource):
    def post(self, person_id, List):
        List_to_search = 'lost'
        if List=='lost':
            List_to_search = 'found'

        filtered_list = Facenet_compare.filter_list(people,List_to_search,people[List][int(person_id)])
        result = [None]*(len(filtered_list)*int(people[List][int(person_id)]['photo_count']))

        for i in range (int(people[List][int(person_id)]['photo_count'])):
            image_path = List+'/'+str(person_id)+'_'+str(i)
            sorted_distances = Facenet_compare.compare_all_filtered(image_path,filtered_list)
            #print(sorted_distances)
            result[i] = sorted_distances

        # Raymond Hettinger
        # https://twitter.com/raymondh/status/944125570534621185
        print('**************************')
        print(result)
        print('**************************')
        return list(dict.fromkeys([item for sublist in map(list, zip(*result)) for item in sublist]))#list of pathes sorted & merged with no duplicates

class get_info(Resource):
    def post(self, List, img_ingex):
        person_id = img_ingex.split('_')[0]
        ret = people[List][int(person_id)]
        with open(List+'/'+img_ingex+'.jpg', "rb") as imageFile:
            ret['image'] = str(base64.b64encode(imageFile.read()))
        ret['image_ext'] = 'jpg'
        print(ret)
        return ret


##
## Actually setup the Api resource routing here
##
api.add_resource(Addperson, '/Addperson/<List>')
api.add_resource(addPhoto, '/addPhoto/<person_id>/<List>')
api.add_resource(get_similar_people, '/get_similar_people/<person_id>/<List>')
api.add_resource(get_info, '/get_info/<List>/<img_ingex>')

if __name__ == '__main__':
    people = {'found':{},'lost':{}}
    try:
        with open('sample.json', 'r') as f:
            temp_dictionary = json.load(f)
            for k in temp_dictionary:
                for k1 in temp_dictionary[k]:
                    t = people[k]
                    t[int(k1)] = temp_dictionary[k][k1]
                    people[k] = t
        print(people)
    except:
        print('************************************************')
        print(traceback.print_exc())
        print('************************************************')
    faceDetection = MTCNN()
    facenet_model = load_model('facenet_keras.h5')
    app.run(host = "localhost",port=5021 ,debug=True)
