from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import io
from PIL import Image
import os
import shutil
import pandas as pd
import time 

# called internally by 'download_images' function 
def download_image(download_path,url,filename,ignore_msgs=False):
    ''' download_path is the folder where you want to save the image , filename is the name of the image'''
    try:
        image_content = requests.get(url).content
        image_bytes = io.BytesIO(image_content)
        file_path = os.path.join(download_path, filename)
        image = Image.open(image_bytes)
        jpg_img = image.convert("RGB")
        with open(file_path,"wb") as f:
            jpg_img.save(f,"JPEG")
    except Exception as e:
        if not ignore_msgs:
            print("Exception occurred while downloading an image\n", e)

def download_images(download_folder_path,urls,recipe,recipe_index,train_imgs_count,ignore_msgs=False):
    ''' download_folder_path is the location of folder that contains train and test folders
        each recipe will have one folder in train and one in test, with folder name having index of 
        recipe underscore and the name of recipe. Index of recipe is the zero-indexed position of recipe
        if the csv file is loaded into a dataframe '''
    try:
        recipe_folder_name = str(recipe_index) + "_" + recipe
        train_folder_path = os.path.join(download_folder_path,"train",recipe_folder_name)
        test_folder_path = os.path.join(download_folder_path,"test",recipe_folder_name)

        if not os.path.exists(train_folder_path):
            os.makedirs(train_folder_path)
        if not os.path.exists(test_folder_path):
            os.makedirs(test_folder_path)
            
        img_number = 1
        for url in urls:
            if img_number <= train_imgs_count:
                download_image(train_folder_path,url,str(img_number)+"_"+recipe+".jpg")
            else:
                download_image(test_folder_path,url,str(img_number)+"_"+recipe+".jpg")
            img_number+=1
    except Exception as e:
        if not ignore_msgs:
            print("Exception occurred while downloading images\n", e)

def delete_recipe(download_folder_path,recipe_index,recipe_csv_path,bool_delete_train=False,bool_delete_test=False,ignore_msgs=False):
    ''' download_folder_path is the location of the folder where train and test folder are present\n
        recipe_index is the zero-index based position of recipe if the csv were to be loaded in a dataframe\n
        recipe_csv_path is the path to the csv '''
    
    if  not bool_delete_train and not bool_delete_test:
        return
    
    df = pd.read_csv(recipe_csv_path,skiprows=recipe_index,nrows=1)
    recipe_name = df.iloc[0,0]
    if bool_delete_train:
        path_train = os.path.join(download_folder_path,"train",str(recipe_index)+"_"+recipe_name)
        if os.path.exists(path_train):
            try:
                shutil.rmtree(path_train)
                if not ignore_msgs:
                    print("recipe train images deleted successfully")
            except Exception as e:
                if not ignore_msgs:
                    print("Execption occurred during deletion inside train directory\n",e)
        else:
            if not ignore_msgs:
                print("folder of recipe inside train directory not found")
                print("path received : ",path_train)

    
    if bool_delete_test:
        path_test = os.path.join(download_folder_path,"test",str(recipe_index)+"_"+recipe_name)
        if os.path.exists(path_test):
            try:
                shutil.rmtree(path_test)
                if not ignore_msgs:
                    print("recipe train images deleted successfully")
            except Exception as e:
                if not ignore_msgs:
                    print("Execption occurred during deletion inside test directory\n",e)
        else:
            if not ignore_msgs:
                print("folder of recipe inside train directory not found")
                print("path received : ",path_test)

def view_recipe(path_to_download_logs,recipe_index,path_to_chromeDriver,time_delay,ignore_msgs=False):
    ''' Parses the download_logs.txt file and open each image url in new tab.Test images will comprise
    the right-most tabs . Don't interfere with active tabs as it may not load separate tab for each image.It loads an image 
    in the current tab and then switch'''
    cService = webdriver.ChromeService(executable_path=path_to_chromeDriver)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach",True)
    try:
        with open(path_to_download_logs,"r") as f:
            start_delimiter_pos = 2 * recipe_index + 1
            current_delimiter_pos = 0
            is_start_delim_reached = False
            test_img_urls = []
            for line in f :
                if not is_start_delim_reached:
                    if line.strip() == "$$$$":
                        current_delimiter_pos += 1
                        if current_delimiter_pos == start_delimiter_pos:
                            is_start_delim_reached = True
                            driver = webdriver.Chrome(service=cService,options=chrome_options) # start the driver
                            time.sleep(time_delay)
                else:
                    if ":>" in line:
                        type,link = tuple(line.split(":>"))
                        if type == "train":
                            driver.get(link)
                            driver.switch_to.new_window('tab')
                            time.sleep(time_delay)
                        elif type =="test":
                            test_img_urls.append(link)
                    elif "$$$$" in line:
                        break
            for test_img_url in test_img_urls:
                driver.get(test_img_url)
                driver.switch_to.new_window('tab')
                time.sleep(time_delay)
            if not ignore_msgs:
                print("view_recipe completed successfully")
    except Exception as e:
        if not ignore_msgs:
            print("Exception occurred inside view_recipe\n",e)

def log_urls(image_urls,path_to_download_logs,train_imgs_count,ignore_msgs=False):
    ''' writes the urls in the log file with both start and end delimiters but doesn't log recipe index and it's name'''
    try:
        with open(path_to_download_logs,"a") as f:
            f.write("$$$$\n") # mark the start delimiter
            logged_urls = 0
            for url in image_urls:
                if logged_urls < train_imgs_count:
                    f.write("train:>"+url+"\n")
                else:
                    f.write("test:>" + url+"\n")

            f.write("$$$$\n")
            f.write("\n") # one empty line between end delimiter and new recipe
            f.flush()
        
    except Exception as e:
        if not ignore_msgs:
            print("Exception occurred while logging urls\n",e)
