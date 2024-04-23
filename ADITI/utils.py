from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
import os
import shutil

def download_image(url,folder,img_no,recipe_name):
    try:
        img_content=requests.get(url,timeout=10)
        if(img_content.status_code == 200):
            img_content=img_content.content
            image_file=io.BytesIO(img_content) 
            image=Image.open(image_file)
            jpg_file=image.convert("RGB")
            file_name=str(img_no)+"_"+recipe_name
            file_path=os.path.join(folder,file_name)
            with open(file_path,"wb") as f: # wb ---> write bytes
                image.save(f,"JPEG") 
                print('Successful download ',img_no)  
        else:
            print("url was inaccessible") 
    except:
        print("Failed")
        
def download_images(download_path,recipe_name,recipe_index,urls,count):
    try:
        recipe_name1=str(recipe_index) + "_" + recipe_name
        train=os.path.join(download_path,"train",recipe_name1)
        test=os.path.join(download_path,"test",recipe_name1)
        if not os.path.exists(train):
            os.makedirs(train)
        if not os.path.exists(test):
            os.makedirs(test)
        x=1
        for url in urls:
            if(x<=count):
                download_image(url,train,x,recipe_name)
            else:
                download_image(url,test,x,recipe_name)
            x=x+1
            time.sleep(1)
            
    except:
        print("Failed download")
        
def logfile_urls(image_urls,train_images,log_path):
    try:
        with open(log_path,"a") as log_file:
            log_file.write("$$$$")
            log_file.write("\n")
            train_urls=0
            for url in image_urls:
                if(train_urls<train_images):
                    log_file.write("train:>"+url+"\n")
                else:
                    log_file.write("test:>" + url+"\n")
                train_urls += 1
            log_file.write("$$$$\n")
            log_file.write("\n")
            log_file.flush()
    except:
        print("Not logged")


