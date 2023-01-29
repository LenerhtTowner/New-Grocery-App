from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from RecipeDB import recipeDB
from RecipeDB import Ingredient
from RecipeDB import Grocery_Item
from StubClasses import RecipeListItem
from math import ceil
from kivy.clock import Clock
import json
import JsonUtils

class RecipeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.gram_list = self.LoadJson("GroceryFiles/json/gramList.json")
        self.liter_list = self.LoadJson("GroceryFiles/json/literList.json")
        self.unit_items = self.LoadJson("GroceryFiles/json/unitItem.json")
        self.whole_list = self.LoadJson("GroceryFiles/json/wholeList.json")
        self.ingredient_dict = {}
        self.shopping_list = []
        Clock.schedule_once(self.loadLocalRecipes, 0)

    def loadLocalRecipes(self, *args):
        recipes = JsonUtils.recipes
        
        for i, recipe in enumerate(recipes):
            li = RecipeListItem()
            li.ids.recipe_label.text = recipe
            self.ids.RecipeScreenBox.add_widget(li)
            # boxlayout = BoxLayout(orientation = "horizontal", size_hint=(1, None))
            # boxlayout.bind(on_height=self.adjustHeight)
            # label = Label(text = recipes[recipe].GetName())
            # checkbox = CheckBox()
            # button = Button(text = "Bin it!", size_hint=(None, None), size=(60,30))
            # self.ids.RecipeScreenBox.add_widget(boxlayout)
            # boxlayout.add_widget(label)
            # boxlayout.add_widget(checkbox)
            # boxlayout.add_widget(button)
        
            # button.bind(on_release=lambda a : JsonUtils.DeleteRecipeFromJson(label.text))
            
        self.ids.RecipeScreenBox.add_widget(BoxLayout())
        
    def adjustHeight(self, instance):
        instance.height = instance.minimum_height
    
    def removeFromLocal(self, instance):
        JsonUtils.removeFromJson(self.selectedRecipe.GetName())
        self.popupPane.dismiss()
    
    def LoadJson(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    def OnUpdateCount(self, instance, recipeName:str, recipeCount:str, value:bool):
        if recipeCount == '' or not recipeCount.isnumeric():
            instance.text = None

        if value:
            self.GetRecipe(recipeName, recipeCount, value)

    def GetRecipe(self, recipeID:int, recipeCount:str, value:bool):
        count = int(recipeCount)
        recipe = recipeDB.FetchRecipe_ID(recipeID)
        
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
            if nextIngr != None and float(nextIngr.GetAmount()) > 0:
                self.ingredient_dict[recipe.GetName()].append(nextIngr)
 

    def convert_to_g_L(self, ingredient, multi = 1):
        converted_ingredient = None
        converted_measure = 0
        converted_unit = ""

        # calculate converted measure and new unit based on the type of unit used
        if ingredient.GetName() in self.gram_list:
            try:
                converted_measure = ingredient.GetAmount() * multi * self.gram_list[ingredient.GetName()][ingredient.GetUnit()]
                converted_unit = "grams"
            except:
                converted_measure = ingredient.GetAmount()
                converted_unit = ingredient.GetUnit()
        elif ingredient.GetName() in self.liter_list:
            try:
                converted_measure = ingredient.GetAmount() * multi * self.liter_list[ingredient.GetName()][ingredient.GetUnit()]
                converted_unit = "liters"
            except:
                converted_measure = ingredient.GetAmount()
                converted_unit = ingredient.GetUnit()
        else:
            try:
                converted_measure = ingredient.GetAmount() * multi * self.whole_list[ingredient.GetName()][ingredient.GetUnit()]
                converted_unit = ingredient.GetUnit()
            except:
                converted_measure = ceil(ingredient.GetAmount())
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