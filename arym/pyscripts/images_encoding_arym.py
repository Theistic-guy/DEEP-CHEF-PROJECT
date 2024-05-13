
from recipe_utils import feature_encoding,create_CNN,path_train_folder,path_json,path_test_folder,path_encoding_names,path_encodings
import os
import json
import pickle
if __name__ == "__main__":
    recipes_list=os.listdir(path_train_folder)
    recipes_list.sort(key=lambda item:int(item.split("_")[0]))
    with open(path_json,"r") as f:
        data = json.load(f)
    
    encoded_list=[]
    recipe_names=[]
    cnn = create_CNN()
    for i in range(0,len(recipes_list)):
        name = data[i]['name']
        recipe_train_folder = os.path.join(path_train_folder,recipes_list[i])
        train_images = os.listdir(recipe_train_folder)
        for img in train_images:
            img_path = os.path.join(recipe_train_folder,img)
            encoded_list.append(feature_encoding(cnn,img_path))
            recipe_names.append(str(i)+"->"+name.strip())
        recipe_test_folder = os.path.join(path_test_folder,recipes_list[i])
        test_images = os.listdir(recipe_test_folder)
        for img in test_images:
            img_path = os.path.join(recipe_test_folder,img)
            encoded_list.append(feature_encoding(cnn,img_path))
            recipe_names.append(str(i)+"->"+name.strip())
    
    print(len(encoded_list),len(recipe_names))
    # print(recipe_names)
    with open(path_encodings, 'wb') as file:
        pickle.dump(encoded_list, file)
    with open(path_encoding_names, 'wb') as file:
        pickle.dump(recipe_names, file)   

