# inventoryscreen.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen



class InventoryScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        # Create a layout for the inventory screen
        inventory_layout = BoxLayout(orientation='vertical')

        button_grid = GridLayout(cols=2, size_hint=(1, None), height=100)

        # Add widgets or layout for the inventory screen
        self.add_widget(Label(text='Inventory Items'))
        self.add_widget(button_grid)
        back_button = Button(text='Back')
        back_button.bind(on_press=self.go_to_main_screen)

        # Add buttons to the grid layout
        button_grid.add_widget(back_button)

    def go_to_main_screen(self, instance):
        self.screen_manager.current = 'main'
