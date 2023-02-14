import json
from RecipeDB import Ingredient, Recipe
from JsonFiles import JsonFiles

jsonDirectory = "./GroceryFiles/json/"


def AppendToJson(key:str, value:dict, jsonFilename:str, overwrite=True):
    try:
        with open(jsonDirectory + jsonFilename, "r") as infile:
            jsonData = json.load(infile)
    except:
        jsonData = {}

    if not overwrite and key in jsonData:
        pass
    else:
        jsonData[key] = value

    try:
        with open(jsonDirectory + jsonFilename, "w") as outfile:
            json.dump(jsonData, outfile, indent=4)

        return True
    except:
        return False


def DeleteFromJson(key:str, jsonFilename:str):
    try:
        with open(jsonDirectory + jsonFilename, "r") as infile:
            jsonData = json.load(infile)
    except:
        jsonData = {}

    if key in jsonData:
        del jsonData[key]

    try:
        with open(jsonDirectory + jsonFilename, "w") as outfile:
            json.dump(jsonData, outfile, indent=4)

        return True
    except:
        return False


def LoadFromJson(jsonFilename:str):
    try:
        with open(jsonDirectory + jsonFilename, "r") as infile:
            result = json.load(infile)
        return result
    except IOError as e:
        print(e)

    return {}


def LoadRecipesFromJson():
    newRecipeDict = {}
    recipeData = None
    with open(jsonDirectory + JsonFiles.RECIPES, 'r') as inFile:
        try:
            recipeData = json.load(inFile)
        except:
            return {}
        
        if recipeData == None:
            return None

    for key in recipeData.keys():
        recipeName = recipeData[key]['__name']
        ingredients = []

        for ing in recipeData[key]['__ingredients']:
            if ing['_Ingredient__amount'] == '':
                ing['_Ingredient__amount'] = 0
            ingredients.append(Ingredient(ing['_Ingredient__amount'], ing['_Ingredient__unit'], ing['_Ingredient__name']))

        recipeMethod = recipeData[key]['__method']

        newRecipeDict[key] = Recipe(recipeName, ingredients, recipeMethod)
    return newRecipeDict