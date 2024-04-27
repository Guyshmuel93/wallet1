from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class AnotherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add a label to display text
        self.add_widget(Label(text='Welcome to Another Page'))
        navigate_button = Button(text='Navigate')
        navigate_button.bind(on_press=self.navigate_to_another_page)
    def navigate_to_another_page(self, instance):
        self.root.current = 'another'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from anotherscreen import AnotherScreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()

        # Create the main screen
        main_screen = Screen(name='main')
        main_layout = BoxLayout(orientation='vertical')

        # Create the upper bar
        upper_bar = BoxLayout(size_hint=(1, None), height=50)
        upper_bar.add_widget(Label(text='Upper Bar'))

        # Create the top-left logo space
        logo_space = Image(source='logo.png', size_hint=(None, None), size=(100, 50))

        # Create a grid layout for buttons
        button_grid = GridLayout(cols=2, size_hint=(1, None), height=100)

        # Create a button to run the query
        run_query_button = Button(text='Run Query')
        run_query_button.bind(on_press=self.run_query)

        # Create a button to navigate to another page
        navigate_button = Button(text='Navigate')
        navigate_button.bind(on_press=self.navigate_to_another_page)

        # Add buttons to the grid layout
        button_grid.add_widget(run_query_button)
        button_grid.add_widget(navigate_button)

        # Add widgets to the upper layout
        upper_bar.add_widget(Label(text='Upper Bar'))
        upper_bar.add_widget(logo_space)

        # Add upper layout to main layout
        main_layout.add_widget(upper_bar)

        # Add button grid to main layout
        main_layout.add_widget(button_grid)

        # Add the main layout to the main screen
        main_screen.add_widget(main_layout)

        # Create another screen
        another_screen = AnotherScreen(name='another')

        # Add screens to the screen manager
        sm.add_widget(main_screen)
        sm.add_widget(another_screen)

        return sm

    def run_query(self, instance):
        print("Query executed.")

    def navigate_to_another_page(self, instance):
        self.root.current = 'another'

if __name__ == '__main__':
    MyApp().run()
