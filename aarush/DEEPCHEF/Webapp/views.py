from django.shortcuts import render

# Create your views here.
import base64
import string
import os
import json
from .forms import ImageUploadForm
from django.shortcuts import render
from django.config import settings
from .encoder import getrecipes
from PIL import Image

def home_page(request):
    raw_image=None
    uploaded_image=None
    recipe_list_to_return=[]
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            raw_image=form.cleaned_data['image']
            uploaded_image=base64.b64encode(raw_image.file.read().decode('ascii'))
            raw_image=Image.open(raw_image)
            recipes_list=getrecipes(raw_image)
            path_to_json=#path to json
            x=json.load(open(path_to_json))
            
            for i in range(len(recipes_list)):
                name=recipes_list[i]
                y=list(filter(lambda x: x["name"]==name,x))
                if(len(y)!=0):
                    y=y[0]
                    image_link=