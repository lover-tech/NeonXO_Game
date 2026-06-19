from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import random

# मोबाइल स्क्रीन का प्रीमियम साइज
Window.size = (420, 720)

class NeonButton(Button):
    """कस्टम राउंडेड और नियॉन स्टाइल बटन"""
    def __init__(self, **kwargs):
        super(NeonButton, self).__init__(**kwargs)
        self.font_size = '55sp'
        self.bold = True
        self.background_normal = ''
        self.background_color = (0.12, 0.12, 0.18, 1) # डार्क प्रीमियम स्पेस कलर

class UltraPremiumTicTacToe(BoxLayout):
    def __init__(self, **kwargs):
        super(UltraPremiumTicTacToe, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 25, 20, 25]
        self.spacing = 18
        
        # गेम स्टेट्स
        self.current_player = 'X'
        self.next_round_starter = 'X' # अगले राउंड की पहली चाल तय करने के लिए
        self.board_state = [''] * 9
        self.game_active = True
        self.scores = {'X': 0, 'O': 0}
        self.game_mode = 'AI' 

        # 1. टॉप हेडर (गेम का नाम)
        self.header_label = Label(
            text="NEON XO",
            font_size='32sp',
            bold=True,
            size_hint=(1, 0.08),
            color=(0, 0.95, 0.95, 1) # Neon Cyan
        )
        self.add_widget(self.header_label)

        # 2. मॉडर्न मोड收藏न बार
        mode_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=12)
        self.btn_vs_ai = Button(text="VS COMPUTER", font_size='13sp', bold=True, background_normal='', background_color=(0, 0.6, 0.8, 1))
        self.btn_vs_2p = Button(text="2 PLAYERS", font_size='13sp', bold=True, background_normal='', background_color=(0.18, 0.18, 0.24, 1))
        
        self.btn_vs_ai.bind(on_press=lambda x: self.set_game_mode('AI'))
        self.btn_vs_2p.bind(on_press=lambda x: self.set_game_mode('2P'))
        
        mode_layout.add_widget(self.btn_vs_ai)
        mode_layout.add_widget(self.btn_vs_2p)
        self.add_widget(mode_layout)

        # 3. प्रीमियम ग्लास-लुक स्कोर बोर्ड
        score_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        self.score_x_label = Label(text="YOU (X)\n0", font_size='16sp', bold=True, halign='center', color=(0, 0.95, 0.95, 1))
        self.score_o_label = Label(text="CPU (O)\n0", font_size='16sp', bold=True, halign='center', color=(1, 0.2, 0.6, 1))
        score_layout.add_widget(self.score_x_label)
        score_layout.add_widget(self.score_o_label)
        self.add_widget(score_layout)

        # 4. लाइव टर्न/स्टेटस इंडिकेटर
        self.status_label = Label(text="YOUR TURN (X)", font_size='22sp', bold=True, size_hint=(1, 0.06), color=(0, 0.95, 0.95, 1))
        self.add_widget(self.status_label)

        # 5. 3x3 का गेम ग्रिड (Neon Matrix)
        self.grid = GridLayout(cols=3, rows=3, spacing=12, size_hint=(1, 0.53))
        self.buttons = []
        for i in range(9):
            btn = NeonButton()
            btn.bind(on_press=self.on_button_click)
            self.buttons.append(btn)
            self.grid.add_widget(btn)
        self.add_widget(self.grid)

        # 6. बॉटम प्रीमियम एक्शन बटन
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=12)
        self.restart_btn = Button(text='NEXT ROUND', font_size='16sp', bold=True, background_normal='', background_color=(0.05, 0.7, 0.4, 1))
        self.restart_btn.bind(on_press=self.next_round)
        
        self.reset_score_btn = Button(text='RESET ALL', font_size='16sp', bold=True, background_normal='', background_color=(0.7, 0.15, 0.15, 1))
        self.reset_score_btn.bind(on_press=self.reset_everything)
        
        bottom_layout.add_widget(self.restart_btn)
        bottom_layout.add_widget(self.reset_score_btn)
        self.add_widget(bottom_layout)

    def set_game_mode(self, mode):
        self.game_mode = mode
        if mode == 'AI':
            self.btn_vs_ai.background_color = (0, 0.6, 0.8, 1)
            self.btn_vs_2p.background_color = (0.18, 0.18, 0.24, 1)
        else:
            self.btn_vs_2p.background_color = (0, 0.6, 0.8, 1)
            self.btn_vs_ai.background_color = (0.18, 0.18, 0.24, 1)
        self.reset_everything(None)

    def on_button_click(self, instance):
        button_index = self.buttons.index(instance)

        if not self.game_active or self.board_state[button_index] != '':
            return

        if self.game_mode == 'AI':
            # AI मोड में हमेशा प्लेयर 'X' होता है
            if self.current_player == 'X':
                self.make_move(button_index, 'X', (0, 0.95, 0.95, 1))
                
                if self.game_active and '' in self.board_state:
                    self.current_player = 'O'
                    self.status_label.text = "CPU IS THINKING..."
                    self.ai_move()
                    
        elif self.game_mode == '2P':
            # 2 Player मोड का पूरा सुधरा हुआ लॉजिक
            if self.current_player == 'X':
                self.make_move(button_index, 'X', (0, 0.95, 0.95, 1))
                if self.game_active:
                    self.current_player = 'O'
                    self.status_label.text = "PLAYER O'S TURN"
                    self.status_label.color = (1, 0.2, 0.6, 1)
            else:
                self.make_move(button_index, 'O', (1, 0.2, 0.6, 1))
                if self.game_active:
                    self.current_player = 'X'
                    self.status_label.text = "PLAYER X'S TURN"
                    self.status_label.color = (0, 0.95, 0.95, 1)

    def make_move(self, index, player, color):
        self.board_state[index] = player
        self.buttons[index].text = player
        self.buttons[index].color = color
        
        is_win, combo = self.check_winner()
        if is_win:
            self.scores[player] += 1
            self.update_score_display()
            
            # जीतने वाला ही अगले राउंड की शुरुआत करेगा
            self.next_round_starter = player 
            
            for idx in combo:
                self.buttons[idx].background_color = (1, 0.75, 0, 1)
                self.buttons[idx].color = (0.05, 0.05, 0.08, 1)
            
            # विनर टेक्स्ट सेटिंग्स
            if self.game_mode == 'AI':
                win_text = "YOU WIN! 🎉" if player == 'X' else "CPU WINS! 🤖"
            else:
                win_text = f"PLAYER {player} WINS! 🎉"
            
            self.status_label.text = win_text
            self.status_label.color = (1, 0.75, 0, 1)
            self.game_active = False
            
        elif '' not in self.board_state:
            self.status_label.text = "IT'S A DRAW! 🤝"
            self.status_label.color = (0.6, 0.6, 0.7, 1)
            self.next_round_starter = 'X' # ड्रॉ होने पर X से शुरुआत
            self.game_active = False

    def ai_move(self):
        # स्मार्ट एआई ब्लॉक और विन लॉजिक
        for player_check in ['O', 'X']:
            for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
                vals = [self.board_state[i] for i in combo]
                if vals.count(player_check) == 2 and vals.count('') == 1:
                    empty_idx = combo[vals.index('')]
                    self.make_move(empty_idx, 'O', (1, 0.2, 0.6, 1))
                    if self.game_active:
                        self.current_player = 'X'
                        self.status_label.text = "YOUR TURN (X)"
                        self.status_label.color = (0, 0.95, 0.95, 1)
                    return
        
        empty_cells = [i for i, val in enumerate(self.board_state) if val == '']
        if empty_cells:
            random_idx = random.choice(empty_cells)
            self.make_move(random_idx, 'O', (1, 0.2, 0.6, 1))
            if self.game_active:
                self.current_player = 'X'
                self.status_label.text = "YOUR TURN (X)"
                self.status_label.color = (0, 0.95, 0.95, 1)

    def check_winner(self):
        win_conditions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for condition in win_conditions:
            if self.board_state[condition[0]] == self.board_state[condition[1]] == self.board_state[condition[2]] != '':
                return True, condition
        return False, []

    def update_score_display(self):
        name_x = "YOU" if self.game_mode == 'AI' else "PLAYER X"
        name_o = "CPU" if self.game_mode == 'AI' else "PLAYER O"
        self.score_x_label.text = f"{name_x}\n{self.scores['X']}"
        self.score_o_label.text = f"{name_o}\n{self.scores['O']}"

    def next_round(self, instance):
        self.board_state = [''] * 9
        self.game_active = True
        
        # जीतने वाले को पहली चाल देना
        self.current_player = self.next_round_starter
        
        for btn in self.buttons:
            btn.text = ''
            btn.background_color = (0.12, 0.12, 0.18, 1)
            
        # टर्न इंडिकेटर टेक्स्ट अपडेट करना
        if self.game_mode == 'AI':
            if self.current_player == 'X':
                self.status_label.text = "YOUR TURN (X)"
                self.status_label.color = (0, 0.95, 0.95, 1)
            else:
                self.status_label.text = "CPU IS THINKING..."
                self.ai_move()
        else:
            self.status_label.text = f"PLAYER {self.current_player}'S TURN"
            self.status_label.color = (0, 0.95, 0.95, 1) if self.current_player == 'X' else (1, 0.2, 0.6, 1)

    def reset_everything(self, instance):
        self.scores = {'X': 0, 'O': 0}
        self.next_round_starter = 'X'
        self.update_score_display()
        self.next_round(None)

class NeonXOApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.07, 1) 
        return UltraPremiumTicTacToe()

if __name__ == '__main__':
    NeonXOApp().run()