from kivy.uix.screenmanager import Screen
from Recipies import fuzzy_recipe_search
from kivymd.uix.list import OneLineListItem

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