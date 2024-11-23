import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy
kivy.require('2.2.1')  # Replace with your installed version
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
import json
import os
import random
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Title
        title = Label(
            text='How to Play',
            font_size='40sp',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(title)
        
        # Rules text
        rules_text = (
            "1. Choose your challenge:\n"
            "   • 10 Random Flags\n"
            "   • 20 Random Flags\n"
            "   • 50 Random Flags\n"
            "   • 100 Random Flags\n"
            "   • All Flags\n\n"
            "2. For each flag shown:\n"
            "   • Select the correct country\n"
            "   • Green = Correct\n"
            "   • Red = Wrong\n\n"
            "3. Try to get the highest score!"
        )
        
        rules = Label(
            text=rules_text,
            font_size='18sp',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(0, 0, 0, 1),
            halign='left',
            valign='middle'
        )
        rules.bind(size=rules.setter('text_size'))
        self.add_widget(rules)
        
        # Back button
        back_btn = Button(
            text='Back to Menu',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        self.add_widget(back_btn)

    def go_back(self, instance):
        self.manager.current = 'menu'

class FlagGame(App):
    def build(self):
        try:
            self.selected_flag_count = None
            Window.clearcolor = (0.95, 0.95, 0.95, 1)
            
            # Handle Android back button
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, 
                                  Permission.WRITE_EXTERNAL_STORAGE])
                from android import loadingscreen
                loadingscreen.hide_loading_screen()
                
                # Bind the back button
                from kivy.core.window import Window
                Window.bind(on_keyboard=self.android_back_click)
                
            # Set window properties
            if platform == 'android':
                Window.fullscreen = 'auto'
            else:
                Window.size = (400, 600)
            
            # Load game data
            self.load_data()
            
            # Create screen manager
            self.sm = ScreenManager()
            
            # Add screens in the correct order
            self.sm.add_widget(MenuScreen(name='menu'))
            self.sm.add_widget(HelpScreen(name='help'))  # Make sure HelpScreen is added
            self.sm.add_widget(GameScreen(name='game'))
            self.sm.add_widget(ScoreScreen(name='score'))
            
            return self.sm
        except Exception as e:
            print(f"Error in build: {e}")
            raise

    def load_data(self):
        try:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            countries_path = os.path.join(data_dir, 'countries.json')
            highscores_path = os.path.join(data_dir, 'highscores.json')
            
            with open(countries_path, 'r') as f:
                self.countries = json.load(f)
                print(f"Loaded {len(self.countries)} countries")
        except Exception as e:
            print(f"Error loading countries data: {e}")
            self.countries = {}
            
        try:
            with open(highscores_path, 'r') as f:
                self.highscores = json.load(f)
        except Exception as e:
            print(f"Error loading highscores: {e}")
            self.highscores = {"scores": []}

    def android_back_click(self, window, key, *largs):
        # Handle Android back button
        if key == 27:  # Android back button key code
            if self.sm.current == 'menu':
                # If on menu, ask to quit
                self.show_quit_dialog()
                return True
            elif self.sm.current == 'game':
                # If in game, go back to menu
                self.sm.current = 'menu'
                return True
            elif self.sm.current in ['help', 'score']:
                # If in help or score screen, go back to menu
                self.sm.current = 'menu'
                return True
        return False

    def show_quit_dialog(self):
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        
        content = BoxLayout(orientation='vertical')
        message = Label(text='Do you want to exit?')
        buttons = BoxLayout(size_hint_y=None, height='40dp')
        
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(message)
        content.add_widget(buttons)
        
        popup = Popup(title='Exit', content=content, 
                     size_hint=(0.8, 0.3))
        
        def on_yes(instance):
            self.stop()
            
        def on_no(instance):
            popup.dismiss()
            
        yes_button.bind(on_press=on_yes)
        no_button.bind(on_press=on_no)
        popup.open()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Title
        title = Label(
            text='Guess the Flag',
            font_size='40sp',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(title)
        
        # Game mode buttons
        modes = [
            ('10 Random Flags', 0.7, lambda x: self.start_game(10)),
            ('20 Random Flags', 0.6, lambda x: self.start_game(20)),
            ('50 Random Flags', 0.5, lambda x: self.start_game(50)),
            ('100 Random Flags', 0.4, lambda x: self.start_game(100)),
            ('All Flags', 0.3, lambda x: self.start_game(None)),
            ('How to Play', 0.2, self.show_help),
            ('Exit', 0.1, self.quit_game)
        ]
        
        for text, pos_y, callback in modes:
            btn = Button(
                text=text,
                size_hint=(0.8, 0.08),
                pos_hint={'center_x': 0.5, 'center_y': pos_y},
                background_color=(0.3, 0.6, 1, 1),
                color=(1, 1, 1, 1),
                font_size='20sp',
                bold=True
            )
            btn.bind(on_press=callback)
            self.add_widget(btn)

    def start_game(self, flag_count):
        app = App.get_running_app()
        app.selected_flag_count = flag_count
        self.manager.current = 'game'
    
    def show_help(self, instance):
        self.manager.current = 'help'
    
    def quit_game(self, instance):
        App.get_running_app().stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.total_questions = 0
        self.current_answer = None
        self.show_feedback = False
        self.used_flags = set()  # Track which flags have been shown
        
        # Update score label - Move it higher
        self.score_label = Label(
            text='Score: 0/0',
            size_hint=(0.3, 0.1),
            pos_hint={'right': 0.95, 'top': 0.98},  # Moved higher
            color=(0, 0, 0, 1),
            font_size='20sp',
            bold=True
        )
        self.add_widget(self.score_label)
        
        # Update flag image - moved higher
        self.flag_image = Image(
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},  # Moved higher from 0.65 to 0.7
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.flag_image)
        
        # Update answer buttons - keep them where they are
        self.answer_buttons = []
        for i in range(4):
            btn = Button(
                size_hint=(0.8, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.45 - (i * 0.12)},
                background_color=(0.3, 0.6, 1, 1),
                color=(1, 1, 1, 1),
                font_size='18sp',
                bold=True
            )
            btn.bind(on_press=self.check_answer)
            self.answer_buttons.append(btn)
            self.add_widget(btn)
        
        # Update home button to say 'Exit' instead of '⌂'
        home_btn = Button(
            text='Exit',  # Changed from '⌂' to 'Exit'
            size_hint=(0.15, 0.08),
            pos_hint={'x': 0.05, 'top': 0.95},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',  # Adjusted font size for 'Exit'
            bold=True
        )
        home_btn.bind(on_press=self.go_home)
        self.add_widget(home_btn)

    def on_enter(self):
        # Reset all game state variables
        self.used_flags = set()
        self.score = 0
        self.total_questions = 0
        self.score_label.text = 'Score: 0/0'  # Reset score display
        
        # Get the selected flag count from the app
        app = App.get_running_app()
        self.flag_count = app.selected_flag_count
        
        # If flag_count is None, use all flags
        if self.flag_count is None:
            self.available_flags = list(app.countries.keys())
        else:
            # Randomly select the specified number of flags
            all_flags = list(app.countries.keys())
            self.available_flags = random.sample(
                all_flags, 
                min(self.flag_count, len(all_flags))
            )
        
        self.start_new_question()

    def start_new_question(self):
        app = App.get_running_app()
        
        try:
            # Get list of remaining flags from our selected subset
            remaining_flags = [flag for flag in self.available_flags 
                             if flag not in self.used_flags]
            
            # If no flags left, show final score
            if not remaining_flags:
                self.show_final_score()
                return
            
            # Select random correct answer from remaining flags
            self.current_answer = random.choice(remaining_flags)
            self.used_flags.add(self.current_answer)
            
            # Load flag image
            flag_path = os.path.join('assets', 'flags', f'{self.current_answer}.png')
            self.flag_image.source = flag_path
            
            # Create list of options (1 correct, 3 wrong)
            options = [self.current_answer]
            all_countries = list(app.countries.keys())
            while len(options) < 4:
                wrong_answer = random.choice(all_countries)
                if wrong_answer not in options:
                    options.append(wrong_answer)
            
            random.shuffle(options)
            
            # Update button texts with country names
            for btn, country_code in zip(self.answer_buttons, options):
                country_name = app.countries.get(country_code, "Unknown")
                btn.text = country_name
                btn.background_color = (0.3, 0.6, 1, 1)  # Reset to blue
                
        except Exception as e:
            print(f"Error in start_new_question: {e}")

    def check_answer(self, instance):
        if self.show_feedback:
            return
            
        app = App.get_running_app()
        selected_text = instance.text
        correct_text = app.countries[self.current_answer]
        
        self.total_questions += 1
        
        if selected_text == correct_text:
            instance.background_color = (0, 1, 0, 1)  # Green for correct
            self.score += 1
        else:
            instance.background_color = (1, 0, 0, 1)  # Red for wrong
            # Show correct answer
            for btn in self.answer_buttons:
                if btn.text == correct_text:
                    btn.background_color = (0, 1, 0, 1)
        
        # Simple score counter during gameplay
        self.score_label.text = f'Score: {self.score}/{self.total_questions}'
        
        # Show feedback briefly before next question
        self.show_feedback = True
        Clock.schedule_once(self.after_feedback, 1.5)

    def after_feedback(self, dt):
        self.show_feedback = False
        self.start_new_question()

    def show_final_score(self):
        score_screen = self.manager.get_screen('score')
        score_screen.final_score.text = f'Final Score: {self.score}/{self.total_questions}'
        self.manager.current = 'score'
        
        # Reset game state
        self.score = 0
        self.total_questions = 0
        self.used_flags = set()
        self.score_label.text = 'Score: 0/0'

    def go_home(self, instance):
        # Reset everything before going back to menu
        self.used_flags = set()
        self.score = 0
        self.total_questions = 0
        self.score_label.text = 'Score: 0/0'
        self.manager.current = 'menu'

class ScoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add score title
        self.score_title = Label(
            text='Your Results',
            font_size='40sp',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            color=(0, 0, 0, 1),  # Black text
            bold=True
        )
        self.add_widget(self.score_title)
        
        # Add score display with black text
        self.final_score = Label(
            text='Score: 0/0',
            font_size='30sp',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            color=(0, 0, 0, 1),  # Black text
            bold=True
        )
        self.add_widget(self.final_score)
        
        # Add buttons
        buttons = [
            ('Play Again', 0.4, self.play_again),
            ('Menu', 0.25, self.go_to_menu)
        ]
        
        for text, pos_y, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(0.8, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': pos_y},
                background_color=(0.3, 0.6, 1, 1),  # Blue color
                color=(1, 1, 1, 1),  # White text
                font_size='20sp',
                bold=True
            )
            btn.bind(on_press=callback)
            self.add_widget(btn)

    def play_again(self, instance):
        self.manager.current = 'game'

    def go_to_menu(self, instance):
        self.manager.current = 'menu'

if __name__ == '__main__':
    FlagGame().run()