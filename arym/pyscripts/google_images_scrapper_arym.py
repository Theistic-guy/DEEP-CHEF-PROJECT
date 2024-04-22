from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# called internally by 'download_images' function 
def download_image(download_path,url,filename):
    try:
        image_content = requests.get(url).content
        image_bytes = io.BytesIO(image_content)
        file_path = download_path + filename
        image = Image.open(image_bytes)
        with open(file_path,"wb") as f:
            image.save(f,"JPEG")
    except Exception as e:
        print("Exception is ", e)

def download_images(download_folder_path,urls,recipe,recipe_index,train_imgs_count):
    try:
        recipe_folder_name = str(recipe_index) + "_" + recipe
        train_folder_path = os.path.join(download_folder_path,recipe_folder,"train")
        test_folder_path = os.path.join(download_folder_path,recipe_folder,"test")

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
        print("Exception is ", e)

# def delete_directory(download_folder_)

# Note : Indexes of the recipe in logs matches index in the dataframe 
# created by reading csv "links_copy" with 
# column heads  as the first line

# link Chrome Webdriver
path = "C:\\Users\\aryam\\Documents\\ML\\ImageToRecipe\\chromedriver.exe"
cService = webdriver.ChromeService(executable_path=path)

# Set Chrome Options to stop self-quitting of driver when script ends
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

try :
    # Prepare driver
    driver = webdriver.Chrome(service=cService,options=chrome_options)
    driver.maximize_window()
    driver.get('https://images.google.com/')
    time.sleep(15)
    search_box = driver.find_element(By.NAME,"q")


    # initialize counters and delays

    # For first batch run ,
    # start = 1 
    # i.e. start with the second line of csv becoz
    # first line are names which is overriden by ' names= ' param

    start = 1 
    count= 1
    big_delay = 7
    small_delay = 3
    max_imgs = 10
    extra_imgs = 5
    no_of_imgs_to_train = 8

    # load links.csv
    df = pd.read_csv("links_copy.csv",skiprows= start,nrows=count,names=['name','link'])

    # open logs
    f = open("download_logs.txt","a")

    # Iterate recipes
    for i in range(len(df['name'])):
        recipe = df.loc[i,'name']
        recipe_index_csv = start + i -1

        # make entry to log 
        print(recipe_index_csv,"-",recipe)
        f.write(str(recipe_index_csv)+"->"+ recipe +"\n")
        f.flush()

        # Enter recipe name in box and hit ENTER
        search_box.send_keys(recipe)
        search_box.send_keys(Keys.ENTER)
        time.sleep(big_delay)

        # Fill thumbnails
        thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb")

        while len(thumbnails) < max_imgs+extra_imgs: # checking condition before scrolling to minimize HTTP Requests
            print("Less images obtained")
            time.sleep(small_delay)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(small_delay)
            thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb") 

        # Click on Each thumbnail and Extract src
        image_urls = set()
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
            # if len(pop_up_box_elems) != 0:
                # print("pop_up_elements_obtained")
            
            for elem in pop_up_box_elems:

                # find <a> tag , it has the img
                if elem.tag_name == 'a':
                    # print("<a> tag obtained")

                    # get all the img tags under <a>
                    img_tags = elem.find_elements(By.TAG_NAME,"img")

                    # print("img tags obtained")
                    for img in img_tags:

                        # get the attribute of that img tag
                        # two very similar but different <img> tags would be present
                        class_name = img.get_attribute("class")

                        # split and the check the third class name
                        if len(class_name.split()) >=3 :
                            third_part = class_name.split()[2]
                            if third_part == "iPVvYb":
                                img_url = img.get_attribute("src")
                                # print("img url obtained")

                                if img_url not in image_urls :
                                    image_urls.add(img_url)
                                    success_count += 1
                                    print("Found ",success_count)
                                    # f.write("Found " + str(success_count) + "\n")
                                else:
                                    print("Found Duplicate")
                                    # f.write("Found Duplicate" + "\n")
            time.sleep(big_delay)
        
        # download the images
        download_images(".\\downloaded_images",image_urls,recipe,recipe_index_csv,no_of_imgs_to_train)
        f.write("$$$$\n") # mark the start delimiter

        # log the urls
        for url in image_urls:
            f.write(url+"\n")

        f.write("$$$$\n")
        f.write("\n") # one empty line between end delimiter and new recipe
        f.flush()

        time.sleep(big_delay)

f.close()        

except Exception as e:
    print("Exception occurred ", e)
    driver.quit()
