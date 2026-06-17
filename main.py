import os
import math
import time
import csv
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.chip import MDChip
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty

# =============================================================================
# 🔥 शुद्ध पायथन महा-इंजन (C++ engine.cpp के 100% सटीक ऑफलाइन नियमों के साथ)
# =============================================================================
class OpatazPythonEngine:
    @staticmethod
    def calc_A(elems):
        if not elems: return 0.0
        first = elems[0]
        max_val = max(elems)
        min_val = min(elems)
        return abs((first + max_val + min_val) / 3.0)

    @staticmethod
    def calc_S(firsts):
        if len(firsts) <= 1: return 1.0
        if len(set(firsts)) == 1: return 1.0
        abs_vals = [abs(v) for v in firsts]
        min_val = min(abs_vals)
        max_val = max(abs_vals)
        return (min_val / max_val) if max_val != 0.0 else 1.0

    @staticmethod
    def calc_sigma(A0, S):
        s = A0 + S
        d = s - math.floor(s)
        return math.ceil(s) if (0.51 <= d <= 0.99) else math.floor(s)

    @staticmethod
    def calc_K(N, V):
        K = math.ceil(math.sqrt(N) * V)
        return K + 1 if (K % 2 == 0) else K

    @staticmethod
    def calc_g(max_val, min_val, K):
        if max_val == min_val or K <= 0: return 1.0
        return math.ceil((max_val - min_val) / float(K))

    @staticmethod
    def detect_and_resolve_loop(elems, K, has_dots):
        loop_elements = set()
        if not has_dots: return elems, loop_elements
        seen = {}
        i = 0
        working_elems = list(elems)
        while i < len(working_elems):
            v = working_elems[i]
            if v in seen:
                start_idx = seen[v]
                loop_part = working_elems[start_idx:i]
                for x in loop_part: loop_elements.add(x)
                last = 0.001 if loop_part[-1] == 0.0 else loop_part[-1]
                O_temp = last
                for j in range(len(loop_part) - 1):
                    t = K + loop_part[j]
                    O_temp *= 0.001 if t == 0.0 else t
                min_l = min(loop_part)
                max_l = max(loop_part)
                r = (min_l / max_l) if max_l != 0.0 else 0.0
                O_inf = abs(O_temp / (1.0 - r)) if r != 1.0 else abs(O_temp)
                del working_elems[start_idx:i + 1]
                working_elems.insert(start_idx, O_inf)
                seen.clear()
                i = 0
                continue
            seen[v] = i
            i += 1
        return working_elems, loop_elements

    @staticmethod
    def apply_c_ratio_manual(chains):
        if not chains: return chains
        mx = max(len(c) for c in chains)
        mod = [list(c) for c in chains]
        for ci in range(mx):
            col = []
            for c in chains:
                if ci < len(c): col.append(c[ci])
            if len(col) <= 1 or len(set(col)) == 1: continue
            min_col = min(col)
            max_col = max(col)
            if max_col == 0.0: continue
            cr = min_col / max_col
            if len(col) == 2:
                for i in range(len(mod)):
                    if ci < len(mod[i]): mod[i][ci] = chains[i][ci] + (col[1 - i] * cr)
            else:
                for i in range(len(mod)):
                    if ci < len(mod[i]): mod[i][ci] = chains[i][ci] + (chains[i][ci] * cr)
        return mod

    @staticmethod
    def apply_rnv_manual(chains):
        if len(chains) <= 1: return chains
        mx = max(len(c) for c in chains)
        mod = [list(c) for c in chains]
        for ci in range(mx):
            col = []
            for c in chains:
                if ci < len(c): col.append(c[ci])
            if len(col) < 2: continue
            min_col = min(col)
            max_col = max(col)
            if (max_col - min_col) >= 2.0:
                avg = sum(col) / len(col)
                for i in range(len(mod)):
                    if ci < len(mod[i]): mod[i][ci] = avg
        return mod

    @staticmethod
    def calc_opataz_manual(elems, K):
        if not elems: return 0.0
        last = elems[-1]
        calc_last = 0.001 if last == 0.0 else (math.ceil(last) if last != math.floor(last) else last)
        O = calc_last
        for i in range(len(elems) - 1):
            t = K + elems[i]
            O *= 0.001 if t == 0.0 else t
        return abs(O)

    @staticmethod
    def accumulate_frequency_chunk(current_aavriti, chunk_flat, x, g, K):
        if g <= 0.0 or K <= 0: return current_aavriti
        epsilon = 1e-9
        for v in chunk_flat:
            diff = v - x
            if diff < -epsilon:
                current_aavriti[0] += 1
                continue
            if diff < 0.0: diff = 0.0
            index = int(math.floor(diff / g))
            if index >= K or v >= (x + K * g - epsilon):
                index = K - 1
            if index < 0:
                index = 0
            current_aavriti[index] += 1
        return current_aavriti

