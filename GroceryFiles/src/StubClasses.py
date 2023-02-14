from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.bottomnavigation import MDBottomNavigation

class RecipeCarousel(Carousel):
    pass

class IngredientInfo(GridLayout):
    pass

class NewRecipeScreen(Screen):
    pass

class NavBar(MDBottomNavigation):
    pass

class RecipeListItem(BoxLayout):
    pass

class RecipeDataPanel(BoxLayout):
    pass


#### DEAD CODE STORAGE ####

# def AddRecipeToJson(recipe:Recipe):
#     recipeData = {}
#     with open('./GroceryFiles/json/recipes.json', 'r') as infile:
#         try:
#             recipeData = json.load(infile)
#         except:
#             pass
            
#     with open('./GroceryFiles/json/recipes.json', 'w') as outfile:
#         recipeData[recipe.GetName()] = recipe.ToDict()
#         json.dump(recipeData, outfile, indent=4)
#         LoadRecipesFromJson()


# def DeleteRecipeFromJson(recipe_name:str):
#     recipeData = {}
#     with open('./GroceryFiles/json/recipes.json', 'r') as infile:
#         try:
#             recipeData = json.load(infile)
#         except:
#             return
    
#     with open('./GroceryFiles/json/recipes.json', 'w') as outfile:
#         try:
#             del recipeData[recipe_name]
#         except:
#             pass
        
#         json.dump(recipeData, outfile, indent=4)