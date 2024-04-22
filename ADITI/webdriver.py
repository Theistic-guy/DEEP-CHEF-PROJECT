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
df = pd.read_csv("recipes.csv",skiprows= 0,nrows=10,names=['name','link'])
df.head()
try:
    driver = webdriver.Chrome(service=driver) # Create a new Chrome session and pass the service object
    driver.maximize_window()
    driver.get("https://images.google.com/")
    time.sleep(3)
    search_box=driver.find_element(By.NAME,'q')
    
    start=1
    count=1
    maximum_images=10
    df = pd.read_csv("recipes.csv",skiprows= start,nrows=10,names=['name','link'])
    
    for i in range(len(df['name'])):
        recipe_name=df.loc[i,'name']
        print(start+i-1,recipe_name)
        
        search_box.send_keys(recipe_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(7)
        
        image_urls=set()
        thumbnails=driver.find_elements(By.CLASS_NAME,'mNsIhb')
        
        while(len(thumbnails) < maximum_images+5):
            time.sleep(3)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
            thumbnails = driver.find_elements(By.CLASS_NAME,"mNsIhb") 
            
        for thumbnail in thumbnails:
            
            if(len(image_urls) == maximum_images):
                break
            try:
                thumbnail.click()
                time.sleep(3)
            except:
                print("thumbnail was not clickable")
                continue
            
            pop_up=driver.find_elements(By.CLASS_NAME,'jlTjKd')
            for elem in pop_up:
                images=elem.find_elements(By.TAG_NAME,"img")
                for image in images:
                    if(image.get_attribute("class") == "sFlh5c pT0Scc iPVvYb" and image.get_attribute("src") not in image_urls):
                        url=image.get_attribute("src")
                        image_urls.add(url)
            time.sleep(7)
    time.sleep(7)
except:
    print("unsuccess")      
            
            
            
        
    
    