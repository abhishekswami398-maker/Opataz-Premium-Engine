import os
import sys
import math
import time
import numpy as np
import pandas as pd
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

Window.keyboard_anim_type = 'padding'

# ==================== KV DESIGN LANGUAGE (TRUE PREMIUM WHITE INTERFACE) ====================
KV = '''
ScreenManager:
    LoginScreen:
    MainScreen:

<LoginScreen>:
    name: 'login'
    MDFloatLayout:
        md_bg_color: [0.97, 0.97, 0.99, 1]

        MDLabel:
            text: "🔮 OPATAZ AI"
            pos_hint: {"center_x": .5, "center_y": .75}
            size_hint_x: .8
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: [0.85, 0.12, 0.12, 1]
            bold: True

        MDLabel:
            text: "On-Device God Mode Engine"
            pos_hint: {"center_x": .5, "center_y": .68}
            size_hint_x: .8
            halign: "center"
            font_style: "Subtitle2"
            theme_text_color: "Custom"
            text_color: [0.4, 0.4, 0.45, 1]

        MDTextField:
            id: phone_num
            hint_text: "Enter Mobile Number"
            helper_text: "With country code (e.g., +91)"
            helper_text_mode: "on_focus"
            pos_hint: {"center_x": .5, "center_y": .52}
            size_hint_x: .8

        MDRaisedButton:
            text: "LOGIN WITH OTP"
            pos_hint: {"center_x": .5, "center_y": .40}
            size_hint_x: .8
            md_bg_color: [0.85, 0.12, 0.12, 1]
            on_release: root.do_login()

        MDRaisedButton:
            text: "CONTINUE WITH GOOGLE"
            pos_hint: {"center_x": .5, "center_y": .31}
            size_hint_x: .8
            md_bg_color: [0.2, 0.2, 0.25, 1]
            on_release: root.do_login()

<MainScreen>:
    name: 'main'
    MDFloatLayout:
        md_bg_color: [0.97, 0.97, 0.99, 1]

        MDCard:
            size_hint: (1, .08)
            pos_hint: {"top": 1}
            md_bg_color: [0.92, 0.94, 0.97, 1]
            radius: [0, 0, 0, 0]
            elevation: 1
            padding: 15
            
            MDLabel:
                text: "🔮 Opataz Engine - Control Panel"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: [0.1, 0.1, 0.1, 1]

        MDRaisedButton:
            id: btn_mode1
            text: "Text Box Mode"
            pos_hint: {"center_x": .28, "center_y": .88}
            size_hint: (.42, .05)
            md_bg_color: [0.85, 0.12, 0.12, 1]
            on_release: root.switch_mode(1)

        MDRaisedButton:
            id: btn_mode2
            text: "CSV File Mode"
            pos_hint: {"center_x": .72, "center_y": .88}
            size_hint: (.42, .05)
            md_bg_color: [0.6, 0.6, 0.65, 1]
            on_release: root.switch_mode(2)

        MDTextField:
            id: txt_chains_input
            hint_text: "Paste Chains here (e.g., 5, -3, 0...)"
            multiline: True
            pos_hint: {"center_x": .5, "center_y": .73}
            size_hint_x: .85
            opacity: 1
            disabled: False

        MDTextField:
            id: txt_csv_input
            hint_text: "Enter CSV Filename (e.g., data.csv)"
            pos_hint: {"center_x": .5, "center_y": .73}
            size_hint_x: .85
            opacity: 0
            disabled: True

        MDRaisedButton:
            id: main_action_btn
            text: "🚀 RUN OPATAZ CORE MATH"
            pos_hint: {"center_x": .5, "center_y": .59}
            size_hint_x: .85
            md_bg_color: [0.85, 0.12, 0.12, 1]
            on_release: root.calculate_opataz()

        MDCard:
            size_hint: (.85, .08)
            pos_hint: {"center_x": .5, "center_y": .48}
            md_bg_color: [0.9, 0.93, 0.96, 1]
            padding: 10
            radius: [8, 8, 8, 8]
            
            MDLabel:
                id: time_label
                text: "Execution Time: -- sec"
                theme_text_color: "Custom"
                text_color: [0.05, 0.45, 0.35, 1]
                font_style: "Button"
                halign: "center"

        MDCard:
            size_hint: (.85, .36)
            pos_hint: {"center_x": .5, "center_y": .23}
            md_bg_color: [1, 1, 1, 1]
            padding: 20
            radius: [12, 12, 12, 12]
            elevation: 2
            orientation: "vertical"
            spacing: 10

            MDLabel:
                text: "🎯 Final Calculation Summary"
                theme_text_color: "Custom"
                text_color: [0.1, 0.1, 0.1, 1]
                font_style: "Subtitle1"
                bold: True

            MDSeparator:
                color: [0.92, 0.92, 0.95, 1]

            MDLabel:
                id: o_prime_label
                text: "O' (Opataz Prime): --"
                theme_text_color: "Custom"
                text_color: [0.25, 0.25, 0.3, 1]
                font_style: "Body1"

            MDLabel:
                id: final_opataz_label
                text: "FINAL RESULT: --"
                theme_text_color: "Custom"
                text_color: [0.85, 0.12, 0.12, 1]
                font_style: "H5"
                bold: True
'''

class LoginScreen(Screen):
    def do_login(self):
        self.manager.current = 'main'

