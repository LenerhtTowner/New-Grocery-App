from kivy.uix.screenmanager import Screen
from Recipies import fetch_recipe_ID
from Recipies import Ingredient
from Recipies import Grocery_Item
from math import ceil
import json

class RecipeScreen(Screen):
    selected_recipes = []
    ingredient_dict = {}
    shopping_list = []
    gram_list = {}
    liter_list = {}
    unit_items = {}
    whole_list = {}

    def __init__(self, name):
        super().__init__(name=name)
        self.InitJson("./GroceryFiles/gramList.json", self.gram_list)
        self.InitJson("./GroceryFiles/literList.json", self.liter_list)
        self.InitJson("./GroceryFiles/unitItem.json", self.unit_items)
        self.InitJson("./GroceryFiles/wholeList.json", self.whole_list)

    def InitJson(self, filePath, dictionary):
        with open(filePath, 'r') as file:
            # whole conversion for each relevant item
            dictionary = json.load(file)

    def UpdateCount(self, instance, recipeName:str, recipeCount:str, value:bool):
        if recipeCount == '' or not recipeCount.isnumeric():
            instance.text = None

        if value:
            self.GetRecipe(recipeName, recipeCount, value)

    def GetRecipe(self, recipeID:int, recipeCount:str, value:bool):
        count = int(recipeCount)
        recipe = fetch_recipe_ID(recipeID)
        
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
                newList.append(Grocery_Item(ceil(ingr.GetAmount() / self.unit_items[ingr.GetName()]), ingr.GetName()))

        return newList