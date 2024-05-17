from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_image=models.ImageField(upload_to="recipe")
                                 