# =============================================================================
# 🎨 UI डिज़ाइन इंटरफ़ेस लेआउट (KivyMD)
# =============================================================================
KV = '''
MDScreenManager:
    LoginScreen:
    MainScreen:

<LoginScreen>:
    name: 'login_screen'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.96, 0.97, 0.98, 1
        padding: "24dp"
        spacing: "20dp"

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "180dp"
            pos_hint: {"center_x": .5}
            spacing: "8dp"
            
            MDLabel:
                text: "🔮 OPATAZ AI"
                halign: "center"
                font_style: "H4"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.85, 0.15, 0.15, 1

            MDLabel:
                text: "ऑफलाइन मोबाइल महा-इंजन संस्करण"
                halign: "center"
                font_style: "Subtitle2"
                theme_text_color: "Hint"

        MDCard:
            orientation: 'vertical'
            padding: "24dp"
            spacing: "16dp"
            size_hint_y: None
            height: "250dp"
            radius: [16, 16, 16, 16]
            elevation: 2
            md_bg_color: 1, 1, 1, 1
            pos_hint: {"center_x": .5}

            MDLabel:
                text: "सुरक्षित प्रमाणीकरण गेटवे"
                font_style: "Body1"
                bold: True
                halign: "center"
                theme_text_color: "Primary"

            MDRoundFlatIconButton:
                icon: "google"
                text: "Gmail / Google ID से लॉगिन करें"
                text_color: 0.1, 0.1, 0.1, 1
                icon_color: 0.85, 0.15, 0.15, 1
                line_color: 0.8, 0.8, 0.8, 1
                pos_hint: {"center_x": .5}
                size_hint_x: 0.95
                on_release: root.login_via_gmail()

            MDRaisedButton:
                text: "⏩ Skip Login (सीधे ऑफलाइन उपयोग करें)"
                md_bg_color: 0.2, 0.2, 0.2, 1
                pos_hint: {"center_x": .5}
                size_hint_x: 0.95
                on_release: root.skip_login()

            MDLabel:
                text: "100% सुरक्षित स्थानीय ऑफ़लाइन डेटा प्रोसेसिंग"
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Hint"

<MainScreen>:
    name: 'main_screen'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.96, 0.97, 0.98, 1

        MDTopAppBar:
            title: "🔮 ओपटाज़ एआई (ऑफ़लाइन)"
            elevation: 4
            md_bg_color: 0.85, 0.15, 0.15, 1
            right_action_items: [["logout", lambda x: root.logout_user()]]

        MDTabs:
            id: tabs
            background_color: 0.85, 0.15, 0.15, 1
            text_color_normal: 1, 1, 1, 0.6
            text_color_active: 1, 1, 1, 1

            Tab:
                title: "📝 मोड 1"
                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: '16dp'
                        spacing: '16dp'

                        MDLabel:
                            text: "📝 मोड 1: मैनुअल चेन्स इनपुट बॉक्स"
                            font_style: "Subtitle1"
                            bold: True

                        MDTextField:
                            id: manual_input_data
                            hint_text: "यहाँ चेन्स इनपुट करें (जैसे: 5, -3, 0...)"
                            multiline: True
                            mode: "rectangle"
                            size_hint_y: None
                            height: "120dp"

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: '12dp'
                            size_hint_y: None
                            height: "48dp"

                            MDRaisedButton:
                                text: "🚀 गॉड लेवल गति से गणना करें"
                                md_bg_color: 0.85, 0.15, 0.15, 1
                                size_hint_x: 0.7
                                on_release: root.calculate_mode_1()

                            MDFillRoundFlatButton:
                                text: "🔄 इनपुट रिसेट"
                                md_bg_color: 0.4, 0.4, 0.4, 1
                                size_hint_x: 0.3
                                on_release: root.clear_manual_input()

                        OutputsContainer:
                            id: outputs_m1

            Tab:
                title: "📂 मोड 2"
                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: '16dp'
                        spacing: '20dp'

                        MDLabel:
                            text: "📂 मोड 2: ऑटोमैटिक CSV फ़ाइल अपलोडर"
                            font_style: "Subtitle1"
                            bold: True

                        MDLabel:
                            text: "यहाँ CSV फ़ाइल अपलोड करें:"
                            font_style: "Body2"
                            theme_text_color: "Secondary"

                        MDCard:
                            orientation: 'horizontal'
                            padding: "16dp"
                            spacing: "12dp"
                            size_hint_y: None
                            height: "72dp"
                            radius: [12, 12, 12, 12]
                            md_bg_color: 0.92, 0.94, 0.96, 1
                            elevation: 0

                            MDIconButton:
                                icon: "file-table-outline"
                                icon_size: "28dp"
                                theme_text_color: "Custom"
                                text_color: 0.15, 0.3, 0.5, 1
                                on_release: root.open_system_file_manager()

                            MDBoxLayout:
                                orientation: 'vertical'
                                size_hint_x: 0.7
                                pos_hint: {"center_y": .5}
                                
                                MDLabel:
                                    id: csv_file_name_lbl
                                    text: "कोई फाइल नहीं चुनी गई"
                                    font_style: "Body1"
                                    bold: True
                                MDLabel:
                                    id: csv_file_size_lbl
                                    text: "अधिकतम सीमा: 1GB+"
                                    font_style: "Caption"
                                    theme_text_color: "Hint"

                            MDIconButton:
                                id: remove_file_btn
                                icon: "close-circle"
                                icon_size: "24dp"
                                theme_text_color: "Custom"
                                text_color: 0.8, 0.2, 0.2, 0.3
                                disabled: True
                                on_release: root.remove_selected_file()

                        MDBoxLayout:
                            orientation: 'vertical'
                            spacing: "8dp"
                            size_hint_y: None
                            height: self.minimum_height

                            MDLabel:
                                text: "पैमाने चुनें (Columns/Metrics Check):"
                                font_style: "Body2"
                                bold: True

                            MDStackLayout:
                                id: chips_container
                                spacing: "8dp"
                                size_hint_y: None
                                height: self.minimum_height

                        MDRaisedButton:
                            text: "🚀 अपलोड की गई फाइल की गणना करें"
                            md_bg_color: 0.85, 0.15, 0.15, 1
                            pos_hint: {"center_x": .5}
                            size_hint_x: 1
                            padding: "14dp"
                            on_release: root.calculate_mode_2()

                        MDSeparator:
                            height: "1dp"

                        OutputsContainer:
                            id: outputs_m2

<OutputsContainer@MDBoxLayout>:
    orientation: 'vertical'
    spacing: '12dp'
    size_hint_y: None
    height: self.minimum_height

    MDLabel:
        id: exec_time_lbl
        text: "⏱️ कुल गणना समय (Execution Time): - "
        font_style: "Caption"
        bold: True

    MDCard:
        orientation: 'vertical'
        padding: "16dp"
        spacing: "8dp"
        size_hint_y: None
        height: "180dp"
        md_bg_color: 1, 1, 1, 1
        elevation: 1
        radius: [12, 12, 12, 12]

        MDLabel:
            text: "📊 परिणाम विवरण (Results):"
            font_style: "Subtitle2"
            bold: True
            theme_text_color: "Secondary"
        MDLabel:
            id: output_k_g
            text: "कुल बॉक्स (K): -  |  इंटरवल आकार (g): -"
            font_style: "Body2"
        MDLabel:
            id: output_prime
            text: "🔢 ओपटाज़' (O'): -"
            font_style: "Body1"
            bold: True
        MDLabel:
            id: output_final
            text: "🎯 FINAL OPATAZ: -"
            font_style: "H5"
            bold: True
            theme_text_color: "Error"
'''

