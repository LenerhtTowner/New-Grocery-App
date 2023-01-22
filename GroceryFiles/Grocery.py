# COMPLETED - TODO-Add functionality to allow app to add multiple recipes ingredients.(Priority 1)
# TODO-Create Screen for Recipe entry(too include asking the user to find iten weights. It occurs to me that the way to handle liquid measurments is to have a way to tack on the value section of a dictionary to the item, effectivy auto filling the liter measurments.)(Priority 2)
    #Create funcionality for the user to dynamically add widgets for ingredients.
    #Create def(s) for converting user recipes into local recipes
# TODO-Creat functionality to allow user to add recipes to a JSON file for local use.(Pri 2)
    #SUB-TASKS TBD
# TODO-Create functionality for dynamic widget generation.(Pri 3)
'''
ROBERT'S NOTES TO ETHAN
    Completed the first TODO on lines 77 - 86.
    I got all the recipe data into the database.
    The recipes can not currently be retrieved by name.
    Each recipe has an ID number (from 1 to 38156). To fetch a recipe use: fetch_recipe(recipe_id:int)

    example:

        from Recipes import *

        recipe = fetch_recipe(1).ToDict()

        print(recipe['__name'])

        for ingredient in recipe["__ingredients"]:
            print(ingredient)

    result:
        Instant Pot Hamburger Soup
        {'_Ingredient__name': 'ground beef', '_Ingredient__amount': '1.5', '_Ingredient__unit': 'pounds'}
        {'_Ingredient__name': 'onion, finely chopped', '_Ingredient__amount': '1', '_Ingredient__unit': 'medium'}
        {'_Ingredient__name': 'beef consomme', '_Ingredient__amount': '3', '_Ingredient__unit': '(14.5 ounce) cans'}
        {'_Ingredient__name': 'diced tomatoes', '_Ingredient__amount': '1', '_Ingredient__unit': '(28 ounce) can'}
        {'_Ingredient__name': 'water', '_Ingredient__amount': '2', '_Ingredient__unit': 'cups'}
        {'_Ingredient__name': 'condensed tomato soup', '_Ingredient__amount': '1', '_Ingredient__unit': '(10.75 ounce) can '}
        {'_Ingredient__name': 'carrots, finely chopped', '_Ingredient__amount': '4', '_Ingredient__unit': ''}
        {'_Ingredient__name': 'celery, finely chopped', '_Ingredient__amount': '3', '_Ingredient__unit': 'stalks'}
        {'_Ingredient__name': 'pearl barley', '_Ingredient__amount': '4', '_Ingredient__unit': 'tablespoons'}
        {'_Ingredient__name': 'dried thyme', '_Ingredient__amount': '0.5', '_Ingredient__unit': 'teaspoon'}
        {'_Ingredient__name': 'bay leaf', '_Ingredient__amount': '1', '_Ingredient__unit': ''}

ETHAN'S NOTES TO ROBERT

'''

from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.widget import Widget 
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.properties import ObjectProperty 
from kivy.lang import Builder
from kivy.core.window import Window
from math import ceil
from Recipies import *

from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem


Window.size = (600, 900)


class RecipeCarousel(Carousel):
    pass

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

    with open("./GroceryFiles/literList.json", 'r') as literFile:
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

class NewRecipeScreen(Screen):
    pass

class SearchRecipeScreen(Screen):
    listItems = []

    def search_Rsql(self, searchStr):
        recipe_matches = fuzzy_recipe_search(searchStr)
        list = self.ids.recipe_list

        for i in self.listItems:
            list.remove_widget(i)
        listItem = []

        label_count = 0
        for match in recipe_matches:
            listItem = OneLineListItem(text=match)
            listItem.text_color = (1, 1, 1, 1)
            listItem.background_color = (0, 0, 0, 1)
            list.add_widget(listItem)
            self.listItems.append(listItem)
            
            label_count += 1
            if label_count >= 100: break

kv = Builder.load_file("grocerykivy.kv")

class TestApp(MDApp):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(RecipeScreen(name='Recipe'))
        sm.add_widget(NewRecipeScreen(name='NewRecipe'))
        sm.add_widget(SearchRecipeScreen(name='SearchRecipe'))
        
        return sm

if __name__ == '__main__':
    TestApp().run()