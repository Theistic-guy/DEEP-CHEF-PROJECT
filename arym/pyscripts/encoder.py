from recipe_utils import feature_encoding,create_CNN,path_encoding_names,path_encodings
import numpy as np
import pickle
from scipy.spatial.distance import cosine

with open(path_encodings,"rb") as f:
    encodings = pickle.load(f)
with open(path_encoding_names,"rb") as f:
    encodings_names = pickle.load(f)

def input_recipe(img_path):
    img_enc = feature_encoding(create_CNN(),img_path)
    img_enc = np.ravel(img_enc)
    similarities = []
    for i in encodings:
        i = np.ravel(i)
        cos = cosine(i,img_enc)
        similarities.append(cos)
    zipped_similarities = sorted(zip(similarities,encodings_names))
    # print(type(zipped_similarities))
    # print(zipped_similarities[:4])
    # print(len(zipped_similarities))
    selected_recipes = []
    selected_names = []
    for j in range(0,200):
        index = int(zipped_similarities[j][1].split("->")[0])
        name = zipped_similarities[j][1].split("->")[1]
        if index not in selected_recipes and name not in selected_names:
            print(index ,name)
            selected_recipes.append(index)
            selected_names.append(name)
            if len(selected_recipes) ==5:
                break
img_path = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images\train\9_Palak Paneer\1_Palak Paneer.jpg"
input_recipe(img_path)
