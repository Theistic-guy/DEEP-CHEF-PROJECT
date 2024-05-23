import os
from keras._tf_keras.keras.preprocessing import image
from keras.src.applications import densenet
import numpy as np
import pickle
import re
from scipy.spatial.distance import cosine
from PIL import Image
import keras
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

model = densenet.DenseNet201(include_top=False, weights='imagenet', input_shape=(256, 256, 3),pooling='avg',classes= 358)

#add paths to encoding and encoding namees
with open("path to encoding","rb") as f:
    enc_list=pickle.load(f)
with open("path to endoing name","rb") as f:
    names_list=pickle.load(f)      
    
def getencodings(path):    
    _img = image.load_img(path, target_size=(256, 256))
    _img = keras.utils.img_to_array(_img)
    _img = np.expand_dims(_img, axis=0)
    _enc = densenet.preprocess_input(_img)
    _enc = model.predict(_enc)
    return _enc

def getrecipes(img):
    encoding=getencodings(img)
    encoding = np.ravel(encoding) 
    similarity_list=[]
    similar_recipes_list=[]
    for i in enc_list:
        i=np.ravel(i)
        cos=cosine(i,encoding)
        similarity_list.append(1-cos)
    sorted_similarity_list=sorted(zip(similarity_list,names_list),reverse=True)
    l=sorted(similarity_list,reverse=True)
    
    top_similar=10
    for i in range(len(sorted_similarity_list)):
        similar_recipe=sorted_similarity_list[i][1]
        similar_recipes_list.append(similar_recipe)
        if len(similar_recipes_list) == top_similar:
            break
    return similar_recipes_list
