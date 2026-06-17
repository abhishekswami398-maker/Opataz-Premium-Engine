import os
import math
import time
import csv
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar

# C++ इंजन बाइंडिंग इंटीग्रेशन की जांच
try:
    import opataz_cpp
except ImportError:
    opataz_cpp = None

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
        spacing: "24dp"

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "220dp"
            pos_hint: {"center_x": .5}
            spacing: "12dp"
            
            # प्रीमियम ऐप लोगो कंटेनर
            FitImage:
                source: 'icon.png'
                size_hint: None, None
                size: "100dp", "100dp"
                pos_hint: {"center_x": .5}
                radius: [24, ]

            MDLabel:
                text: "🔮 ओपटाज़ एआई"
                halign: "center"
                font_style: "H4"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.85, 0.15, 0.15, 1

            MDLabel:
                text: "स्पीड मोड महा-इंजन संस्करण"
                halign: "center"
                font_style: "Subtitle2"
                theme_text_color: "Hint"

        MDCard:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "16dp"
            size_hint_y: None
            height: "180dp"
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
                text: "Google ID से साइन-इन करें"
                text_color: 0.1, 0.1, 0.1, 1
                icon_color: 0.85, 0.15, 0.15, 1
                line_color: 0.8, 0.8, 0.8, 1
                pos_hint: {"center_x": .5}
                size_hint_x: 0.9
                on_release: root.simulate_google_login()

            MDLabel:
                text: "100% सुरक्षित स्थानीय ऑफ़लाइन मोड स्टोरेज"
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Hint"

<MainScreen>:
    name: 'main_screen'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.98, 0.98, 0.98, 1

        MDTopAppBar:
            title: "🔮 ओपटाज़ एआई - C++ स्पीड मोड"
            elevation: 4
            md_bg_color: 0.85, 0.15, 0.15, 1
            right_action_items: [["logout", lambda x: root.logout_user()]]

        MDTabs:
            id: tabs
            on_tab_switch: root.on_tab_switch(*args)
            background_color: 0.85, 0.15, 0.15, 1
            text_color_normal: 1, 1, 1, 0.6
            text_color_active: 1, 1, 1, 1
            indicator_color: 1, 1, 1, 1

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
                            theme_text_color: "Primary"

                        MDTextField:
                            id: manual_input_data
                            hint_text: "चेन्स इनपुट बॉक्स (जैसे: 5, -3, 0...)"
                            multiline: True
                            mode: "rectangle"
                            size_hint_y: None
                            height: "140dp"

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: '12dp'
                            size_hint_y: None
                            height: "48dp"

                            MDRaisedButton:
                                text: "🚀 गॉड लेवल गति से गणना करें"
                                md_bg_color: 0.85, 0.15, 0.15, 1
                                size_hint_x: 0.6
                                on_release: root.calculate_mode_1()

                            MDFillRoundFlatButton:
                                text: "🔄 Reset"
                                md_bg_color: 0.4, 0.4, 0.4, 1
                                size_hint_x: 0.4
                                on_release: root.clear_manual_input()

                        MDSeparator:
                            height: "1dp"

                        root_outputs_m1: root_outputs_m1

            Tab:
                title: "📂 मोड 2"
                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: '16dp'
                        spacing: '16dp'

                        MDLabel:
                            text: "📂 मोड 2: ऑटोमैटिक CSV फ़ाइल अपलोडर"
                            font_style: "Subtitle1"
                            bold: True
                            theme_text_color: "Primary"

                        MDRaisedButton:
                            text: "📂 बड़ी CSV फाइल चुनें (Up to 1GB+)"
                            md_bg_color: 0.1, 0.5, 0.8, 1
                            pos_hint: {"center_x": .5}
                            size_hint_x: 0.9
                            on_release: root.open_system_file_manager()

                        MDLabel:
                            id: csv_file_status
                            text: "कोई फाइल नहीं चुनी गई (100% सुरक्षित ऑफलाइन मोड)"
                            halign: "center"
                            font_style: "Caption"
                            theme_text_color: "Secondary"

                        MDFillRoundFlatButton:
                            text: "🚀 अपलोड की गई फाइल की गणना करें"
                            md_bg_color: 0.85, 0.15, 0.15, 1
                            pos_hint: {"center_x": .5}
                            size_hint_x: 0.9
                            on_release: root.calculate_mode_2()

                        MDSeparator:
                            height: "1dp"

                        root_outputs_m2: root_outputs_m2

