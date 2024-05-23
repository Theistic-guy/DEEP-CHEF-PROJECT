from django.shortcuts import render,redirect

# Create your views here.
import base64
import string
import os
import imghdr
import json
from .forms import ImageUploadForm
from django.conf import settings
from .encoder import getrecipes
from PIL import Image
import io
from .models import *
from django.shortcuts import render



def home(request):
    queryset=None
    recipe_list_to_return=[]
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            recipe_image=request.FILES.get('image')
            Recipe.objects.create(
                recipe_image=recipe_image,
            )
            queryset= Recipe.objects.all()
            queryset=queryset.last().recipe_image
            DIR=  #path to static
            c=str(queryset)
            recipes_list=getrecipes(os.path.join(DIR,c))
            path_to_json= # path to json
            x=json.load(open(path_to_json))
            for i in range(len(recipes_list)):
                name=recipes_list[i]
                recipe_name=name.split("_")[1]
                y=list(filter(lambda x: x["name"]==recipe_name,x))
                if(len(y)!=0):
                    y=y[0]
                    image_link= #if needed add path to image
                    calories=y['calories']
                    cooking_time=y['cooking_time']
                    directions=y['directions']
                    ingredients=y['ingredients']
                    servings=y['serving']
                    list_to_append=[string.capwords(recipe_name),image_link,cooking_time,servings,calories,ingredients,directions]
                    recipe_list_to_return.append(list_to_append)
    else:
        form=ImageUploadForm()
    return render(request,'home.html',{'form': form,'recipe':queryset,
                                                'recipe_list_to_return': recipe_list_to_return[:5],
                                                'similar_recipe_list': recipe_list_to_return[5:10]})
    
    
    
    
    