import recipe_utils as ru
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
path_logs = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\arym\txt\download_logs.txt"
path_driver = r"C:\Users\aryam\Documents\ML\ImageToRecipe\chromedriver.exe"
path_csv = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\links_copy_main.csv"
path_download_folder = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images"



# reload
for i in range(24,27):
    ru.reload_urls_and_save(path_download_folder,path_logs,path_csv,i,8)


# print(ru.check_logs_integrity(path_logs,10))