from kivy.uix.screenmanager import Screen
from Recipies import fuzzy_recipe_search
from kivymd.uix.list import OneLineListItem
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
from kivy.uix.button import Button

class SearchRecipeScreen(Screen):
    listItems = []

    def show_details(self, instance):
        # TODO create and display a popup to show the recipe
        
        # Create the popup window(Button Doesn't work right. Cant get the dismiss function to work)
        popup = Popup(title = 'Recipe',
                      content = Label(text = 'The code nessisary to populate the recipe'),
                      size_hint = (None, None), size = (self.height, self.width),
                      CloseButton = Button(text = "nvm"), CloseButton.bind(on_release = popup.dismiss))

        # Open the popup window
        popup.open()
        
        # CloseButton.bind(on_release = popup.dismiss)

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