from kivy.uix.screenmanager import Screen
from Recipies import fuzzy_recipe_search
from kivymd.uix.list import OneLineListItem
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class SearchRecipeScreen(Screen):
    listItems = []
    popupPane = None

    def show_details(self, instance):
        # TODO create and display a popup to show the recipe
        
        # Create a layout for the popup because popup can only contain one widget
        layout = BoxLayout(orientation="vertical")

        # Create the lable for the popup
        label = Label(text = 'The code nessisary to populate the recipe')

        # Create the Close Button and then bind it to the close details function
        CloseButton = Button(text = "nvm")
        CloseButton.bind(on_release = self.close_details)

        # Add the label and button to the box layout
        layout.add_widget(label)
        layout.add_widget(CloseButton)

        # Create the popup window passing in the above layout as the content
        popup = Popup(title = 'Recipe',
                      content = layout,
                      size_hint = (None, None),
                      size = (self.height, self.width),
                      )

        # Save a reference to the popup so that it can be easily closed later                      
        self.popupPane = popup

        # Open the popup window
        popup.open()

    # close the recipe details popup
    def close_details(self, instance):
        self.popupPane.dismiss()

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
            listItem.bind(on_release = lambda instance : self.show_details(instance))
            list.add_widget(listItem)
            self.listItems.append(listItem)
            
            label_count += 1
            if label_count >= 100: break