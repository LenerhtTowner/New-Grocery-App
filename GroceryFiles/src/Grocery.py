# TODO - **Create Screen for Recipe entry(too include asking the user to find item weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.**
    #Create def(s) for converting user recipes into local recipes.
#TODO - Update the calculation function so that the user can be prompted to enter gram/liter per units, and have that function fill in the data for the rest of the measrues.(i.e. If the user enters an amount per cup the program uses this info to calculate Tbs tsp and so on.)
#TODO - Creat functionality to gather data from the user.
#TODO - Finish dev on getting the users lists to show on screen for review and modification and display the grocery items needed to make those meals.

'''
ROBERT'S NOTES TO ETHAN

ETHAN'S NOTES TO ROBERT
    I have added a pass condition to the 'CreateNewList.py in the event that self.recipe in listDict
    (lines 21 and 22). I removed some of the TODOs above as they are complete. I'll have added new 
    ones as well. If I'm missing anything please add. My intent is to list everything left that we 
    need to send this program to market. 
                                                                                    -Hic Sunt Leones. 
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