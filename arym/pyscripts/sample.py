import recipe_utils as ru
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
path_logs = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\arym\txt\download_logs.txt"
path_driver = r"C:\Users\aryam\Documents\ML\ImageToRecipe\chromedriver.exe"
path_csv = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\links_copy_main.csv"
path_download_folder = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images"
path_json = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\arym\json\recipes.json"
'''
Potato Curry with Spinach and Chickpeas  --  Sweet Potato Curry With Spinach and Chickpeas
Chicken Makhani (Indian Butter Chicken)  --  Chicken Makhani
Cashew Chicken  --  Cashew Chicken Curry
Cucumber Salad  --  Cucumber Salad with curd
Ginger Yogurt  --  Ginger Yogurt recipe
Indian Fry Bread  --  American Indian Fry Bread
Garbanzo Beans  --  Garbanzo Beans recipe
'''


# with open(path_logs,"r") as f:
#     df = pd.read_csv(path_csv)
#     index = 0
#     for line in f:
#         if("->" in line):
#             name_in_log = line.split("->")[1].strip()
#             name_in_csv = df.at[index,'name'].strip()
#             if(name_in_log != name_in_csv):
#                 print(name_in_log," -- ",name_in_csv)
#             index+=1
