from django.shortcuts import render,redirect

# Create your views here.
import base64
import string
import os
import json
from .forms import ImageUploadForm
from django.conf import settings
from .encoder import getrecipes
from PIL import Image
import io
from .models import *

from django.shortcuts import render



def home_page(request):
    raw_image=None
    uploaded_image=None
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
            """raw_image=form.cleaned_data['image']
            uploaded_image=base64.b64encode(raw_image.file.read())
            uploaded_image=io.BytesIO(uploaded_image)
            img=Image.open(uploaded_image)
            #raw_iamge=Image.open(uploaded_image)
            img.save(uploaded_image, "JPG")
            io.BytesIO().seek(0)
            uploaded_image= img.read()
            databytes=io.BytesIO(uploaded_image)
            #Image.open(databytes)"""
            #print(queryset)
            #C:\Users\Aarush Raj\OneDrive\Desktop\img2rec\DEEP-CHEF-PROJECT\aarush\public\static
            DIR=r"C:/Users/Aarush Raj/OneDrive/Desktop/img2rec/DEEP-CHEF-PROJECT/aarush/DEEPCHEF/public/static/" 
            c=str(queryset)
            recipes_list=getrecipes(os.path.join(DIR,c))
            path_to_json=r"C:\Users\Aarush Raj\OneDrive\Desktop\img2rec\DEEP-CHEF-PROJECT\aarush\recipes.json"
            x=json.load(open(path_to_json))
            
            for i in range(len(recipes_list)):
                name=recipes_list[i]
                recipe_name=name.split("_")[1]
                y=list(filter(lambda x: x["name"]==recipe_name,x))
                if(len(y)!=0):
                    y=y[0]
                    image_link="C:\\Users\\Aarush Raj\\OneDrive\\Desktop\\img2rec\\DEEP-CHEF-PROJECT\\downloaded_images\\train\\" + name + "\\1_" + recipe_name + ".jpg"
                    calories=y['calories']
                    cooking_time=y['cooking_time']
                    directions=y['directions']
                    ingredients=y['ingredients']
                    servings=y['serving']
                    list_to_append=[string.capwords(recipe_name),image_link,cooking_time,servings,calories,ingredients,directions]
                    recipe_list_to_return.append(list_to_append)
                    
            #return redirect(' /')
    else:
        form=ImageUploadForm()
    return render(request,r'C:\Users\Aarush Raj\OneDrive\Desktop\img2rec\DEEP-CHEF-PROJECT\aarush\DEEPCHEF\Webapp\templates\Webapp\home.html',{'form': form, 'uploaded_image': uploaded_image,
                                                'recipe_list_to_return': recipe_list_to_return[:4],
                                                'similar_recipe_list': recipe_list_to_return[4:10]})