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


def download_image(url,folder,img_no,recipe_name):
    try:
        img_content=requests.get(url).content
        image_file=io.BytesIO(img_content) 
        image=Image.open(image_file)
        file_name=str(img_no)+recipe_name
        file_path=os.path.join(folder,file_name)
        with open(file_path,"wb") as f:# wb ---> write bytes
            image.save(f,"JPEG") 
            print('Successful download ',img_no)    
    except:
        print("Failed")
        
def download_images(download_path,recipe_name,recipe_index,urls,count):
    try:
        recipe_name1=recipe_name+str(recipe_index)
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
    except:
        print("Failed download")

path = "C:\\Users\\aditi\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
driver=webdriver.ChromeService(executable_path=path) #creates an instance of Chrome WebDriver, which allows you to interact  with the Chrome browser.
try:
    driver = webdriver.Chrome(service=driver) # Create a new Chrome session and pass the service object
    driver.maximize_window()
    driver.get("https://images.google.com/")
    time.sleep(15)
    search_box=driver.find_element(By.NAME,'q')
    
    start=1
    count=1
    maximum_images=10
    train_images_count=8
    
    df = pd.read_csv('C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\recipes.csv',skiprows= start,nrows=count,names=['name','link'])
    
    for i in range(len(df['name'])):
        recipe_name=df.loc[i,'name']
        print(start+i,recipe_name)
        
        search_box.send_keys(recipe_name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(7)
        
        
        thumbnails=driver.find_elements(By.CLASS_NAME,'mNsIhb')
        
        while(len(thumbnails) < 15):
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
                    if len(image.get_attribute("class").split()) >=3 :
                            third = image.get_attribute("class").split()[2]
                            if third == "iPVvYb":
                                img_url = image.get_attribute("src")
                                if img_url not in image_urls :
                                    image_urls.add(img_url)
                                    successful_count=successful_count+1
                                    print("success ",successful_count)
                            else:
                                continue
            time.sleep(7)
        
        for url in image_urls:
            print(url)
        download_images("C:\\Users\\aditi\\OneDrive\\Desktop\\PROJECTS\\DEEP-CHEF-PROJECT\\ADITI\\download_images",recipe_name,start+i,image_urls,train_images_count)
        time.sleep(7)
            
except:
    print("unsuccess")  
    driver.quit()    
            
            
            
        
    
    