from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
import base64
import imghdr
import io
import sys
import os
# note : this is an anti-patter , kinda opposes PEP , rejected by Guido himself
# problematic to actual deployment or cross-platforms situations
# check and modify (if needed) to ensure portability and actual deployment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))

from pyscripts.encoder import input_recipe
from pyscripts.recipe_utils import fetch_encoding_names,fetch_encodings,fetch_json
def home(request):
    return render(request,'home.html')

def analyze(request):
    uploaderName= request.POST.get('hiddenElement')
    if uploaderName == "":
        return HttpResponse("No image selected")
    else:
        if uploaderName in request.FILES:
            uploadedFile = request.FILES[uploaderName]
            binary_content = uploadedFile.read()
            params = {"toAlert":False}
            img_type = imghdr.what(None,h=binary_content)
            if img_type == None:
                return HttpResponse("Uploaded file is not recognized as an image")
            if img_type != 'jpeg':
                params['toAlert'] = True
            base64_encoded_data = base64.b64encode(binary_content).decode('ascii')
            dataURL = f'data:image/{img_type};base64,{base64_encoded_data}'
            params['dataURL'] = dataURL

            # convert binary content of uploaded file into bytesIO
            io_file = io.BytesIO(binary_content)
            
            # check cache 
            cached_name = 'cached_data'
            if cached_name not in cache:
                print("oh ho je kya hai gayo")
                cache.set(cached_name, {'encodings': fetch_encodings(), 'encoding_names': fetch_encoding_names(),'json':fetch_json()})
            
            # get the cached data
            cached_data = cache.get(cached_name)

            #process the image
            recipes = input_recipe(io_file,cached_data['encodings'],cached_data['encoding_names'])
            chosen_recipes = list()
            for i in recipes:
                chosen_recipes.append(cached_data['json'][i[0]])

            # for i in range(0,5):
            #     print(chosen_recipes[i]['name'],recipes[i][1])
            print(len(chosen_recipes))
            print(type(chosen_recipes))
            params["json"] = chosen_recipes
            # params["json"] = [{"name": "tyu","cooking_time":"2hrs","calories":"4r234","ingredients":"1 1/2 lbs boneless skinless chicken , cut in 1 inch cubes\n1  cup plain yogurt\n2  tablespoons lemon juice\n2  teaspoons ground cumin\n2  teaspoons    ground red pepper\n2  teaspoons black pepper\n1  teaspoon cinnamon\n1  teaspoon salt\n1  piece    minced ginger (1-inch long)\n6  bamboo skewers (6-inch)\n1  tablespoon unsalted butter\n2  garlic cloves , minced\n1  jalapeno chile , minced\n2  teaspoons ground coriander\n1  teaspoon ground cumin\n1  teaspoon paprika\n1  teaspoon garam masala (buy in Indian market)\n1/2 teaspoon salt\n1 (8   ounce) can tomato sauce\n1  cup    whipping cream\n1/4 cup   chopped fresh cilantro\n","directions":"1 1/2 lbs boneless skinless chicken , cut in 1 inch cubes\n1  cup plain yogurt\n2  tablespoons lemon juice\n2  teaspoons ground cumin\n2  teaspoons    ground red pepper\n2  teaspoons black pepper\n1  teaspoon cinnamon\n1  teaspoon salt\n1  piece    minced ginger (1-inch long)\n6  bamboo skewers (6-inch)\n1  tablespoon unsalted butter\n2  garlic cloves , minced\n1  jalapeno chile , minced\n2  teaspoons ground coriander\n1  teaspoon ground cumin\n1  teaspoon paprika\n1  teaspoon garam masala (buy in Indian market)\n1/2 teaspoon salt\n1 (8   ounce) can tomato sauce\n1  cup    whipping cream\n1/4 cup   chopped fresh cilantro\n"}, {"name": "tyu"}, {"name": "tyu"}, {"name": "tyu"}, {"name": "tyu"}]
            return render(request,'analyze.html',params)
        else:
            return HttpResponse("No image selected")