#Grocery app
import math

from Recipies import *

with open("gramList.json", 'r') as gramFile:
    # gram conversion for each relevant item
    gram_list = json.load(gramFile)

with open("literlist.json", 'r') as literFile:
    # liter conversion for each relevant item
    liter_list = json.load(literFile)

with open("unitItem.json", 'r') as unitFile:
    # unit conversion for each relevant item
    unit_items = json.load(unitFile)

with open("wholeList.json", 'r') as wholeFile:
    # whole conversion for each relevant item
    whole_list = json.load(wholeFile)


class Grocery_Item:
    def __init__(self, amount:int, name:str):
        self.__amount = amount
        self.__name = name

    def __str__(self):
        return "{0} {1}".format(self.__amount, self.__name)


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
    for ingredient in recipe._Recipe__ingredients:
        nextIngr = convert_to_g_L(ingredient, mult)

        # check to see if this ingredient is already in the list
        for ingr in ingredient_list:
            if ingr._Ingredient__name == nextIngr._Ingredient__name:
                # the ingredient already exists so add it to the existing item
                ingr._Ingredient__amount += nextIngr._Ingredient__amount
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
    if ingredient._Ingredient__name in gram_list:
        converted_measure = ingredient._Ingredient__amount * multi * gram_list[ingredient._Ingredient__name][ingredient._Ingredient__unit]
        converted_unit = "grams"
    elif ingredient._Ingredient__name in liter_list:
        converted_measure = ingredient._Ingredient__amount * multi * liter_list[ingredient._Ingredient__name][ingredient._Ingredient__unit]
        converted_unit = "liters"
    else:
        converted_measure = ingredient._Ingredient__amount * multi * whole_list[ingredient._Ingredient__name][ingredient._Ingredient__unit]
        converted_unit = ingredient._Ingredient__unit

    # create a new ingredient item based on the new unit and measure
    converted_ingredient = Ingredient(converted_measure, converted_unit, ingredient._Ingredient__name)
    return (converted_ingredient)


def unit_item_calc(groceryList):
    newList = []
    for ingr in groceryList:
        if ingr == None:
            continue
        if ingr._Ingredient__name in unit_items:
            newList.append(Grocery_Item(math.ceil(ingr._Ingredient__amount / unit_items[ingr._Ingredient__name]), ingr._Ingredient__name))

    return newList

if __name__ == "__main__":
    main()