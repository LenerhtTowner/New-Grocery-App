import json
from RecipeDB import Ingredient, Recipe

def AddRecipeToJson(recipe:Recipe):
    recipeData = {}
    with open('./GroceryFiles/json/recipes.json', 'r') as infile:
        try:
            recipeData = json.load(infile)
        except:
            pass
            
    with open('./GroceryFiles/json/recipes.json', 'w') as outfile:
        recipeData[recipe.GetName()] = recipe.ToDict()
        json.dump(recipeData, outfile, indent=4)
        LoadRecipesFromJson()

def DeleteRecipeFromJson(recipe_name:str):
    recipeData = {}
    with open('./GroceryFiles/json/recipes.json', 'r') as infile:
        try:
            recipeData = json.load(infile)
        except:
            return
    
    with open('./GroceryFiles/json/recipes.json', 'w') as outfile:
        try:
            del recipeData[recipe_name]
        except:
            pass
        
        json.dump(recipeData, outfile, indent=4)

def EncodeRecipesToJson():
    with open('GroceryFiles/json/recipes.json', 'w') as outfile:
        recipeData = {}

        for key in recipes.keys():
            recipeData[key] = recipes[key].ToDict()
            
        json.dump(recipeData, outfile, indent=4)


def LoadRecipesFromJson(filepath = 'GroceryFiles/json/recipes.json'):
    newRecipeDict = {}
    recipeData = None
    with open(filepath, 'r') as inFile:
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