from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd


path = "C:\\Users\\aditi\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
driver=webdriver.ChromeService(executable_path=path) #creates an instance of Chrome WebDriver, which allows you to interact  with the Chrome browser.
try:
    driver = webdriver.Chrome(service=driver) # Create a new Chrome session and pass the service object
    driver.maximize_window()
    driver.get("https://images.google.com/")
    time.sleep(10)
    search_box=driver.find_element(By.NAME,'q')
    
    start=1
    count=1
    maximum_images=10
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
        count=0
        for thumbnail in thumbnails:
            print(len(image_urls))
            if(count == maximum_images):
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
                  print(len(images))
                  for image in images:
                    print(image.get_attribute("class") )
                    if len(image.get_attribute("class")) >=3 :
                            third = image.get_attribute("class").split()[2]
                            if third == "iPVvYb":
                                img_url = image.get_attribute("src")
                                if img_url not in image_urls :
                                    image_urls.add(img_url)
                                    count=count+1
                            else:
                                continue


        time.sleep(7)
except:
    print("unsuccess")      
            
            
            
        
    
    