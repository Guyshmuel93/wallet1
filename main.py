import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from mysql import db_config, DatabaseManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from prettytable import PrettyTable


class RootWidget(BoxLayout):
    pass


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (9, 5, 7, 1)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint=(None, None), size=(400, 500),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.card_input = TextInput(hint_text='Enter card name', multiline=False)
        self.amount_input = TextInput(hint_text='Enter amount', multiline=False)
        self.experation = TextInput(hint_text='Enter expiration', multiline=False)
        insert_button = Button(text='Insert Card', on_press=self.insert_card)

        self.search_input = TextInput(hint_text='Enter store name', multiline=False,
                                      size_hint_y=None,
                                      height=30,
                                      size_hint_x=None,
                                      width=180)
        search_button = Button(text='Search', on_press=self.search)
        showAll_button = Button(text='Show All Cards', on_press=self.showallcards)

        layout.add_widget(self.card_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.experation)
        layout.add_widget(insert_button)
        layout.add_widget(self.search_input)
        layout.add_widget(search_button)
        layout.add_widget(showAll_button)

        self.popup = Popup(title='Search Results', size_hint=(None, None), size=(400, 400), auto_dismiss=False)

        self.result_label = Label(text='', size_hint_y=None, height=300)
        back_button = Button(text='Back', size_hint_y=None, height=50, on_press=self.popup.dismiss)
        self.popup.content = BoxLayout(orientation='vertical', spacing=10)
        self.popup.content.add_widget(self.result_label)
        self.popup.content.add_widget(back_button)

        self.add_widget(layout)
        # self.add_widget(frame)

    def extract_total_amount(self, result):
        if result:
            return int(result[0]['total_amount'])
        else:
            return 0  # Or any default value you want to return if there is no result

    # def search(self, instance):
    #     store_name = self.search_input.text
    #
    #     db_manager = DatabaseManager(db_config)
    #     db_manager.connect()
    #     query_results = f"SELECT SUM(amount) AS total_amount FROM cards WHERE card_name IN (SELECT card_name FROM stores WHERE store_name = 'castro');"
    #     result = db_manager.execute_query(query_results)
    #     query = f"SELECT * FROM cards WHERE card_name IN (SELECT card_name FROM stores WHERE store_name='castro');"
    #     listing = db_manager.execute_query(query)
    #
    #     total_amount = self.extract_total_amount(result)
    #     print(total_amount)
    #     print(listing)
    #     if result:
    #         # Prepare the result text
    #         result_text = f"Details for cards at {store_name}:\n"
    #         for row in result:
    #             result_text += f"for the store: {store_name} you have total credits of : {total_amount}"
    #
    #         # Set the result text to the label in the popup
    #         self.result_label.text = result_text
    #     else:
    #         self.result_label.text = f"No cards found at {store_name}"
    #
    #     self.popup.open()

    def search(self, instance):
        store_name = self.search_input.text

        db_manager = DatabaseManager(db_config)
        db_manager.connect()

        # Query to get cards for the specified store
        query = f"SELECT * FROM cards WHERE card_name IN (SELECT card_name FROM stores WHERE store_name='{store_name}');"
        rows = db_manager.execute_query(query)

        # Query to get the total amount of credits for the specified store
        total_amount_query = f"SELECT SUM(amount) AS total_amount FROM cards WHERE card_name IN (SELECT card_name FROM stores WHERE store_name='{store_name}');"
        total_amount_result = db_manager.execute_query(total_amount_query)
        total_amount = total_amount_result[0]['total_amount'] if total_amount_result else 0

        # Create a GridLayout for the table
        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)

        # Add column headers
        grid_layout.add_widget(Label(text='Card Name', bold=True))
        grid_layout.add_widget(Label(text='Amount', bold=True))
        grid_layout.add_widget(Label(text='Expiration', bold=True))

        # Add data rows
        for row in rows:
            grid_layout.add_widget(Label(text=row['card_name']))
            grid_layout.add_widget(Label(text=str(row['amount'])))
            grid_layout.add_widget(Label(text=row['expiration']))

        # Prepare the result text
        result_text = f"Total credits for {store_name}: {total_amount}\n\n"

        # Set the GridLayout as content for the popup
        self.popup.content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.popup.content.add_widget(Label(text=result_text))
        self.popup.content.add_widget(grid_layout)

        # Open the popup to display the result
        self.popup.open()

    def insert_card(self, instance):
        card_name = self.card_input.text
        amount = self.amount_input.text
        expiration = self.experation.text

        if not card_name or not amount or not expiration:
            result_text = f"Please fill in all fields\n"
            self.result_label.text = result_text
            self.popup.open()

        else:
            db_manager = DatabaseManager(db_config)
            # Connect to the database
            db_manager.connect()

            query = "INSERT INTO cards (card_name, amount, expiration) VALUES ('{}', '{}', '{}');".format(card_name, amount,
                                                                                                          expiration)
            db_manager.execute_query(query)

            self.card_input.text = ''  # Clear input field after insertion
            self.amount_input.text = ''  # Clear input field after insertion
            self.experation.text = ''  # Clear input field after insertion
            result_text = f"Card inserted successfully\n"
            self.result_label.text = result_text
            self.popup.open()


    def showallcards(self, instance):
        db_manager = DatabaseManager(db_config)
        db_manager.connect()
        query = "select * from cards;"
        rows = db_manager.execute_query(query)

        # Create a GridLayout for the table
        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)

        # Add column headers
        grid_layout.add_widget(Label(text='Card Name'))
        grid_layout.add_widget(Label(text='Amount'))
        grid_layout.add_widget(Label(text='Expiration'))

        # Add data rows
        for row in rows:
            grid_layout.add_widget(Label(text=row['card_name']))
            grid_layout.add_widget(Label(text=str(row['amount'])))
            grid_layout.add_widget(Label(text=row['expiration']))

        # Set the GridLayout as content for the popup
        self.popup.content = grid_layout

        # Open the popup to display the result
        self.popup.open()

class MyApp(App):
    def build(self):
        # Window.size = (720, 1280)

        sm = ScreenManager()
        sm.add_widget(SearchScreen(name='search'))
        return sm


if __name__ == '__main__':
    MyApp().run()
