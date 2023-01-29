from kivy.uix.screenmanager import Screen
from RecipeDB import recipeDB
from kivymd.uix.list import OneLineListItem
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
import JsonUtils

class test():
    def printstuff(self, instance):
        pass

class SearchRecipeScreen(Screen):
    test = test()
    listItems = []
    popupPane = None
    WidgetToID = {}
    selectedRecipe = None

    def addToLocal(self, instance):
        JsonUtils.AddRecipeToJson(self.selectedRecipe)
        self.popupPane.dismiss()
    
    def show_details(self, instance):
        # TODO create and display a popup to show the recipe
        self.selectedRecipe = recipeDB.FetchRecipe_ID(self.WidgetToID[instance])

        recipeStr = ''

        for ing in self.selectedRecipe.GetIngredients():
            if recipeStr != "": recipeStr += "\n"
            recipeStr += f"{ing.GetAmount()} {ing.GetUnit()} {ing.GetName()}"

        # Create a layout for the popup because popup can only contain one widget
        layout = GridLayout(cols = 1)
        buttonLayout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=30)
        # Create the lable for the popup
        label = Label(text=recipeStr)
        label.padding_y = 16

        # Create the Close Button and then bind it to the close details function
        AddButton = Button(text = "add",
                             size_hint = (None, None),
                             size = (90, 30),
                            )
        
        CloseButton = Button(text = "nvm",
                             size_hint = (None, None),
                             size = (90, 30),
                            )
                            
        CloseButton.bind(on_release = self.close_details)
        AddButton.bind(on_release = self.addToLocal)

        buttonLayout.add_widget(CloseButton)
        buttonLayout.add_widget(AddButton)

        # Add the label and button to the box layout
        layout.add_widget(label)
        layout.add_widget(buttonLayout)

        # Create the popup window passing in the above layout as the content
        popup = Popup(title = instance.text,
                      content = layout,
                      size_hint = (1, None),
                      height = self.width
                      )

        # Save a reference to the popup so that it can be easily closed later                      
        self.popupPane = popup

        # Open the popup window
        self.popupPane.open()

    # close the recipe details popup
    def close_details(self, instance):
        self.popupPane.dismiss()
        self.popupPane = None

    def search_Rsql(self, searchStr):
        recipe_matches = recipeDB.FuzzyRecipeSearch(searchStr)
        list = self.ids.recipe_list

        for i in self.listItems:
            list.remove_widget(i)
        listItem = []

        label_count = 0
        for match in recipe_matches:
            listItem = OneLineListItem(text=match)
            listItem.text_color = (1, 1, 1, 1)
            listItem.background_color = (0, 0, 0, 1)
            listItem.bind(on_release = lambda instance : self.show_details(instance))
            list.add_widget(listItem)
            self.listItems.append(listItem)
            self.ids[recipe_matches[match]] = listItem
            self.WidgetToID[listItem] = recipe_matches[match]
            
            label_count += 1
            if label_count >= 100: break