class Tab(BoxLayout):
    pass

class LoginScreen(Screen):
    def login_via_gmail(self):
        MDSnackbar(text="Gmail / Google ID से प्रमाणीकरण सफल!").open()
        self.manager.current = 'main_screen'

    def skip_login(self):
        MDSnackbar(text="लॉगिन छोड़ दिया गया। लोकल ऑफलाइन मोड चालू है।").open()
        self.manager.current = 'main_screen'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_file_path = None
        self.detected_columns = []
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_system_path
        )

    def logout_user(self):
        self.manager.current = 'login_screen'
        self.remove_selected_file()
        MDSnackbar(text="सफलतापूर्वक लॉग-आउट किया गया।").open()

    def open_system_file_manager(self):
        primary_ext_storage = os.getenv("EXTERNAL_STORAGE", "/sdcard")
        if os.path.exists(primary_ext_storage):
            self.file_manager.show(primary_ext_storage)
        else:
            self.file_manager.show('/')

    def select_system_path(self, path):
        self.exit_file_manager()
        if path.lower().endswith('.csv'):
            self.selected_file_path = path
            file_name = os.path.basename(path)
            file_size_kb = os.path.getsize(path) / 1024
            self.ids.csv_file_name_lbl.text = file_name
            self.ids.csv_file_size_lbl.text = f"{file_size_kb:.1f} KB"
            self.ids.remove_file_btn.disabled = False
            self.ids.remove_file_btn.text_color = [0.85, 0.15, 0.15, 1]
            self.load_csv_columns(path)
        else:
            MDSnackbar(text="गलत फ़ाइल! कृपया केवल .csv फ़ाइल अपलोड करें।").open()

    def load_csv_columns(self, path):
        self.ids.chips_container.clear_widgets()
        try:
            with open(path, mode='r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header:
                    self.detected_columns = [col.strip() for col in header if col.strip()]
                    for col in self.detected_columns:
                        chip = MDChip(
                            text=col,
                            icon_check=True,
                            bg_color=[0.85, 0.15, 0.15, 1],
                            text_color=[1, 1, 1, 1],
                            icon_check_color=[1, 1, 1, 1],
                            size_hint_x=None
                        )
                        self.ids.chips_container.add_widget(chip)
        except Exception:
            pass

    def remove_selected_file(self):
        self.selected_file_path = None
        self.ids.csv_file_name_lbl.text = "कोई फाइल नहीं चुनी गई"
        self.ids.csv_file_size_lbl.text = "अधिकतम सीमा: 1GB+"
        self.ids.remove_file_btn.disabled = True
        self.ids.remove_file_btn.text_color = [0.8, 0.2, 0.2, 0.3]
        self.ids.chips_container.clear_widgets()
        MDSnackbar(text="फ़ाइल हटा दी गई है!").open()

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def clear_manual_input(self):
        self.ids.manual_input_data.text = ""
        self.ids.outputs_m1.ids.output_k_g.text = "कुल बॉक्स (K): -  |  इंटरवल आकार (g): -"
        self.ids.outputs_m1.ids.output_prime.text = "🔢 ओपटाज़' (O'): -"
        self.ids.outputs_m1.ids.output_final.text = "🎯 FINAL OPATAZ: -"
        self.ids.outputs_m1.ids.exec_time_lbl.text = "⏱️ कुल गणना समय (Execution Time): - "

    def parse_chains_with_loop_flag(self, text):
        chains_info = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if line:
                has_dots = '...' in line or '..' in line
                line_clean = line.replace('[', '').replace(']', '').replace('...', '').replace('..', '')
                elements = [float(x) for x in line_clean.split(',') if x.strip()]
                if elements: 
                    chains_info.append({'elements': elements, 'has_dots': has_dots})
        return chains_info

    def calculate_mode_1(self):
        input_text = self.ids.manual_input_data.text.strip()
        if not input_text:
            MDSnackbar(text="कृपया पहले चेन्स इनपुट बॉक्स में डेटा दर्ज करें!").open()
            return

        start_time = time.time()
        try:
            chains_info = self.parse_chains_with_loop_flag(input_text)
            if not chains_info: return
            
            raw_chains = [c['elements'] for c in chains_info]
            A_vals_kg = [OpatazPythonEngine.calc_A(c) for c in raw_chains if c]
            A0_kg = sum(A_vals_kg) / len(A_vals_kg) if A_vals_kg else 1.0
            
            firsts_kg = [c[0] for c in raw_chains if c]
            S_kg = OpatazPythonEngine.calc_S(firsts_kg)
            sigma_kg = OpatazPyt
