from django.shortcuts import render,redirect
from .forms import Image_Upload
from .models import *
import os
from PIL import Image
import json
import base64
from .encoder import input_recipe
import string
import io
import base64
from django.conf import settings
from django.shortcuts import render 


def find_recipe(request):
    og_image=None
    uploaded_image=None
    return_similar_recipes=[]
    if request.method == 'POST':  # if we trying to upload data to server
        form = Image_Upload(request.POST,request.FILES)   #form contains the data(POST) which has to besubmitted to server and the FILES i.e. Image
        if form.is_valid(): #VALIDATION RULES are present in the Image_Upload
            og_image=request.FILES.get('image')
            Recipe.objects.create(
                og_image=og_image
            )
            queryset=Recipe.objects.all()
            queryset=queryset.last().recipe_image
            for i in range(len(similar_recipes)):
                recipe_name=similar_recipes[i]
                recipe_name=recipe_name.split("_")[1]
                recipe_details=list(filter(lambda x: x["name"]==recipe_name,x))
                if len(recipe_details) != 0:
                    y=recipe_details[0]
                    image_link= '''Add the link here'''
                    cooking_duration=y["cooking_time"]
                    nutrition_calories=y["calories"]
                    recipe_ingredients=y["ingredients"]
                    recipe_direction=y["directions"]
                    list_to_append=[string.capwords(recipe_name),image_link,recipe_ingredients,recipe_direction,cooking_duration,nutrition_calories]
                    return_similar_recipes.append(list_to_append)
    else:
        form=Image_Upload()
        
    return render(request, 'C:\\Users\\aditi\\OneDrive\\Desktop\\DJANGO\\deepchef_webapp\\webapp1\\templates\\home.html', {'form': form, 'uploaded_image': og_image,
                                                'recipe_list_to_return': return_similar_recipes[:4],
                                                'similar_recipe_list': return_similar_recipes[4:10]})      
    
    
    
