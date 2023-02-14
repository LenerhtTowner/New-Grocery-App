from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from JsonUtils import LoadFromJson
from JsonFiles import JsonFiles
from CreatNewList import CreateNewGroceryList
import JsonUtils

class GroceryListScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mainLayout = BoxLayout(orientation="vertical")
        self.add_widget(mainLayout)

        lists = LoadFromJson(JsonFiles.GROCERY_LISTS)

        # create a dropdown menu
        dropdown = DropDown()
        self.ids["dropdown"] = dropdown
        for listName in lists:
            btn = Button(text=listName, size_hint_y=None, height=35)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        # create a big main button
        mainbutton = Button(text='Saved Lists', size_hint=(1, None), height=40)

        try:
            lists = JsonUtils.LoadFromJson(JsonFiles.GROCERY_LISTS)

            # create a dropdown menu
            dropdown = DropDown()
            self.ids["dropdown"] = dropdown
            for listName in lists:
                btn = Button(text=listName, size_hint_y=None, height=35)
                btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)

            mainbutton.bind(on_release=self.ids.dropdown.open)
            
            dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        except:
            pass

        mainLayout.add_widget(mainbutton)

        groceryItemBox = BoxLayout(orientation="vertical")
        mainLayout.add_widget(groceryItemBox)

        newListButton = Button(text="New List", size_hint=(1, None), height=40)
        mainLayout.add_widget(newListButton)

        createListPopup = CreateNewGroceryList()
        self.ids["createListPopup"] = createListPopup
        
        newListButton.bind(on_release=self.ids.createListPopup.open)