class MainScreen(Screen):
    current_mode = 1

    def switch_mode(self, mode_num):
        self.current_mode = mode_num
        if mode_num == 1:
            self.ids.btn_mode1.md_bg_color = [0.85, 0.12, 0.12, 1]
            self.ids.btn_mode2.md_bg_color = [0.6, 0.6, 0.65, 1]
            self.ids.txt_chains_input.opacity = 1
            self.ids.txt_chains_input.disabled = False
            self.ids.txt_csv_input.opacity = 0
            self.ids.txt_csv_input.disabled = True
            self.ids.main_action_btn.md_bg_color = [0.85, 0.12, 0.12, 1]
        else:
            self.ids.btn_mode1.md_bg_color = [0.6, 0.6, 0.65, 1]
            self.ids.btn_mode2.md_bg_color = [0.05, 0.52, 0.36, 1]
            self.ids.txt_chains_input.opacity = 0
            self.ids.txt_chains_input.disabled = True
            self.ids.txt_csv_input.opacity = 1
            self.ids.txt_csv_input.disabled = False
            self.ids.main_action_btn.md_bg_color = [0.05, 0.52, 0.36, 1]

    def calculate_opataz(self):
        start_time = time.time()
        try:
            if self.current_mode == 1:
                text_data = self.ids.txt_chains_input.text.strip()
                if not text_data: return
                lines = text_data.split('\n')
                raw_list = []
                for l in lines:
                    if l.strip():
                        nums = [float(x) for x in l.replace('[','').replace(']','').split(',') if x.strip()]
                        if nums: raw_list.append(nums)
                if not raw_list: return
                max_cols = max(len(c) for c in raw_list)
                padded_data = [c + [0.0]*(max_cols - len(c)) for c in raw_list]
                raw_data = np.array(padded_data, dtype=np.float64)
                apply_filters = False
            else:
                filename = self.ids.txt_csv_input.text.strip()
                if not filename or not os.path.exists(filename):
                    self.ids.final_opataz_label.text = "Error: File not found!"
                    return
                df = pd.read_csv(filename)
                raw_data = df.values.astype(np.float64)
                apply_filters = True

            rows, cols = raw_data.shape
            first_elements = raw_data[:, 0]
            max_elements = raw_data.max(axis=1)
            min_elements = raw_data.min(axis=1)
            A_vals = np.abs((first_elements + max_elements + min_elements) / 3.0)
            A0 = np.mean(A_vals)

            if len(first_elements) <= 1 or np.all(first_elements == first_elements[0]):
                S = 1.0
            else:
                abs_firsts = np.abs(first_elements)
                S = np.min(abs_firsts) / np.max(abs_firsts) if np.max(abs_firsts) != 0 else 1.0

            s_val = A0 + S
            d_val = s_val - math.floor(s_val)
            sigma = math.ceil(s_val) if (0.51 <= d_val <= 0.99) else math.floor(s_val)

            n_kg = len(str(int(sigma))) if sigma > 0 else 1
            V = 1.0 + (sigma / (10 ** n_kg))
            K = math.ceil(math.sqrt(rows) * V)
            if K % 2 == 0: K += 1

            global_max = raw_data.max()
            global_min = raw_data.min()
            g = math.ceil((global_max - global_min) / K) if global_max != global_min else 1.0
            if g <= 0: g = 1.0

            processed_data = raw_data.copy()
            if apply_filters:
                col_mins = raw_data.min(axis=0)
                col_maxs = raw_data.max(axis=0)
                col_avgs = raw_data.mean(axis=0)
                C_ratios = np.where(col_maxs != 0, col_mins / col_maxs, 0.0)
                if cols == 2:
                    temp0 = processed_data[:, 0] + (processed_data[:, 1] * C_ratios[0])
                    temp1 = processed_data[:, 1] + (processed_data[:, 0] * C_ratios[1])
                    processed_data[:, 0], processed_data[:, 1] = temp0, temp1
                else:
                    for j in range(cols):
                        processed_data[:, j] = processed_data[:, j] + (processed_data[:, j] * C_ratios[j])
                for j in range(cols):
                    if (col_maxs[j] - col_mins[j]) >= 2.0:
                        processed_data[:, j] = col_avgs[j]

            last_col = processed_data[:, -1]
            calc_last = np.where(last_col == 0.0, 0.001, np.where(last_col != np.floor(last_col), np.ceil(last_col), last_col))
            O_matrix = calc_last.copy()
            for j in range(cols - 1):
                t_val = K + processed_data[:, j]
                O_matrix *= np.where(t_val == 0.0, 0.001, t_val)

            O_prime = float(np.sum(np.abs(O_matrix)))
            base_cand = int(g)
            log_base = float(base_cand + 1) if base_cand % 2 != 0 else float(base_cand)
            if log_base <= 1: log_base = 2.0
            
            final_result = math.log(O_prime, log_base) if O_prime > 1 else O_prime
            end_time = time.time() - start_time

            self.ids.time_label.text = f"✅ Processed in: {end_time:.4f} sec"
            self.ids.o_prime_label.text = f"O' (Opataz Prime): {O_prime:.4f}"
            self.ids.final_opataz_label.text = f"FINAL RESULT: {final_result:.6f}"
        except Exception as ex:
            self.ids.final_opataz_label.text = f"Error: {str(ex)}"

class OpatazApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_string(KV)

if __name__ == '__main__':
    OpatazApp().run()
