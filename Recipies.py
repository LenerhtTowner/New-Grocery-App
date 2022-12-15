import json
from json import JSONEncoder
import pickle


class Ingredient:
    def __init__(self, amount:float, unit:str, name:str):
        self.name = name
        self.amount = amount
        self.unit = unit

    def __str__(self):
        return "{0} {1} {2}".format(self.amount, self.unit, self.name)


class Recipe:
    def __init__(self, name:str, ingredients:Ingredient):
        self.name = name
        self.ingredients = ingredients

    def ToDict(self):
        jsonData = {'name': self.name, 'ingredients': []}
        for ing in self.ingredients:
            jsonData['ingredients'].append(ing.__dict__)

        return jsonData

    def __repr__():
        return "Recipe()"

    def __str__(self):
        return self.name


'''recipes = {
    "pancakes" : Recipe
    (
        "pancakes", 
        [
            Ingredient(1.5, "cup", "all-purpose flour"),
            Ingredient(3.5, 'tbs', 'baking powder'),
            Ingredient(.25, 'tsp', 'salt'),
            Ingredient(1.25, 'cup', 'milk'),
            Ingredient(3, 'tbs', 'butter'),
            Ingredient(1, 'whole', 'egg')
        ]
    ),

    "broccoli cheddar soup":Recipe
    (
        "broccoli cheddar soup",
        [
            Ingredient(1, 'whole', 'onion'),
            Ingredient(3, 'clove', 'garlic'),
            Ingredient(1, 'whole', 'potato'),
            Ingredient(1, 'whole', 'broccoli'),
            Ingredient(200, 'gram', 'spinach'),
            Ingredient(1, 'liter', 'chicken stock'),
            Ingredient(100, "ml", 'cream'),
            Ingredient(400, 'gram', 'cheddar'),
            Ingredient(2, 'tbs', 'olive oil')
        ]
    )
}'''


def PickelRecipes():
    with open('recipes.dat', 'wb') as outFile:
        for i in recipes.keys():
            pickle.dump(recipes[i], outFile)


def LoadPickledRecipes():
    recipes = {}

    with open('recipes.dat', 'rb') as inFile:
        while True:
            try:
                recipe = pickle.load(inFile)
                recipes[recipe.name] = recipe
            except EOFError:
                break
        return recipes


def EncodeRecipesToJson():
    with open('recipes.json', 'w') as outfile:
        recipeData = {}

        for key in recipes.keys():
            recipeData[key] = recipes[key].ToDict()
            
        json.dump(recipeData, outfile, indent=4)


def LoadRecipesFromJson():
    newRecipeDict = {}
    recipeData = None
    with open('recipes.json', 'r') as inFile:
        recipeData = json.load(inFile)
        
        if recipeData == None:
            return None

    for key in recipeData.keys():
        recipeName = recipeData[key]['name']
        ingredients = []

        for ing in recipeData[key]['ingredients']:
            ingredients.append(Ingredient(ing['amount'], ing['unit'], ing['name']))

        newRecipeDict[key] = Recipe(recipeName, ingredients)

    return newRecipeDict


#EncodeRecipesToJson()
recipes = LoadRecipesFromJson()