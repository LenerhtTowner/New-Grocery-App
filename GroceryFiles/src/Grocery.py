# COMPLETED - TODO-Add functionality to allow app to add multiple recipes ingredients.(Priority 1)
# TODO-Create Screen for Recipe entry(too include asking the user to find iten weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.
    #Create def(s) for converting user recipes into local recipes
# TODO-Creat functionality to allow user to add recipes to a JSON file for local use.(Pri 2)
    #SUB-TASKS TBD
# TODO-Create functionality for dynamic widget generation.(Pri 3)
'''
ROBERT'S NOTES TO ETHAN

I Refactored Recipes.py and changed the name to RecipeDB.py. All database related functions now exist within a RecipeDB class.
See the comment at the top of RecipeDB.py for an example of usage.
This was done to that the connection to the db could be managed in one place and to group together similar functionality.
I also moved the *.py files and the .kv file into a foler named src and The json files into a folder named json.
The file structure was getting difficult to read so I thought that cleaning and organizing things would be beneficial

ETHAN'S NOTES TO ROBERT
    
'''

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

#Imports functionality to allow user to search recipies from the recipes.db database.
from RecipeSearchScreen import SearchRecipeScreen

#StubClasses refers to classes that MUST exist to bulster the Kivy framework but have no actual functionality.
from StubClasses import NewRecipeScreen

#Imports the recipe screen from external file.
from RecipeScreen import RecipeScreen

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