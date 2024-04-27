# profilescreen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a layout for the profile screen
        profile_layout = BoxLayout(orientation='vertical')

        # Add a profile picture
        profile_picture = Image(source='profile_pic.png', size_hint=(1, 0.5))

        # Add user information labels
        user_name_label = Label(text='John Doe', font_size=24)
        user_bio_label = Label(text='Software Developer | Musician', font_size=18)
        user_location_label = Label(text='New York, USA', font_size=18)

        # Add widgets to the profile layout
        profile_layout.add_widget(profile_picture)
        profile_layout.add_widget(user_name_label)
        profile_layout.add_widget(user_bio_label)
        profile_layout.add_widget(user_location_label)

        # Set the profile layout as the content of the screen
        self.add_widget(profile_layout)
