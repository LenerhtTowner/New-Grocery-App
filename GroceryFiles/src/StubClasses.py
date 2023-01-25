from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import Screen
from kivymd.uix.bottomnavigation import MDBottomNavigation

class RecipeCarousel(Carousel):
    pass

class IngredientInfo(GridLayout):
    pass

class NewRecipeScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class NavBar(MDBottomNavigation):
    pass

#### DEAD CODE STORAGE ####
# import json
# from json import JSONEncoder

# def EncodeRecipesToJson():
#     with open('./venv/recipes.json', 'w') as outfile:
#         recipeData = {}

#         for key in recipes.keys():
#             recipeData[key] = recipes[key].ToDict()
            
#         json.dump(recipeData, outfile, indent=4)


# def LoadRecipesFromJson(filepath = './GroceryFiles/recipes.json'):
#     newRecipeDict = {}
#     recipeData = None
#     with open(filepath, 'r') as inFile:
#         recipeData = json.load(inFile)
        
#         if recipeData == None:
#             return None

#     for key in recipeData.keys():
#         recipeName = recipeData[key]['__name']
#         __ingredients = []

#         for ing in recipeData[key]['__ingredients']:
#             __ingredients.append(Ingredient(ing['__amount'], ing['__unit'], ing['__name']))

#         newRecipeDict[key] = Recipe(recipeName, __ingredients)

#     return newRecipeDict


# #EncodeRecipesToJson()
# recipes = LoadRecipesFromJson()