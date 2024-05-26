import os
import numpy as np
import keras
from keras.preprocessing import image
from keras.applications import densenet
import pickle
from scipy.spatial.distance import cosine
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

cnn_model=densenet.DenseNet201(include_top= False ,weights='imagenet', input_shape=(256,256,3),pooling='avg',classes= 350) 

with open(r'C:\Users\aditi\OneDrive\Desktop\PROJECTS\DEEP-CHEF-PROJECT\aarush\encodings.txt','rb') as f:
    encodings_list=pickle.load(f,encoding='utf-8')
with open(r'C:\Users\aditi\OneDrive\Desktop\PROJECTS\DEEP-CHEF-PROJECT\aarush\enc_names.txt','rb') as f:
    encoding_name_list=pickle.load(f,encoding='utf-8')
    
def feature_encoding(img):
    img=image.load_img(img,target_size=(256,256))
    img=keras.utils.img_to_array(img)
    img=np.expand_dims(img,axis=0)
    encoded=densenet.preprocess_input(img)
    encoded=cnn_model.predict(encoded)
    print(len(encoded[0]))
    return encoded

def input_recipe(img):
    encoding=feature_encoding(img)
    encoding = np.ravel(encoding) 
    similarity_list=[]
    similar_recipes_list=[]
    for i in encodings_list:
        i=np.ravel(i)
        cos=cosine(i,encoding)
        similarity_list.append(1-cos)
    sorted_similarity_list=sorted(zip(similarity_list,encoding_name_list),reverse=True)
    l=sorted(similarity_list,reverse=True)
    print(l[0])
    
    top_similar=10
    for i in range(len(sorted_similarity_list)):
        similar_recipe=sorted_similarity_list[i][1]
        similar_recipes_list.append(similar_recipe)
        if len(similar_recipes_list) == top_similar:
            break
    return similar_recipes_list
    

#input_image_path="C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\downloaded_images\\test\\0_Chicken Tikka Masala\\9_Chicken Tikka Masala.jpg"
#input_recipe(input_image_path)
    
    

