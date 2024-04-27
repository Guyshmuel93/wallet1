from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from mysql import get_connection

class RootWidget(BoxLayout):
    pass

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (169, 5, 7, 1)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint=(None, None), size=(400, 500),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.card_input = TextInput(hint_text='Enter card name',multiline=False)
        self.amount_input = TextInput(hint_text='Enter amount',multiline=False)
        self.expiration_input = TextInput(hint_text='Enter expiration',multiline=False)
        insert_button = Button(text='Insert Card', on_press=self.insert_card)
        self.search_input = TextInput(hint_text='Enter store name',multiline=False,
                                      size_hint_y = None,
                                      height = 30,
                                      size_hint_x = None,
                                      width = 70)
        search_button = Button(text='Search', on_press=self.search)

        layout.add_widget(self.card_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.expiration_input)
        layout.add_widget(insert_button)
        layout.add_widget(self.search_input)
        layout.add_widget(search_button)

        self.popup = Popup(title='Search Results', size_hint=(None, None), size=(400, 400), auto_dismiss=False)

        self.result_label = Label(text='', size_hint_y=None, height=300)
        back_button = Button(text='Back', size_hint_y=None, height=50, on_press=self.popup.dismiss)
        self.popup.content = BoxLayout(orientation='vertical', spacing=10)
        self.popup.content.add_widget(self.result_label)
        self.popup.content.add_widget(back_button)

        self.add_widget(layout)

    def search(self, instance):
        store_name = self.search_input.text

        db_manager = get_connection()
        db_manager.connect()

        # Example query
        query = """
            SELECT card_name, amount, expiration
            FROM cards
            WHERE store_name = '{}'
        """.format(store_name)
        result = db_manager.execute_query(query)

        # Display the results in the popup
        if result:
            result_text = f"Details for cards at {store_name}:\n"
            for row in result:
                result_text += f"Card: {row[0]}, Amount: {row[1]}, Expiration: {row[2]}\n"
            self.result_label.text = result_text
        else:
            self.result_label.text = f"No cards found at {store_name}"
        self.popup.open()

    def insert_card(self, instance):
        card_name = self.card_input.text
        amount = self.amount_input.text
        expiration = self.expiration_input.text

        db_manager = get_connection()
        db_manager.connect()

        # Example query for insertion
        query = """
            INSERT INTO cards (card_name, expiration, amount)
            VALUES ('{}', '{}', {})
        """.format(card_name, expiration, amount)
        db_manager.execute_query(query)

        self.card_input.text = ''  # Clear input field after insertion
        self.amount_input.text = ''  # Clear input field after insertion
        self.expiration_input.text = ''  # Clear input field after insertion
        self.result_label.text = 'Card inserted successfully!'  # Show success message


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SearchScreen(name='search'))
        return sm


if __name__ == '__main__':
    MyApp().run()
