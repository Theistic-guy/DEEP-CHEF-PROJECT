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
from recipe_utils import download_images,log_urls,fetch_response_from_url

driver = None

# link Chrome Webdriver
webdriver_path = ru.path_driver
cService = webdriver.ChromeService(executable_path=webdriver_path)




# def isDriverValid(driver):
#     if driver != "Not initialized":
#         try:
#             driver.title
#             return True
#         except:
#             return False
#     else:
#         return False

def create_driver_and_load(cService,delay,detach=True):
    global driver
    try:
        # Set Chrome Options to stop self-quitting of driver when script ends
        chrome_options = Options()
        chrome_options.add_experimental_option("detach",detach)
        driver = webdriver.Chrome(service=cService,options=chrome_options)
        driver.maximize_window()
        driver.get('https://images.google.com/')
        time.sleep(delay)
    except Exception as e :
        print("Exception occurred creating driver \n",e)







try :
    # Prepare driver
    create_driver_and_load(cService,4)


    # initialize counters and delays

    # For first batch run ,
    # start = 1 
    # i.e. start with the second line of csv becoz
    # first line are column names which is overriden by ' names= ' param
    start = 114
    count= 9
    big_delay = 10
    small_delay = 3
    max_imgs = 10
    extra_imgs = 5
    no_of_imgs_to_train = 8

    # max attempts to re-start the driver 
    max_attempts_start_driver = 3

    # load links.csv

    links_csv_path = ru.path_csv
    df = pd.read_csv(links_csv_path,skiprows= start,nrows=count,names=['name','link']) #<-- file path used

    # open logs
    download_logs_path = ru.path_logs
    f = open(download_logs_path,"a") # <-- file path used

    # Iterate recipes
    names_length  = len(df['name'])
    i = 0
    while i < names_length:

        recipe = df.loc[i,'name']
        recipe_index_csv = start + i -1

        # Note : Indexes of the recipe in logs matches index in the dataframe 
        # created by reading csv "links_copy" with 
        # column heads  as the first line
        # through out the code , recipe_index or index of recipe carries the same 
        # meaning

        # make entry to log 
        print(recipe_index_csv,"->",recipe)
        f.write(str(recipe_index_csv)+"->"+ recipe +"\n")
        f.flush()

        # Enter recipe name in box and hit ENTER
        search_box = driver.find_element(By.NAME,"q")
        search_box.clear()
        search_box.send_keys(recipe)
        search_box.send_keys(Keys.ENTER)
        time.sleep(big_delay)

        # Fill thumbnails
        thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb")
        if (len(thumbnails)<max_imgs+extra_imgs):
            print("driver session closed")
            driver.quit()
            print("creating new driver session")
            create_driver_and_load(cService,4)
            max_attempts_start_driver -=1 
            if max_attempts_start_driver < 0:
                raise
            i -=1

            

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
                                    if fetch_response_from_url(img_url,100).status == 200:
                                        image_urls.append(img_url)
                                        success_count += 1
                                        print("Found ",success_count)
                                    else:
                                        print("Image skipped:status_code not 200")
                                else:
                                    print("Found Duplicate")
            time.sleep(small_delay)
        
        # log the urls
        log_urls(image_urls,download_logs_path,no_of_imgs_to_train)
        

        # download the images , first n images go to train and rest to test
        # n is no_of_imgs_to_train
        download_images(ru.path_download_folder,image_urls,recipe,recipe_index_csv,no_of_imgs_to_train) # <-- file path used

        time.sleep(big_delay)

        i += 1 # increment the loop counter

    f.close()        

except Exception as e:
    print("Exception occurred in main script .Quitting Driver \n ", e)
    # driver.quit()
