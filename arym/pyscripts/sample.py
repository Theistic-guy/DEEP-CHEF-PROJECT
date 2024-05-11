import recipe_utils as ru
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
import os

path_logs = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\arym\txt\download_logs.txt"
path_driver = r"C:\Users\aryam\Documents\ML\ImageToRecipe\chromedriver.exe"
path_csv = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\links_copy_main.csv"
path_download_folder = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images"
path_json = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\arym\json\recipes.json"

list1 = os.listdir(r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images\train")
df = pd.read_csv(path_csv)
for i in range(0,len(list1)):
    name_in_folder = list1[i].split("_")[1]
    index = int(list1[i].split("_")[0])-2
    
    if(name_in_folder != df.at[index,'name']):
        print(name_in_folder," -- ",df.at[index,'name'])

