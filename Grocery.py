#Grocery app
import math

class Ingredient:
    def __init__(self, amount:float, unit:str, name:str):
        self.amount = amount
        self.unit = unit
        self.name = name

    def __str__(self):
        return "{0} {1} {2}".format(self.amount, self.unit, self.name)

class Grocery_Item:
    def __init__(self, amount:int, name:str):
        self.amount = amount
        self.name = name

    def __str__(self):
        return "{0} {1}".format(self.amount, self.name)

class Recipe:
    def __init__(self, name:str, ingredients:Ingredient):
        self.name = name
        self.ingredients = ingredients

    def __repr__():
        return "Recipe()"

    def __str__(self):
        return self.name

recipes = {
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
}

unit_items = {
    "all-purpose flour":2267.962, 
    "baking powder":230, 
    "salt":737, 
    "milk":3.78, 
    "butter":454, 
    "egg":12, 
    'olive oil':.504, 
    'cheddar':907.185, 
    "cream":907.185, 
    'spinach':311.845, 
    'chicken stock':1, 
    "garlic":1, 
    'onion':1, 
    'potato':1
}

gram_list = {
    "all-purpose flour":{"cup":120, 'tbs':7.8, 'tsp':2.6, 'gram':1}, 
    "baking powder":{"cup":220.8, 'tbs':13.8, 'tsp':4, 'gram':1}, 
    "salt":{"cup":273, 'tbs':17.06, 'tsp':7, 'gram':1}, 
    "butter":{"cup":227, 'tbs':14, 'tsp':4.7, 'gram':1}, 
    'spinach':{"cup":30.0467060355, 'gram':1}, 
    'cheddar':{"cup":120, 'gram':1}
}

liter_list = {
    "milk":{"cup":.236588, 'tbs':.0147868, 'tsp':.00492892, 'ml':.001, 'liter':1}, 
    'chicken stock':{'cup':0.236588, 'tbs':0.0147868, 'tsp':0.00492892, 'ml':.001, 'liter':1}, 
    'cream':{'cup':0.236588, 'tbs':0.0147868, 'tsp':0.00492892, 'ml':.001, 'liter':1}, 
    'olive oil':{'cup':0.236588, 'tbs':0.0147868, 'tsp':0.00492892, 'ml':.001, 'liter':1}
}

whole_list = {
    "egg": {"carton": 12, "whole": 1}, 
    'garlic':{'whole':1, "bulb":1, 'clove':1}, 
    "onion":{'whole': 1}, 
    'broccoli':{"head": 1, 'whole':1}, 
    'potato':{'whole':1}
}

selected_recipes = []
ingredient_list = []
shopping_list = []


def main():
    # this section of code will repeat until the user is done selecting recipes
    while True:
        choice = Get_Recipe_Choice()

        # we only get here if the user did not make a recipe selection int Get_Recipe_Choice()
        # so we should be done getting recipes, break out of the loop
        if choice == None:
            break
        
        #extract the selected recipe from the dictionary
        newRecipe = recipes[choice]

        # TODO this is unreliable, should enforce integer input
        multi = int(input("How many times will you make this meal? ")) 

        # For each ingredient in the recipe we add it to the list if it's new
        # otherwise we add it's ammount to whatever already exists
        Add_Recipe_To_Ingredient_List(newRecipe, multi)
        
        confirm = input('Add another recipe? [y] or [n] ')
        if confirm != 'y' and confirm != 'yes':
            break

    # convert all ingredients to grocery items
    # their ammounts are expressed in grams, liters, or wholes
    shopping_list = unit_item_calc(ingredient_list)

    for item in shopping_list:
        print(item)


def Get_Recipe_Choice():
    while True:
        choice = input('Which recipes do you want to shop for: ')

        if choice not in recipes.keys():
            print("'" + choice + "' was not a valid selection.")
            confirm = input('Add another? [y] or [n] ')

            if confirm.lower() != "y" and confirm.lower() != "yes":
                choice = None
                break
        else:
            break

    return choice


def Add_Recipe_To_Ingredient_List(recipe, mult):
    for ingredient in recipe.ingredients:
        nextIngr = convert_to_g_L(ingredient, mult)

        # check to see if this ingredient is already in the list
        for ingr in ingredient_list:
            if ingr.name == nextIngr.name:
                # the ingredient already exists so add it to the existing item
                ingr.amount += nextIngr.amount
                nextIngr = None
                break

        # if the item was found previously it will be null now
        # otherwise add it to the list
        if nextIngr != None:
            ingredient_list.append(nextIngr)


def convert_to_g_L(ingredient, multi = 1):
    converted_ingredient = None
    converted_measure = 0
    converted_unit = ""

    # calculate converted measure and new unit based on the type of unit used
    if ingredient.name in gram_list:
        converted_measure = ingredient.amount * multi * gram_list[ingredient.name][ingredient.unit]
        converted_unit = "grams"
    elif ingredient.name in liter_list:
        converted_measure = ingredient.amount * multi * liter_list[ingredient.name][ingredient.unit]
        converted_unit = "liters"
    else:
        converted_measure = ingredient.amount * multi * whole_list[ingredient.name][ingredient.unit]
        converted_unit = ingredient.unit

    # create a new ingredient item based on the new unit and measure
    converted_ingredient = Ingredient(converted_measure, converted_unit, ingredient.name)
    return (converted_ingredient)


def unit_item_calc(groceryList):
    newList = []
    for ingr in groceryList:
        if ingr == None:
            continue
        if ingr.name in unit_items:
            newList.append(Grocery_Item(math.ceil(ingr.amount / unit_items[ingr.name]), ingr.name))

    return newList

if __name__ == "__main__":
    main()