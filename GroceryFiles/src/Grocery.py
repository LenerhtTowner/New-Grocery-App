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

    def build(self):
        main = MainScreen()

        main._keyboard = Window.request_keyboard(self._keyboard_closed, main)
        main._keyboard.bind(on_key_down=self._on_keyboard_down)

        return MainScreen()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

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