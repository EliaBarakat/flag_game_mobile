from kivy.resources import resource_add_path
import os
from kivy.app import App
from flag_game_mobile import FlagGame

# Set up asset paths
current_dir = os.path.dirname(os.path.abspath(__file__))
resource_add_path(os.path.join(current_dir, 'assets'))
resource_add_path(os.path.join(current_dir, 'data'))

if __name__ == '__main__':
    FlagGame().run()
