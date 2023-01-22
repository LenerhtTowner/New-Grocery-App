# COMPLETED - TODO-Add functionality to allow app to add multiple recipes ingredients.(Priority 1)
# TODO-Create Screen for Recipe entry(too include asking the user to find iten weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.
    #Create def(s) for converting user recipes into local recipes
# TODO-Creat functionality to allow user to add recipes to a JSON file for local use.(Pri 2)
    #SUB-TASKS TBD
# TODO-Create functionality for dynamic widget generation.(Pri 3)
'''
ROBERT'S NOTES TO ETHAN
    Completed the first TODO on lines 77 - 86.
    I got all the recipe data into the database.
    The recipes can not currently be retrieved by name.
    Each recipe has an ID number (from 1 to 38156). To fetch a recipe use: fetch_recipe(recipe_id:int)

    example:

        from Recipes import *

        recipe = fetch_recipe(1).ToDict()

        print(recipe['__name'])

        for ingredient in recipe["__ingredients"]:
            print(ingredient)

    result:
        Instant Pot Hamburger Soup
        {'_Ingredient__name': 'ground beef', '_Ingredient__amount': '1.5', '_Ingredient__unit': 'pounds'}
        {'_Ingredient__name': 'onion, finely chopped', '_Ingredient__amount': '1', '_Ingredient__unit': 'medium'}
        {'_Ingredient__name': 'beef consomme', '_Ingredient__amount': '3', '_Ingredient__unit': '(14.5 ounce) cans'}
        {'_Ingredient__name': 'diced tomatoes', '_Ingredient__amount': '1', '_Ingredient__unit': '(28 ounce) can'}
        {'_Ingredient__name': 'water', '_Ingredient__amount': '2', '_Ingredient__unit': 'cups'}
        {'_Ingredient__name': 'condensed tomato soup', '_Ingredient__amount': '1', '_Ingredient__unit': '(10.75 ounce) can '}
        {'_Ingredient__name': 'carrots, finely chopped', '_Ingredient__amount': '4', '_Ingredient__unit': ''}
        {'_Ingredient__name': 'celery, finely chopped', '_Ingredient__amount': '3', '_Ingredient__unit': 'stalks'}
        {'_Ingredient__name': 'pearl barley', '_Ingredient__amount': '4', '_Ingredient__unit': 'tablespoons'}
        {'_Ingredient__name': 'dried thyme', '_Ingredient__amount': '0.5', '_Ingredient__unit': 'teaspoon'}
        {'_Ingredient__name': 'bay leaf', '_Ingredient__amount': '1', '_Ingredient__unit': ''}

ETHAN'S NOTES TO ROBERT

'''

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

#Imports functionality to allow user to search recipies from the recipes.db database.
from RecipeSearchScreen import SearchRecipeScreen

#StubClasses refers to classes that MUST exist to bulster the Kivy framework but have no actual functionality.
from StubClasses import *

#Imports the recipe screen from external file.
from RecipeScreen import RecipeScreen

#Imports functionality from the Recipies.py file
from Recipies import *

#Sets a standard window size(*MUST be altered to fit any window size before going into BETA trials)
Window.size = (600, 900)

kv = Builder.load_file("grocerykivy.kv")

class TestApp(MDApp):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(RecipeScreen(name='Recipe'))
        sm.add_widget(NewRecipeScreen(name='NewRecipe'))
        sm.add_widget(SearchRecipeScreen(name='SearchRecipe'))
        
        return sm

if __name__ == '__main__':
    TestApp().run()