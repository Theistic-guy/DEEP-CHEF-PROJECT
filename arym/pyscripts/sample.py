import recipe_utils as ru
path_logs = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\arym\txt\download_logs.txt"
path_driver = r"C:\Users\aryam\Documents\ML\ImageToRecipe\chromedriver.exe"
path_csv = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\links_copy_main.csv"
path_download_folder = r"C:\Users\aryam\Documents\ML\ImageToRecipe\DEEP-CHEF-PROJECT\downloaded_images"

ru.reload_urls_and_save(path_download_folder,path_logs,path_csv,11,8)
