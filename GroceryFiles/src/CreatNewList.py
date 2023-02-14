import json
from kivy.uix.popup import Popup

class CreateNewGroceryList(Popup):

    def __init__(self, **kwargs):
        super().__init__()

        if "recipe" in kwargs:
            self.recipe = kwargs['recipe']
        else:
            self.recipe = None
    

    def addNewListToJson(self, textInput):
        newListDict = {}

        with open('GroceryFiles\json\groceryLists.json', 'r') as infile:
            listDict = json.load(infile)

        if self.recipe in listDict:
            pass

        elif self.recipe != None:
            listDict[textInput.text] = {self.recipe.GetName(): self.recipe.ToDict()}
        else:
            listDict[textInput.text] = {}

        with open('GroceryFiles\json\groceryLists.json', 'w') as outfile:
            json.dump(listDict, outfile, indent=4)
