from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.utils import platform
import random
import json
import os

class FlagGameApp(App):
    def build(self):
        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add a label for the title
        title = Label(text='Guess the Flag!', size_hint_y=0.1)
        layout.add_widget(title)
        
        # Add a placeholder for the flag image
        self.flag_image = Image(source='', size_hint_y=0.6)
        layout.add_widget(self.flag_image)
        
        # Add a button to start the game
        start_button = Button(
            text='Start Game', 
            size_hint_y=0.3,
            background_color=(0.3, 0.6, 0.9, 1)
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)
        
        return layout
    
    def start_game(self, instance):
        print("Game started!")
        # Add your game logic here

if __name__ == '__main__':
    FlagGameApp().run()