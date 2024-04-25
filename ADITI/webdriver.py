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
import utils 
from utils import download_images,logfile_urls
from selenium.webdriver.chrome.options import Options

driver=None

path = "C:\\Users\\aditi\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
services=webdriver.ChromeService(executable_path=path) #creates an instance of Chrome WebDriver, which allows you to interact  with the Chrome browser.

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

def create_driver_load(services,option):
    global driver
    try:
        driver = webdriver.Chrome(service=services,options=option) # Create a new Chrome session and pass the service object
        driver.maximize_window()
        driver.get("https://images.google.com/")
        time.sleep(7)
    except Exception as e :
        print("Error file creating and loading the driver")
    
try:
    create_driver_load(services,chrome_options)
    start=693
    count=1
    maximum_images=10
    train_images_count=8
    extra_images=5
    new_driver_count=3
    
    df = pd.read_csv('C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\recipes.csv',skiprows= start,nrows=count,names=['name','link'])
    
    log_file= open("C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\recipes_logfiles.txt","a")
    
    csv_length=len(df['name'])
    i=0
    
    while(i<csv_length):
        
        recipe_name=df.loc[i,'name']
        print(start+i,"->",recipe_name)
        log_file.write(str(start+i)+"->"+recipe_name)
        log_file.write("\n")
        log_file.flush()
        
        search_box = driver.find_element(By.NAME,"q")
        search_box.clear()
        search_box.send_keys(recipe_name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(10)
        
        
        thumbnails=driver.find_elements(By.CLASS_NAME,'mNsIhb')
        
        if(len(thumbnails) < maximum_images+extra_images):
            print("less_images")
            driver.quit()
            print("create new driver")
            new_driver_count=new_driver_count-1
            create_driver_load(services,chrome_options)
            if new_driver_count < 0:
                raise
            i=i-1
        
        image_urls=list()  
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
                                        image_urls.append(img_url)
                                        successful_count=successful_count+1
                                        print("success ",successful_count)
                                    else:
                                        print("inaccessbile")
                                        continue
                                else:
                                    print("Failed Duplicate")
                                    continue
            time.sleep(7)
        logfile_urls(image_urls,train_images_count,"C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\recipes_logfiles.txt")
        download_images("C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\downloaded_images",recipe_name,start+i,image_urls,train_images_count)
        
        time.sleep(7)
        i=i+1
    log_file.close()


except Exception as e:
    print("unsuccess",e)  
    driver.quit()    
            
            
            
        
    
    