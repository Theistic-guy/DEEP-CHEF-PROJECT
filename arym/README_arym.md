This file contains information concerning usage of files under 'arym' folder and their dependencies
Different folders contain files with types respective of their names

<h4>Under csv</h4>
links.csv contains recipe names and their links with first line as header , "name,link" is the actual header line
links_copy.csv is copy of the above to work with , tweak with , read-write etc. to prevent unknown changes

<h4>Under html</h4>
food_arym.html has the html code of the page loaded when "indian" keyword is searched on "food.com" , it contains code of JS inserted elements that contains recipe name and their link . This file is used by scrapper_arym.ipynb to parse and prepare links.csv.

<h4>Under notebooks</h4>
scrapper_arym.ipynb parses the food_arym.html and prepares the links.csv

<h4>Under pyscripts</h4>
google_images_scrapper_arym.py uses chrome webdriver and selenium library to automatically open Chrome , search images , extract thumbnails, click on thumbnails and extract the "src" of the img tag . All the image urls of a particular recipe are stored in the download_logs.txt in the "txt" folder. 
After installing "chromedriver.exe" as per your chrome version , specify its path in the global "path" variable in the above file.

<h4>Under txt</h4>
In the scrapper_arym.ipynb file, certain unnecessary keywords are searched in the list of recipe names and the flagged recipe names are outputted into the "Corrected_names.txt" where they are manually edited ( edit the name after ' --> ') . After editing , the edited names are copied into a dataframe which is then written back to the csv file. Note that links.csv and its copy links_copy.csv already contains a lot of changes made by me but 'Corrected_names.txt' doesn't reflect that (actually it was overwritten in a run) 

About download_logs.txt , it contains the recipe index and the recipe name , recipe index refers to the zero-indexed position of a recipe in the links.csv file if it were to be loaded in a pandas dataframe (.read_csv("links.csv")). The format of download_logs.txt is (from line 23 to 35) :-

recipe_index1->recipe_name1
$$$$
htttps://......
htttps://......
htttps://......
.
.
$$$$

recipe_index2->recipe_name2
.
.
$$$$

urls of images of a recipe are between 4 dollar signs at start and at end. There is an empty line between $$$$ of previous recipe and recipe_index->recipe_name of next recipe
Replace recipe_index1 with the actual index and recipe_name1 with the actual recipe name
