# TODO-Create Screen for Recipe entry(too include asking the user to find iten weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.
    #Create def(s) for converting user recipes into local recipes
# TODO-Creat functionality to allow user to add recipes to a JSON file for local use.(Pri 2)
    #SUB-TASKS TBD
# TODO-Create functionality for dynamic widget generation.(Pri 3)
'''
ROBERT'S NOTES TO ETHAN

ETHAN'S NOTES TO ROBERT
    
'''

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from RecipeDB import recipeDB
from GroceryListScreen import GroceryListScreen
from RecipeSearchScreen import SearchRecipeScreen
from RecipeScreen import RecipeScreen
from StubClasses import *

#Sets a standard window size(*MUST be altered to fit any window size before going into BETA trials)
Window.size = (600, 900)

kv = Builder.load_file("grocerykivy.kv")

class TestApp(MDApp):
    active_list = None

    def build(self):
        return MainScreen()

if __name__ == '__main__':
    TestApp().run()
    recipeDB.Close()