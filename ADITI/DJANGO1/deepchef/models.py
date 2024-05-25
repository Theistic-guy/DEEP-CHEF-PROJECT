from django.db import models

# Create your models here.
class recipe(models.Model):
    recipe_image=models.ImageField(upload_to="recipe")
    

