from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import recipe_utils as ru
from recipe_utils import download_images,log_urls

# Note : Indexes of the recipe in logs matches index in the dataframe 
# created by reading csv "links_copy" with 
# column heads  as the first line

# link Chrome Webdriver
webdriver_path = "C:\\Users\\aryam\\Documents\\ML\\ImageToRecipe\\chromedriver.exe" # <-- file path used
cService = webdriver.ChromeService(executable_path=webdriver_path)

# Set Chrome Options to stop self-quitting of driver when script ends
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

try :
    # Prepare driver
    driver = webdriver.Chrome(service=cService,options=chrome_options)
    driver.maximize_window()
    driver.get('https://images.google.com/')
    time.sleep(7)
    search_box = driver.find_element(By.NAME,"q")


    # initialize counters and delays

    # For first batch run ,
    # start = 1 
    # i.e. start with the second line of csv becoz
    # first line are names which is overriden by ' names= ' param
    start = 1 
    count= 1
    big_delay = 10
    small_delay = 5
    max_imgs = 10
    extra_imgs = 5
    no_of_imgs_to_train = 8

    # load links.csv
    links_csv_path = "C:\\Users\\aryam\\Documents\\ML\\ImageToRecipe\\DEEP-CHEF-PROJECT\\arym\csv\\links_copy.csv"
    df = pd.read_csv(links_csv_path,skiprows= start,nrows=count,names=['name','link']) #<-- file path used

    # open logs
    download_logs_path = "C:\\Users\\aryam\\Documents\\ML\\ImageToRecipe\\DEEP-CHEF-PROJECT\\arym\\txt\\download_logs.txt"
    f = open(download_logs_path,"a") # <-- file path used

    # Iterate recipes
    for i in range(len(df['name'])):
        recipe = df.loc[i,'name']
        recipe_index_csv = start + i -1

        # make entry to log 
        print(recipe_index_csv,"->",recipe)
        f.write(str(recipe_index_csv)+"->"+ recipe +"\n")
        f.flush()

        # Enter recipe name in box and hit ENTER
        search_box.send_keys(recipe)
        search_box.send_keys(Keys.ENTER)
        time.sleep(big_delay)

        # Fill thumbnails
        thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb")

        # This code is scrapped
        # while len(thumbnails) < max_imgs+extra_imgs: # checking condition before scrolling to minimize HTTP Requests
        #     print("Less images obtained")
        #     time.sleep(small_delay)
        #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #     time.sleep(small_delay)
        #     thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb") 

        # Click on Each thumbnail and Extract src
        image_urls = list()
        success_count = 0
        for thumbnail in thumbnails:
            if success_count == max_imgs:
                break

            try:
                thumbnail.click()
                time.sleep(small_delay)
            except:
                print("Error in clicking thumbnail")
                continue
            
            # Find the pop-up image box
            pop_up_box_elems = driver.find_elements(By.CLASS_NAME,"jlTjKd")

            for elem in pop_up_box_elems:

                # find <a> tag , it has the img
                if elem.tag_name == 'a':
                    # get all the img tags under <a>
                    img_tags = elem.find_elements(By.TAG_NAME,"img")

                    for img in img_tags:

                        # get the attribute of that img tag
                        # two very similar but different <img> tags would be present
                        class_name = img.get_attribute("class")

                        # split and the check the third class name
                        if len(class_name.split()) >=3 :
                            third_part = class_name.split()[2]
                            if third_part == "iPVvYb":
                                img_url = img.get_attribute("src")

                                if img_url not in image_urls :
                                    image_urls.append(img_url)
                                    success_count += 1
                                    print("Found ",success_count)
                                else:
                                    print("Found Duplicate")
            time.sleep(small_delay)
        
        # download the images , first n images go to train and rest to test
        # n is no_of_imgs_to_train
        download_images("C:\\Users\\aryam\\Documents\\ML\\ImageToRecipe\\DEEP-CHEF-PROJECT\\downloaded_images",image_urls,recipe,recipe_index_csv,no_of_imgs_to_train) # <-- file path used
        

        # log the urls
        log_urls(image_urls,recipe_index_csv,recipe,download_logs_path,no_of_imgs_to_train)

        time.sleep(big_delay)

    f.close()        

except Exception as e:
    print("Exception occurred ", e)
    driver.quit()
