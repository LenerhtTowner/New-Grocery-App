# TODO - **Create Screen for Recipe entry(too include asking the user to find item weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.**
    #Create def(s) for converting user recipes into local recipes.
#TODO - Update the calculation function so that the user can be prompted to enter gram/liter per units, and have that function fill in the data for the rest of the measrues.(i.e. If the user enters an amount per cup the program uses this info to calculate Tbs tsp and so on.)
#TODO - Create functionality to gather data from the user.
#TODO - Finish dev on getting the users lists to show on screen for review and modification and display the grocery items needed to make those meals.
#TODO - Add functionality to attempt to load recipe data from an arbitrary Json file
    #If the file does not contain valid recipe data then the function should print an error and return None

'''
ROBERT'S NOTES TO ETHAN
    I moved the pass logic to JsonUtils so that it can apply any time an entry already exists in a
    file. I also added red error messages that print to the console when that happens. 

    The loading and unloading of json files has been cleaned up and moved to the jsonUtils file and
    the names of all of the json files are now stored in a jsonFiles object in JsonUtils. This 
    is only meant to reduce the trouble of misspelling and to allow for a central location for the 
    strings in case one of the file names changes for some reason. The syntax to add an entry to 
    a json file, load a json file and delete an entry from a json file are as follows:

    
Load groceyrLits.json from the file:
    ########################################################
        import JsonUtils
        from JsonUtils import JsonFiles

        lists = JsonUtils.LoadFromJson(JsonFiles.GROCERY_LISTS)
    ########################################################

        
Add an entry to groceyrLists.json:
    ########################################################
        import JsonUtils
        from JsonUtils import JsonFiles

        JsonUtils.AppendToJson("listName", {"list": "contents"}, JsonFiles.GROCERY_LISTS)
    ########################################################
    JsonUtils.AppendToJson() accepts a keword argument to indicate if you would like to
    overwrite the value if it already exists. By default it is True. If you do not want to 
    overwrite then make sure to specify False at the end of the arguments. I am not married to 
    this default so If you would like to change it that would not hurt my feelings
    ########################################################
        JsonUtils.AppendToJson("listName", {"list": "contents"}, JsonFiles.GROCERY_LISTS, overwrite=False)
    ########################################################
        

Remove an existing entry from groceryLists.json
    ########################################################
        import JsonUtils
        from JsonUtils import JsonFiles

        JsonUtils.DeleteFromJson("listName", JsonFiles.GROCERY_LISTS)
    ########################################################

        
ETHAN'S NOTES TO ROBERT

'''

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from RecipeDB import recipeDB
from GroceryListScreen import GroceryListScreen
from RecipeSearchScreen import SearchRecipeScreen
from RecipeScreen import RecipeScreen
from MainScreen import MainScreen
from StubClasses import *

#Sets a standard window size(*MUST be altered to fit any window size before going into BETA trials)
Window.size = (600, 900)

kv = Builder.load_file("grocerykivy.kv")


class TestApp(MDApp):
    ctrl = False
    shft = False

    mainScreen = None

    def build(self):
        self.mainScreen = MainScreen()

        self.mainScreen._keyboard = Window.request_keyboard(self._keyboard_closed, self.mainScreen)
        self.mainScreen._keyboard.bind(on_key_down=self._on_keyboard_down)

        return self.mainScreen


    def _keyboard_closed(self):
        self.mainScreen._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.mainScreen._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if 't' in keycode and "shift" in modifiers and "ctrl" in modifiers:
            appRoot = MDApp.get_running_app().root
            self.printTree(appRoot)


    def printTree(self, widget:Widget, indent = "", marker = "", isLast = True, isRoot = True):
        print(indent + marker + widget.__class__.__name__)

        if not isRoot:
            indent += "   " if isLast else "│  "

        try:
            lastChild = widget.children[-1]
        except:
            lastChild = None

        for i in widget.children:
            self.printTree(i, indent, "└──" if i == lastChild else "├──", i == lastChild, False)


if __name__ == '__main__':
    TestApp().run()
    recipeDB.Close()