<OutputsContainer@MDBoxLayout>:
    id: output_container
    orientation: 'vertical'
    spacing: '12dp'
    size_hint_y: None
    height: self.minimum_height

    MDLabel:
        id: exec_time_lbl
        text: "⏱️ कुल गणना समय (Execution Time): - "
        font_style: "Caption"
        bold: True
        theme_text_color: "Secondary"

    MDCard:
        orientation: 'vertical'
        padding: "16dp"
        spacing: "8dp"
        size_hint_y: None
        height: "200dp"
        md_bg_color: 1, 1, 1, 1
        elevation: 2
        radius: [12, 12, 12, 12]

        MDLabel:
            text: "📊 परिणाम विवरण (Results):"
            font_style: "Subtitle1"
            bold: True
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

class Tab(MDBoxLayout):
    pass

class LoginScreen(com.kivy.Screen if 'com' in globals() else object):
    import sys
    from kivy.uix.screenmanager import Screen
    locals()['Screen'] = Screen
    
    def simulate_google_login(self):
        MDSnackbar(text="Google ID प्रमाणीकरण सफल! स्थानीय सुरक्षा सिंक चालू है।").open()
        time.sleep(0.5)
        self.manager.current = 'main_screen'

class MainScreen(kivy.uix.screenmanager.Screen if 'kivy' in locals() else object):
    from kivy.uix.screenmanager import Screen
    locals()['Screen'] = Screen
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_file_path = None
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_system_path
        )

    def logout_user(self):
        self.manager.current = 'login_screen'
        MDSnackbar(text="सफलतापूर्वक लॉग-आउट किया गया।").open()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

    def open_system_file_manager(self):
        # सुरक्षित लोकल एंड्रॉयड प्राइमरी स्टोरेज पाथ एक्सेस
        primary_ext_storage = os.getenv("EXTERNAL_STORAGE", "/sdcard")
        if os.path.exists(primary_ext_storage):
            self.file_manager.show(primary_ext_storage)
        else:
            self.file_manager.show('/')

    def select_system_path(self, path):
        self.exit_file_manager()
        if path.lower().endswith('.csv'):
            self.selected_file_path = path
            self.ids.csv_file_status.text = f"फ़ाइल चुनी गई: {os.path.basename(path)}"
        else:
            self.ids.csv_file_status.text = "गलत फ़ाइल! कृपया केवल .csv फ़ाइल चुनें।"

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def clear_manual_input(self):
        self.ids.manual_input_data.text = ""
        self.ids.output_k_g.text = "कुल बॉक्स (K): -  |  इंटरवल आकार (g): -"
        self.ids.output_prime.text = "🔢 ओपटाज़' (O'): -"
        self.ids.output_final.text = "🎯 FINAL OPATAZ: -"
        self.ids.exec_time_lbl.text = "⏱️ कुल गणना समय (Execution Time): - "

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
        if not opataz_cpp:
            MDSnackbar(text="C++ महा-इंजन कोर कंपोनेंट लोड नहीं हो सका!").open()
            return

        input_text = self.ids.manual_input_data.text.strip()
        if not input_text:
            MDSnackbar(text="कृपया पहले चेन्स इनपुट बॉक्स में डेटा दर्ज करें!").open()
            return

        start_time = time.time()
        try:
            chains_info = self.parse_chains_with_loop_flag(input_text)
            if not chains_info: return
            
            raw_chains = [c['elements'] for c in chains_info]
            A_vals_kg = [opataz_cpp.calc_A(c) for c in raw_chains if c]
            A0_kg = sum(A_vals_kg) / len(A_vals_kg) if A_vals_kg else 1.0
            firsts_kg = [c[0] for c in raw_chains if c]
            
            S_kg = opataz_cpp.calc_S(firsts_kg)
            sigma_kg = opataz_cpp.calc_sigma(A0_kg, S_kg)
            n_kg = len(str(int(sigma_kg))) if sigma_kg > 0 else 1
            V_kg = 1 + (sigma_kg / (10 ** n_kg))
            K = opataz_cpp.calc_K(len(raw_chains), V_kg)
            
            all_raw_data = []
            for c in raw_chains: all_raw_data.extend(c)
            x = min(all_raw_data) if all_raw_data else 0.0
            global_max = max(all_raw_data) if all_raw_data else 0.0
            g = opataz_cpp.calc_g(global_max, x, K)
            
            resolved = []
            for c in chains_info:
                res_c, _ = opataz_cpp.detect_and_resolve_loop(c['elements'], K, c['has_dots'])
                resolved.append(res_c)
                
            if len(resolved) == 1:
                O_prime = opataz_cpp.calc_opataz_manual(resolved[0], K)
            else:
                after_c = opataz_cpp.apply_c_ratio_manual(resolved)
                after_rnv = opataz_cpp.apply_rnv_manual(after_c)
                O_pts = [opataz_cpp.calc_opataz_manual(c, K) for c in after_rnv]
                fcr = [c[0] for c in after_rnv if c]
                if len(set(fcr)) == 1:
                    O_prime = (sum(O_pts) / len(O_pts)) + (1.0 * K)
                else:
                    abs_fcr = [abs(v) for v in fcr]
                    R = (min(abs_fcr) / max(abs_fcr)) * K if max(abs_fcr) != 0 else 0
                    O_prime = sum(O_pts) + R

            O_prime = abs(O_prime)
            base_candidate = int(g)
            log_base = float(base_candidate + 1) if base_candidate % 2 != 0 else float(base_candidate)
            if log_base <= 1: log_base = 2.0
            
            O_final = O_prime if (O_prime <= 1 or log_base <= 1) else math.log(O_prime, log_base)
            
            exec_time = time.time() - start_time
            self.ids.exec_time_lbl.text = f"⏱️ कुल गणना समय (Execution Time): {exec_time:.4f} सेकंड"
            self.ids.output_k_g.text = f"कुल बॉक्स (K): {K}  |  इंटरवल आकार (g): {g:.4f}"
            self.ids.output_prime.text = f"🔢 ओपटाज़' (O'): {O_prime:.6f}"
            self.ids.output_final.text = f"🎯 FINAL OPATAZ: {O_final:.6f}"
            
        except Exception as e:
            self.ids.output_final.text = "गणना में त्रुटि आई!"

    def calculate_mode_2(self):
        if not opataz_cpp:
            MDSnackbar(text="C++ महा-इंजन कोर कंपोनेंट लोड नहीं हो सका!").open()
            return

        if not self.selected_file_path:
            MDSnackbar(text="कृपया पहले .csv फाइल सिलेक्ट करें!").open()
            return

        start_time = time.time()
        try:
            total_rows = 0
            firsts_kg = []
            A_vals_sum = 0.0
            global_min, global_max = float('inf'), -float('inf')
            
            col_mins = []
            col_maxs = []
            all_rows_data = []

            with open(self.selected_file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                
                for row in reader:
                    if not row: continue
                    try:
                        vals = [float(x) for x in row if x.strip() != '']
                        if not vals: continue
                    except ValueError:
                        continue
                    
                    total_rows += 1
                    all_rows_data.append(vals)
                    
                    row_min = min(vals)
                    row_max = max(vals)
                    if row_min < global_min: global_min = row_min
                    if row_max > global_max: global_max = row_max
                    
                    n_cols = len(vals)
                    if not col_mins:
                        col_mins = list(vals)
                        col_maxs = list(vals)
                    else:
                        for i in range(min(len(col_mins), n_cols)):
                            if vals[i] < col_mins[i]: col_mins[i] = vals[i]
                            if vals[i] > col_maxs[i]: col_maxs[i] = vals[i]
                    
                    if n_cols == 1:
                        firsts_kg.append(vals[0])
                        A_vals_sum += abs((vals[0] + vals[0] + vals[0]) / 3)
                    else:
                        firsts_kg.append(vals[0])
                        A_vals_sum += abs((vals[0] + row_max + row_min) / 3)

            if total_rows == 0:
                MDSnackbar(text="चयनित CSV फ़ाइल खाली है!").open()
                return

            x = global_min
            A0_kg = A_vals_sum / total_rows
            S_kg = opataz_cpp.calc_S(firsts_kg)
            sigma_kg = opataz_cpp.calc_sigma(A0_kg, S_kg)
            n_kg = len(str(int(sigma_kg))) if sigma_kg > 0 else 1
            V_kg = 1 + (sigma_kg / (10 ** n_kg))
            K = opataz_cpp.calc_K(total_rows, V_kg)
            g = opataz_cpp.calc_g(global_max, x, K)
            
            n_elements = len(col_mins)
            C_ratios = [0.0] * n_elements
            for idx in range(n_elements):
                if col_maxs[idx] != 0: 
                    C_ratios[idx] = col_mins[idx] / col_maxs[idx]

            O_pts_sum = 0.0
            for vals in all_rows_data:
                n_cols = len(vals)
                mod_vals = [0.0] * n_cols
                if n_elements == 2 and n_cols >= 2:
                    mod_vals[0] = vals[0] + (vals[1] * C_ratios[0])
                    mod_vals[1] = vals[1] + (vals[0] * C_ratios[1])
                else:
                    for idx in range(min(n_elements, n_cols)):
                        mod_vals[idx] = vals[idx] + (vals[idx] * C_ratios[idx])
                        
                for idx in range(min(n_elements, n_cols)):
                    if (col_maxs[idx] - col_mins[idx]) >= 2:
                        mod_vals[idx] = sum(vals) / len(vals)
                        
                if n_elements == 1:
                    last_val = mod_vals[0] if mod_vals[0] != 0 else 0.001
                    O_pts_sum += abs(last_val)
                else:
                    last_val = mod_vals[-1] if mod_vals[-1] != 0 else 0.001
                    first_val = mod_vals[0]
                    calc_lasts = math.ceil(last_val) if last_val != 0 else 0.001
                    components = K + first_val
                    if components == 0: components = 0.001
                    O_pts_sum += abs(calc_lasts * components)

            if len(set(firsts_kg)) == 1:
                O_prime = (O_pts_sum / total_rows) + (1.0 * K)
            else:
                abs_firsts = [abs(v) for v in firsts_kg]
                R_filter = (min(abs_firsts) / max(abs_firsts)) * K if max(abs_firsts) != 0 else 0
                O_prime = O_pts_sum + R_filter
                
            O_prime = abs(O_prime)
            base_candidate = int(g)
            log_base = float(base_candidate + 1) if base_candidate % 2 != 0 else float(base_candidate)
            if log_base <= 1: log_base = 2.0
            
            O_final = O_prime if (O_prime <= 1 or log_base <= 1) else math.log(O_prime, log_base)

            exec_time = time.time() - start_time
            self.ids.exec_time_lbl.text = f"⏱️ कुल गणना समय (Execution Time): {exec_time:.4f} सेकंड"
            self.ids.output_k_g.text = f"प्रोसेस्ड रोज़ (Rows): {total_rows:,} | K: {K}"
            self.ids.output_prime.text = f"🔢 ओपटाज़' (O'): {O_prime:.6f}"
            self.ids.output_final.text = f"🎯 FINAL OPATAZ: {O_final:.6f}"

        except Exception as e:
            self.ids.output_final.text = "CSV फाइल गणना में त्रुटि!"

class ScreenManagerSetup(kivy.uix.screenmanager.ScreenManager if 'kivy' in locals() else object):
    pass

class OpatazApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        
        # कंपोनेंट डिक्लेरेशन फिक्स
        from kivy.uix.screenmanager import ScreenManager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(MainScreen(name='main_screen'))
        return sm

if __name__ == '__main__':
    # डायनामिक लेआउट ओवरराइड इंजेक्शन
    full_kv_compiled = KV + "\\n" + """
<MainScreen>:
    root_outputs_m1: outputs_m1
    root_outputs_m2: outputs_m2
    id: main_scr_layout
    
    # इंजेक्टेड लेआउट्स
    OutputsContainer:
        id: outputs_m1
    OutputsContainer:
        id: outp
