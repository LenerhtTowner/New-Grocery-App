import json
import JsonUtils
from JsonUtils import JsonFiles
from kivy.uix.popup import Popup

class CreateNewGroceryList(Popup):

    def __init__(self, **kwargs):
        super().__init__()

        if "recipe" in kwargs:
            self.recipe = kwargs['recipe']
        else:
            self.recipe = None
    

    def addNewListToJson(self, textInput):
        newListName = textInput.text

        if self.recipe != None:
            newList = {self.recipe.GetName(): self.recipe.ToDict()}
        else:
            newList = {}

        success = JsonUtils.AppendToJson(newListName, newList, JsonFiles.GROCERY_LISTS, False)
