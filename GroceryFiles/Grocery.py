# COMPLETED - TODO-Add functionality to allow app to add multiple recipes ingradients.(Priority 1)
# TODO-Create Screen for Recipe entry(too include asking the user to find iten weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.
    #Create def(s) for converting user recipes into local recipes
# TODO-Creat functionality to allow user to add recipes to a JSON file for local use.(Pri 2)
    #SUB-TASKS TBD
# TODO-Create functionality for dynamic widget generation.(Pri 3)
###ROBERT'S NOTES TO ETHAN
### Completed the first TODO on lines 77 - 86
###ETHAN'S NOTES TO ROBERT
###

from kivy.factory import Factory
from kivy.app import App
from kivy.uix.widget import Widget 
from kivy.properties import ObjectProperty 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.garden.moretransitions import PixelTransition,RippleTransition,BlurTransition,RVBTransition
from kivy.uix.gridlayout import GridLayout
import math
from math import sqrt

from Recipies import *

class IngredientInfo(GridLayout):
    pass

class Grocery_Item:
    def __init__(self, amount:int, name:str):
        self.__amount = amount
        self.__name = name

    def __str__(self):
        return "{0} {1}".format(self.__amount, self.__name)

class RecipeScreen(Screen):
    selected_recipes = []
    ingredient_dict = {}
    shopping_list = []


    with open("./GroceryFiles/gramList.json", 'r') as gramFile:
        # gram conversion for each relevant item
        gram_list = json.load(gramFile)

    with open("./GroceryFiles/literlist.json", 'r') as literFile:
        # liter conversion for each relevant item
        liter_list = json.load(literFile)

    with open("./GroceryFiles/unitItem.json", 'r') as unitFile:
        # unit conversion for each relevant item
        unit_items = json.load(unitFile)

    with open("./GroceryFiles/wholeList.json", 'r') as wholeFile:
        # whole conversion for each relevant item
        whole_list = json.load(wholeFile) 
        
    
    def UpdateCount(self, instance, recipeName:str, recipeCount:str, value:bool):
        if recipeCount == '' or not recipeCount.isnumeric():
            instance.text = None

        if value:
            self.GetRecipe(recipeName, recipeCount, value)

    def GetRecipe(self, recipeName:str, recipeCount:str, value:bool):
        count = int(recipeCount)
        recipe = recipes[recipeName]
        
        if not value:
            count = 0
        
        self.Add_Recipe_To_Ingredient_List(recipe, count)

        shopping_list = []
        shoppingListText = ''

        for i in self.ingredient_dict.keys():
            shopping_list += self.unit_item_calc(self.ingredient_dict[i])
        
        for i in shopping_list:
            shoppingListText += str(i) + "\n"
            
        self.ids.Recipe_List.text = shoppingListText
        
        
    def Add_Recipe_To_Ingredient_List(self, recipe, mult):
        self.ingredient_dict[recipe.GetName()] = []
        for ingredient in recipe.GetIngredients():
            nextIngr = self.convert_to_g_L(ingredient, mult)

            # check to see if this ingredient is already in the list
            for ingr in self.ingredient_dict[recipe.GetName()]:
                if ingr.GetName() == nextIngr.GetName():
                    # the ingredient already exists so add it to the existing item
                    ingr.Add(nextIngr.GetAmount())
                    nextIngr = None
                    break

            # if the item was found previously it will be null now
            # otherwise add it to the list
            if nextIngr != None and nextIngr.GetAmount() > 0:
                self.ingredient_dict[recipe.GetName()].append(nextIngr)


    def convert_to_g_L(self, ingredient, multi = 1):
        converted_ingredient = None
        converted_measure = 0
        converted_unit = ""

        # calculate converted measure and new unit based on the type of unit used
        if ingredient.GetName() in self.gram_list:
            converted_measure = ingredient.GetAmount() * multi * self.gram_list[ingredient.GetName()][ingredient.GetUnit()]
            converted_unit = "grams"
        elif ingredient.GetName() in self.liter_list:
            converted_measure = ingredient.GetAmount() * multi * self.liter_list[ingredient.GetName()][ingredient.GetUnit()]
            converted_unit = "liters"
        else:
            converted_measure = ingredient.GetAmount() * multi * self.whole_list[ingredient.GetName()][ingredient.GetUnit()]
            converted_unit = ingredient.GetUnit()

        # create a new ingredient item based on the new unit and measure
        converted_ingredient = Ingredient(converted_measure, converted_unit, ingredient.GetName())
        return (converted_ingredient)


    def unit_item_calc(self, groceryList):
        newList = []
        for ingr in groceryList:
            if ingr == None:
                continue
            if ingr.GetName() in self.unit_items:
                newList.append(Grocery_Item(math.ceil(ingr.GetAmount() / self.unit_items[ingr.GetName()]), ingr.GetName()))

        return newList

class NewRecipeScreen(Screen):
    pass

kv = Builder.load_file("grocerykivy.kv")

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm = ScreenManager(transition=RVBTransition())
        sm.add_widget(RecipeScreen(name='Recipe'))
        sm.add_widget(NewRecipeScreen(name='NewRecipe'))

        return sm

if __name__ == '__main__':
    TestApp().run()
    
    
        # def main():
    #     # this section of code will repeat until the user is done selecting recipes
    #     while True:
    #         choice = Get_Recipe_Choice()

    #         # we only get here if the user did not make a recipe selection int Get_Recipe_Choice()
    #         # so we should be done getting recipes, break out of the loop
    #         if choice == None:
    #             break
            
    #         #extract the selected recipe from the dictionary
    #         newRecipe = recipes[choice]

    #         # TODO this is unreliable, should enforce integer input
    #         multi = int(input("How many times will you make this meal? ")) 

    #         # For each ingredient in the recipe we add it to the list if it's new
    #         # otherwise we add it's ammount to whatever already exists
    #         Add_Recipe_To_Ingredient_List(newRecipe, multi)
            
    #         confirm = input('Add another recipe? [y] or [n] ')
    #         if confirm != 'y' and confirm != 'yes':
    #             break

    #     # convert all ingredients to grocery items
    #     # their ammounts are expressed in grams, liters, or wholes
    #     shopping_list = unit_item_calc(ingredient_list)

    #     for item in shopping_list:
    #         print(item)


    # def Get_Recipe_Choice():
    #     while True:
    #         choice = input('Which recipes do you want to shop for: ')

    #         if choice not in recipes.keys():
    #             print("'" + choice + "' was not a valid selection.")
    #             confirm = input('Add another? [y] or [n] ')

    #             if confirm.lower() != "y" and confirm.lower() != "yes":
    #                 choice = None
    #                 break
    #         else:
    #             break

    #     return choice