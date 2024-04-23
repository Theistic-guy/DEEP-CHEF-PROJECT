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

driver=None
search_box=None


path = "C:\\Users\\aditi\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
services=webdriver.ChromeService(executable_path=path) #creates an instance of Chrome WebDriver, which allows you to interact  with the Chrome browser.

def driver_valid(driver):
    if(driver != "Not Intialized"):
        try:
            driver.title
            return True
        except:
            return False
    else:
        return False
    
def create_driver_load(services):
    global driver,search_box
    try:
        driver = webdriver.Chrome(service=services) # Create a new Chrome session and pass the service object
        driver.maximize_window()
        driver.get("https://images.google.com/")
        time.sleep(7)
        search_box=driver.find_element(By.NAME,'q')
    except:
        print("Error file creating and loading the driver")
    
        


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



try:
    create_driver_load(services)
    start=670
    count=1
    maximum_images=6
    train_images_count=8
    extra_images=5
    
    df = pd.read_csv('C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\recipes.csv',skiprows= start,nrows=count,names=['name','link'])
    
    log_file= open("C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\recipes_logfiles.txt","a")
    
    for i in range(len(df['name'])):
        recipe_name=df.loc[i,'name']
        
        log_file.write(str(start+i-1)+"->"+recipe_name)
        log_file.write("\n")
        log_file.flush()
        
        search_box.send_keys(recipe_name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(7)
        
        
        thumbnails=driver.find_elements(By.CLASS_NAME,'mNsIhb')
        
        while(len(thumbnails) < maximum_images+extra_images):
            print("less_images")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
            thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb") 
        
        image_urls=set()  
        successful_count=0
        for thumbnail in thumbnails:
            #print(len(image_urls))
            if(successful_count == maximum_images):
                break
            try:
                thumbnail.click()
                time.sleep(3)
            except:
                print("thumbnail was not clickable")
                continue
            
            pop_up=driver.find_elements(By.CLASS_NAME,'jlTjKd')
            
            for elem in pop_up:
                
                if(elem.tag_name == 'a'):
                    
                  images=elem.find_elements(By.TAG_NAME,"img")
                  #print(len(images))
                  for image in images:
                      
                    class_name=image.get_attribute("class")
                    
                    if len(class_name.split()) >=3 :
                            third = class_name.split()[2]
                            if third == "iPVvYb":
                                img_url = image.get_attribute("src")
                                if img_url not in image_urls :
                                    if(requests.get(img_url).status_code == 200):
                                        image_urls.add(img_url)
                                        successful_count=successful_count+1
                                        print("success ",successful_count)
                            else:
                                print("Failed Duplicate")
                                continue
            time.sleep(7)
            
        download_images("C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\download_images",recipe_name,start+i-1,image_urls,train_images_count)
        
        log_file.write("$$$$")
        log_file.write("\n")
        for url in image_urls:
            log_file.write(url+"\n")
        log_file.write("$$$$")
        log_file.write("\n")
        log_file.flush()
        
        time.sleep(7)
    log_file.close()


except:
    print("unsuccess")  
    driver.quit()    
            
            
            
        
    
    