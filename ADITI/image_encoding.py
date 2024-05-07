import os
import numpy as np
from keras.preprocessing import image
from keras.applications import densenet
import pickle

cnn_model=densenet.DenseNet201(include_top= False ,weights='imagenet', input_shape=(256,256,3),pooling='avg',classes= 350) 
''' 
include_top is false when we to customize the output of the model , it is mainly used when we using the model forn someone personal model where we dont want it to give pre defined outputs

weights is optional can be none or imagenet which is a predifen dataset of weights used in cnn

image_shape is optional defines the aspect ratio of the training dataset

pooling is also optional which defines how the features are being chosen in the last convolution layer like here it is avg , it can be max also 

classes is the number of classes we want to segregate our images in like we have around 350 classes of image or recipe 
'''

def feature_encoding(url):
    img=image.load_img(url,target_size=(256,256))
    img=image.img_to_array(img)
    img=np.expand_dims(img,axis=0)
    encoded=densenet.preprocess_input(img)
    encoded=cnn_model.predict(encoded)
    print(len(encoded[0]))
    return encoded


'''
The above function turns images to vector encoding and takes image as a imput. 

img_to_array turns image to a numerical array.

expand_dims is used to expand the dimension of the img vector

densenet.preprocess_input is used to preprocess the data according to the requirements of the specific pre-trained model and then the cnn model is applied on the image vector 
'''


'''This line ensures that the following code block is only executed if the script is run directly (not imported as a module)'''

if __name__ == '__main__':  
    
    recipes_list=os.listdir("C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\downloaded_images\\train")
    encoded_list=[]
    count=0
    for i in recipes_list[0:1]:
        name=i.split("_")[1]
        for j in range(0,8):
            img_path="C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\downloaded_images\\train\\"+i+"/"+str(j+1)+'_'+ name +'.jpg'
            #img=image.load_img(img_path,target_size=(256,256))
            encoding=feature_encoding(img_path)
            encoded_list.append(encoding)
        count=count+1
        print(count)
    print(len(recipes_list),len(encoded_list))
    
    with open('encodings.txt', 'wb') as file:
        pickle.dump(encoded_list, file)
    with open('encoding_name.txt', 'wb') as file:
        pickle.dump(recipes_list, file)   
    
    


    