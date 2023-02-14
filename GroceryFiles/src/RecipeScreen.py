from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from RecipeDB import recipeDB, Ingredient, Grocery_Item
from StubClasses import RecipeListItem, RecipeDataPanel
from JsonFiles import JsonFiles
import JsonUtils
from math import ceil
from kivy.clock import Clock

class RecipeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gram_list  = self.LoadJson(JsonFiles.GRAM_LIST)
        self.liter_list = self.LoadJson(JsonFiles.LITER_LIST)
        self.unit_items = self.LoadJson(JsonFiles.UNIT_ITEM)
        self.whole_list = self.LoadJson(JsonFiles.WHOLE_LIST)
        self.ingredient_dict = {}
        self.shopping_list = []
        Clock.schedule_once(self.LoadLocalRecipes, 0)


    def adjustLabelTextWidth(self, instance):
        instance.text_size = (instance.width, instance.text_size[1])


    def adjustLabelHeight(self, instance):
        instance.height = instance.texture_size[1]
 

    def wrapText(self, instance, *args):
        print(args)
        instance.text_size = (instance.width, None)
        instance.size_hint=(1, None)
        instance.height = instance.texture_size[1]


    def ShowSelectedRecipe(self, instance:Widget, recipeName):
        recipe = recipeDB.FetchRecipe_Name(recipeName)

        popup = Popup(title=recipe.GetName(), title_size="30dp")

        content = BoxLayout(orientation="vertical")
        popup.content = content

        recipeDataPanel = RecipeDataPanel()
        content.add_widget(recipeDataPanel)
        # add ingredient List
        for i, ing in enumerate(recipe.GetIngredients()):
            recipeDataPanel.ids.IngredientLabel.text += "\u2022 " + str(ing) + "\n"

        # add method
        recipeDataPanel.ids.MethodLabel.text=recipe.GetMethod()

        # add button to close popup
        testButton = Button(text="test", size_hint=(1, None), height=60)
        testButton.bind(on_release=popup.dismiss)
        content.add_widget(testButton)
        
        popup.open()


    def ResetRecipes(self, *args):
        self.ClearRecipes()
        self.LoadLocalRecipes()


    def ClearRecipes(self, *args):
        self.ids.RecipeScreenBox.clear_widgets()


    def LoadLocalRecipes(self, *args):
        recipes = JsonUtils.LoadRecipesFromJson()
        
        for i, recipe in enumerate(recipes):
            li = RecipeListItem()
            li.ids.recipe_label.text = f"[ref={recipe}]{recipe}[/ref]"
            li.ids.recipe_label.bind(on_ref_press = self.ShowSelectedRecipe)
            #li.ids.recipe_check.bind(active = self.ShowSelectedRecipe)
            self.ids.RecipeScreenBox.add_widget(li)
            
        self.ids.RecipeScreenBox.add_widget(BoxLayout())
        

    def SetMinimumHeight(self, instance, *args):
        instance.height = instance.minimum_height
    

    def RemoveFromLocal(self, instance):
        JsonUtils.DeleteFromJson(self.selectedRecipe.GetName(), JsonFiles.RECIPES)
        self.popupPane.dismiss()
    

    def LoadJson(self, file_name: str) -> dict:
        return JsonUtils.LoadFromJson(file_name)


    def OnUpdateCount(self, instance:Widget, recipeName:str, recipeCount:str, value:bool):
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