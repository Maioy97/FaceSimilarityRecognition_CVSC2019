from tensorflow.compat.v1.keras.models import load_model
from mtcnn.mtcnn import MTCNN
from tensorflow.compat.v1.keras.preprocessing.image import img_to_array
from io import StringIO
import cv2
import numpy as np
import csv
import os
from operator import itemgetter
from matplotlib import pyplot as plt
from shutil import copyfile

from datetime import date
from datetime import datetime


def filter_list(people,List,person_info):
    filtered_list = []
    threshold = 5
    today = date.today()
    age = today.years-person_info['birth_year']
    if age > 20:
        threshold = 15
    # Iterate over all the items in dictionary
    for (key, value) in people[List].items():
        # Check if item satisfies the given condition then add to new dict
        if value['gender'] == person_info['gender']:
            difference = abs(value['birth_year'] - person_info['birth_year'])
            if difference < threshold:
                filtered_list.append([List+'/'+str(key)+'_'+str(i)] for i in range(people[List][key]['photo_count']))
    return filtered_list

def vector_to_csv(vector, imagename, filename="../vectors.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        fieldnames = ['imagename', 'vector']
        writer = csv.writer(file)  # DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writerow(fieldnames)

        # writer.writerow({'id':'id', 'label':'label'})
        row = [str(imagename), vector]
        writer.writerow(row)  # ({'id': line, 'label': aftersep})


def get_embedding_dic(filename="../vectors.csv"):  # reads the csv into dictionary (embeddings_dictionary)
    try:
        with open(filename) as f:
            next(f)  # Skip the header
            reader = csv.reader(f, skipinitialspace=True)
            result = dict(reader)
            return result
    except:
        return {}


def embed_croped_face(model, cropped):
    img = cv2.resize(cropped, (160, 160))
    #plt.imshow(img)
    #plt.xticks([]), plt.yticks([])
    #plt.show()
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    vector = model.predict(img)
    return vector


def crop_face(img, faceDetection, model):
    data = cv2.imread(img)
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    # detect faces
    boxes = faceDetection.detect_faces(data)
    if len(boxes) > 0:
        # crop face
        x, y, width, height = boxes[0]['box']
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        cropped_img = data[y:y + height, x:x + width]

        return embed_croped_face(model, cropped_img)
    else:
        # cv2_imshow(data)
        data = np.transpose(data, (1, 0, 2))
        # cv2_imshow(data)
        boxes = faceDetection.detect_faces(data)
        # crop face
        if len(boxes) == 0:
            print('no face found in ' + img)
            return
        x, y, width, height = boxes[0]['box']
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        cropped_img = data[y:y + height, x:x + width]

        return embed_croped_face(model, cropped_img)


def embed_all_faces(image_directory, faceDetection, model, embedding_dictionary):
    # load models
    # faceDetection = MTCNN()
    # model = load_model('facenet_keras.h5')
    # embedding_dictionary = get_embedding_dic()

    for img_name in (os.listdir(image_directory)):
        img = os.path.join(image_directory, img_name)
        if img in embedding_dictionary:
            continue
        vector = crop_face(img, faceDetection, model)
        vector_to_csv(vector, img)


def l2_normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))


def findEuclideanDistance(source_representation, test_representation):
    return np.linalg.norm(source_representation - test_representation)


def compare(img1_representation, img2_representation):
    img1_representation = l2_normalize(img1_representation)
    img2_representation = l2_normalize(img2_representation)

    euclidean_distance = findEuclideanDistance(img1_representation, img2_representation)
    return euclidean_distance

def compare_all_filtered(image_to_compare, filtered_List):

    embedding_dictionary = get_embedding_dic()

    s = StringIO(embedding_dictionary[image_to_compare][2:len(embedding_dictionary[image_to_compare]) - 2].replace('\n', ' '))
    image_to_compare_vector = np.genfromtxt(s, skip_header=False)

    dict_imgname_distance = {}
    for img in filtered_List:
        if not img in embedding_dictionary:
            continue
        s = StringIO(embedding_dictionary[img][2:len(embedding_dictionary[img]) - 2].replace('\n', ' '))
        current_vector = np.genfromtxt(s, skip_header=False)
        dict_imgname_distance[img] = compare(image_to_compare_vector, current_vector)
    return sorted(dict_imgname_distance, key=dict_imgname_distance.get)  #  image names sorted by distance


# info is a dictionary containing all information about the person including (name, birth date, lost/found date,
# sketch or not(T/F), found/lost place, contact number, M/F, any aditional notes free string)

# if a sketch was provided its index will be 0 (as it will be the first to add) (image names saved will be Id_imageIndex)
# list_name : string ('found' or 'lost')
