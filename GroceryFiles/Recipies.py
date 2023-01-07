import json
from json import JSONEncoder
import pickle


class Ingredient:
    def __init__(self, amount:float, unit:str, name:str):
        self.__name = name
        self.__amount = amount
        self.__unit = unit

    def __str__(self):
        return "{0} {1} {2}".format(round(self.__amount, 2), self.__unit, self.__name)
    
    def GetName(self):
        return self.__name
    
    def GetAmount(self):
        return self.__amount
    
    def Add(self, amount):
        self.__amount += amount
    
    def GetUnit(self):
        return self.__unit


class Recipe:
    def __init__(self, name:str, ingredients:Ingredient):
        self.__name = name
        self.__ingredients = ingredients
        
    def GetName(self):
        return self.__name
    
    def GetIngredients(self):
        return self.__ingredients

    def ToDict(self):
        jsonData = {'name': self.__name, '__ingredients': []}
        for ing in self.__ingredients:
            jsonData['__ingredients'].append(ing.__dict__)

        return jsonData

    def __repr__():
        return "Recipe()"

    def __str__(self):
        return self.__name


def EncodeRecipesToJson():
    with open('./venv/recipes.json', 'w') as outfile:
        recipeData = {}

        for key in recipes.keys():
            recipeData[key] = recipes[key].ToDict()
            
        json.dump(recipeData, outfile, indent=4)


def LoadRecipesFromJson():
    newRecipeDict = {}
    recipeData = None
    with open('./GroceryFiles/recipes.json', 'r') as inFile:
        recipeData = json.load(inFile)
        
        if recipeData == None:
            return None

    for key in recipeData.keys():
        recipeName = recipeData[key]['__name']
        __ingredients = []

        for ing in recipeData[key]['__ingredients']:
            __ingredients.append(Ingredient(ing['__amount'], ing['__unit'], ing['__name']))

        newRecipeDict[key] = Recipe(recipeName, __ingredients)

    return newRecipeDict


#EncodeRecipesToJson()
recipes = LoadRecipesFromJson()

