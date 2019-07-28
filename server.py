from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import json

from tensorflow.compat.v1.keras.models import load_model
from mtcnn.mtcnn import MTCNN
from shutil import copyfile
import Facenet_compare

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
parser.add_argument('image_path', type=str)
parser.add_argument('notes', type=str)

# Todo
# add photo to an existing person givin its id and list
class addPhoto(Resource):
    def post(self, person_id, List):
        args = parser.parse_args()
        people[List][person_id]['photo_count'] = people[List][person_id]['photo_count'] + 1
        
        #copy image, get vector, save vector
        new_image_path = List+'/'+str(person_id)+'_'+str(people[List][person_id]['photo_count']-1)
        copyfile(args['image_path'], new_image_path)
        vector = Facenet_compare.crop_face(new_image_path,faceDetection, facenet_model)
        Facenet_compare.vector_to_csv(vector,new_image_path)

        with open(filename, 'w') as f:
            json.dump(people, f)

        return person_id


# lets you POST to add new person given its list
class Addperson(Resource):
    def post(self, List):
        #parse arguments and add the info to json file 
        args = parser.parse_args()
        person_id = int(max(people[List].keys())) + 1
        people[List][person_id] = {'name': args['name'],'birth_year': args['birth_year'],
        'lost_found_date': args['lost_found_date'],
        'sketch': args['sketch'],'found_lost_place': args['found_lost_place'],
        'contact_number': args['contact_number'],'gender': args['gender'],
        'notes': args['notes'],'photo_count':1 }
        #copy image, get vector, save vector
        new_image_path = List+'/'+str(person_id)+'_'+str(people[List][person_id]['photo_count']-1)
        copyfile(args['image_path'], new_image_path)
        vector = Facenet_compare.crop_face(new_image_path,faceDetection, facenet_model)
        Facenet_compare.vector_to_csv(vector,new_image_path)

        with open(filename, 'w') as f:
            json.dump(people, f)

        return people[List][person_id], 201

class get_similar_people(Resource):
    def post(self, person_id, List):
        List_to_search = 'lost'
        if List=='lost':
            List_to_search = 'found'

        filtered_list = Facenet_compare.filter_list(people,List_to_search,people[List][person_id])
        result = [None]*(len(filtered_list)*people[List][person_id]['photo_count'])

        for i in range (people[List][person_id]['photo_count']):
            image_path = List+'/'+str(person_id)+'_'+str(i)
            sorted_distances = Facenet_compare.compare_all_filtered(image_path,filtered_list)
            result[i::people[List][person_id]['photo_count']] = sorted_distances

        # Raymond Hettinger
        # https://twitter.com/raymondh/status/944125570534621185
        return list(dict.fromkeys(result))#list of pathes sorted & merged with no duplicates

##
## Actually setup the Api resource routing here
##
api.add_resource(Addperson, '/Addperson/<List>')
api.add_resource(addPhoto, '/addPhoto/<person_id>/<List>')
api.add_resource(get_similar_people, '/get_similar_people/<person_id>/<List>')

if __name__ == '__main__':
    faceDetection = MTCNN()
    facenet_model = load_model('../facenet_keras.h5')
    with open('sample.json', 'r') as f:
        people = json.load(f)
    app.run(debug=True)
