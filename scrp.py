import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
url="https://www.food.com/search/indian"
response = requests.get(url)

soup = BeautifulSoup(, 'html.parser')
recipes = soup.find_all('div', class_ ="fd-tile fd-recipe")

# Create a list to store recipe data
recipe_data = []
print(recipes)
# Loop through each recipe element
for recipe in recipes:
  # Extract recipe name (adjust the selector)
  recipe_name = recipe.find('a').text.strip()
  
  #recipe_name = recipe.select_one('.title a').text.strip()
  # Extract recipe link (adjust the selector)
  recipe_link = recipe.find('a', {'href': True})['href']
  #recipe_name = recipe.select_one('.title a').text.strip()
  # Add data to the list
  
  recipe_data.append({'name': recipe_name, 'links': recipe_link})
  print(len(recipe_data))

# Write the data to a CSV file
with open('links.csv', 'w', newline='') as csvfile:
  fieldnames = ['name', 'links']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(recipe_data)

if os.path.exists('links.csv'):
    print("links.csv created successfully!")
else:
    print("Could not create links.csv. Please check permissions.")
    
    
print(recipe_data)
""""
import os
import csv
import pandas as pd
from pyquery import PyQuery as pq

url = "https://www.food.com/search/indian"

response = pq(url)

recipes = response('div.fd-inner-tile')

# Create a list to store recipe data
recipe_data = []
print(recipes)
# Loop through each recipe element
for recipe in recipes:
    # Extract recipe name (adjust the selector)
    recipe_name = pq(recipe)('a').text().strip()

    # Extract recipe link (adjust the selector)
    recipe_link = pq(recipe)('a[href]').attr('href')

    # Add data to the list
    recipe_data.append({'name': recipe_name, 'links': recipe_link})
    print(len(recipe_data))

# Write the data to a CSV file
with open('links.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'links']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(recipe_data)

if os.path.exists('links.csv'):
    print("links.csv created successfully!")
else:
    print("Could not create links.csv. Please check permissions.")

print(recipe_data)"""



"""import scrapy
from scrapy.log import logger
name = "indian_recipes"
start_urls = ["https://www.food.com/search/indian"]

def parse(self, response):
  recipes = response.css(".fd-inner-tile")
  logger.info(f"Found {len(recipes)} recipes")
  for recipe in recipes:
    recipe_name = recipe.css(".title a::text").get().strip()
    recipe_link = recipe.css("a::attr(href)").get()

    yield {
        "name": recipe_name,
        "link": recipe_link,
            }"""
  

            
            



























"""
url='https://www.food.com/recipe/chicken-tikka-masala-25587'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.find('p', {'class': "fd-ingredient-text"}).text.strip())
ul_tag = soup.find('ul', {'class': "ingredient-list"})
li_tags = ul_tag.find_all('a')
for li in li_tags:
    print(li.text.strip())


url='https://www.food.com/search/indian'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())    
"""
