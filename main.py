import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from mysql import get_connection
import pymysql

class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            connection = mysql.connector.connect(**mysql_config)
            print("Connected to MySQL database")

            # Create a cursor object
            cursor = connection.cursor()

            # Your database operations here

        except mysql.connector.Error as error:
            print("Error:", error)

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

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
        self.experation = TextInput(hint_text='Enter expiration',multiline=False)
        insert_button = Button(text='Insert Card', on_press=self.insert_card)
        root = RootWidget()

        # frame = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint=(None, None), size=(400, 500),
        #                    pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # frame = BoxLayout(orientation='vertical')
        # test_button = Button(text='move', on_press=self.insert_card)
        # frame.add_widget(test_button)
        # test_button = Button(text=' first',size_hint_y = None,
        #                               height = root.height * 0.8,
        #                               size_hint_x = None,
        #                               width = root.width*10)
        # # frame.add_widget(frame.test)
        # frame.add_widget(test_button)
        #
        # frame.bind(minimum_height=frame.test.setter('height'))
        # frame.pos_hint = {'x': 0, 'y': 0}

        self.search_input = TextInput(hint_text='Enter store name',multiline=False,
                                      size_hint_y = None,
                                      height = 30,
                                      size_hint_x = None,
                                      width = 70)
        search_button = Button(text='Search', on_press=self.search)

        layout.add_widget(self.card_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.experation)
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
        # self.add_widget(frame)

    def search(self, instance):
        store_name = self.search_input.text

        # Connect to the SQLite database
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # # Execute the query
        # cursor.execute("""
        #     SELECT s.card_name, cm.amount, cm.expiration
        #     FROM stores AS s
        #     INNER JOIN cards AS cm ON s.card_name = cm.card_name
        #     WHERE s.store_name=?
        # """, (store_name,))
        # rows = cursor.fetchall()
        #
        # # Close the cursor and connection
        # cursor.close()
        # conn.close()
        db_manager = DatabaseManager()
        db_manager.connect()

        # Example query
        query = """"
            SELECT * from stores;
            
        """
        result = db_manager.execute_query(query)
        print("Query Result:")
        for rows in result:
            print(rows)

        # Display the results in the popup
        if rows:
            result_text = f"Details for cards at {store_name}:\n"
            for row in rows:
                result_text += f"Card: {row[0]}, Amount: {row[1]}, Expiration: {row[2]}\n"
            self.result_label.text = result_text
        else:
            self.result_label.text = f"No cards found at {store_name}"
        self.popup.open()

    def insert_card(self, instance):
        card_name = self.card_input.text
        amount = self.amount_input.text
        expiration = self.experation.text

        # Connect to the SQLite database
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Execute the insertion
        cursor.execute("INSERT INTO cards (card_name, expiration, amount) VALUES (?, ?, ?)", (card_name, expiration, amount))

        # Commit changes and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        self.card_input.text = ''  # Clear input field after insertion
        self.amount_input.text = ''  # Clear input field after insertion
        self.experation.text = ''  # Clear input field after insertion
        self.result_label.text = 'Card inserted successfully!'  # Show success message


class MyApp(App):
    def build(self):
        # Window.size = (720, 1280)

        sm = ScreenManager()
        sm.add_widget(SearchScreen(name='search'))
        return sm


if __name__ == '__main__':
    MyApp().run()
