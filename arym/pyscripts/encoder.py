from .recipe_utils import feature_encoding,create_CNN,fetch_encoding_names,fetch_encodings
import numpy as np
import pickle
from scipy.spatial.distance import cosine



def input_recipe(img_path,encodings,encoding_names):
    '''
    returns zipped recipe indexes with their names
    '''
    img_enc = feature_encoding(create_CNN(),img_path)
    img_enc = np.ravel(img_enc)
    similarities = []
    for i in encodings:
        i = np.ravel(i)
        cos = cosine(i,img_enc)
        similarities.append(cos)
    zipped_similarities = sorted(zip(similarities,encoding_names))
    selected_recipes = []
    selected_names = []

    # imp note: here we have chosen arbitrarily a big no 200
    # because we need 5 distinct recipes
    # assuming we have repeated each recipe say 3 times which is quite a very very wild assumption
    # we have actually did it for three or four recipes out of all
    # assuming so , we would again in very contrived sense have 30 images with same 
    # index appearing under the sorted list
    # therefore under such a wild context scanning 200 images would 
    # very highly likely yield 5 different recipe indexes(json)
    for j in range(0,200): 
        index = int(zipped_similarities[j][1].split("->")[0])
        name = zipped_similarities[j][1].split("->")[1].strip()

        # note that we are also checking the recipe names because duplicate ones 
        # would have different index but exactly same names
        if index not in selected_recipes and name not in selected_names:
            # print(index ,name)
            selected_recipes.append(index)
            selected_names.append(name)
            if len(selected_recipes) ==5: # 5 is the no of different recipes we want
                break
    return tuple(zip(selected_recipes,selected_names))

if __name__ == '__main__':
    img_path = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images\train\9_Palak Paneer\1_Palak Paneer.jpg"
    input_recipe(img_path,fetch_encodings(),fetch_encoding_names())
