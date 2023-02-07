from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import json

class GroceryListScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mainLayout = BoxLayout(orientation="vertical")
        self.add_widget(mainLayout)

        with open("GroceryFiles\\json\\groceryLists.json", 'r') as infile:
            lists = json.load(infile)

        # create a dropdown menu
        dropdown = DropDown()
        for listName in lists:
            btn = Button(text=listName, size_hint_y=None, height=35)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        # create a big main button
        mainbutton = Button(text='Saved Lists', size_hint=(1, None), height=40)
        mainbutton.bind(on_release=dropdown.open)
        
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        mainLayout.add_widget(mainbutton)

        groceryItemBox = BoxLayout(orientation="vertical")
        mainLayout.add_widget(groceryItemBox)
        
        mainLayout.add_widget(Button(text="New List", size_hint=(1, None), height=40))

        
