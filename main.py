import os
import math
import time
import pandas as pd
import numpy as np
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager

# C++ इंजन को जोड़ने की जांच
try:
    import opataz_cpp
except ImportError:
    opataz_cpp = None

# मोबाइल स्क्रीन का सुंदर डिज़ाइन (Buttons और Boxes)
KV = '''
BoxLayout:
    orientation: 'vertical'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDTopAppBar:
        title: "🔮 ओपटाज़ एआई - ऑफलाइन मोड"
        elevation: 4
        md_bg_color: 0.85, 0.15, 0.15, 1
        pos_hint: {"top": 1}

    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: '16dp'
            spacing: '16dp'

            # --- पहला विकल्प (मोड 1) ---
            MDLabel:
                text: "विकल्प 1: मैन्युअल चेन्स इनपुट बॉक्स"
                font_style: "H6"
                bold: True

            MDTextField:
                id: input_data
                hint_text: "यहाँ अपनी चेन्स डालें (जैसे: 2, 3, 2..)"
                multiline: True
                mode: "rectangle"
                size_hint_y: None
                height: "140dp"

            MDFillRoundFlatButton:
                text: "🔄 डेटा साफ़ करें (Reset)"
                md_bg_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .5}
                on_release: app.clear_input()

            MDSeparator:
                height: "2dp"

            # --- दूसरा विकल्प (मोड 2) ---
            MDLabel:
                text: "विकल्प 2: ऑटोमैटिक CSV फ़ाइल अपलोडर"
                font_style: "H6"
                bold: True

            MDRaisedButton:
                text: "📂 बड़ी CSV फाइल चुनें (Up to 1GB+)"
                md_bg_color: 0.1, 0.5, 0.8, 1
                pos_hint: {"center_x": .5}
                on_release: app.open_file_manager()

            MDLabel:
                id: file_status
                text: "कोई फाइल नहीं चुनी गई (100% सुरक्षित ऑफलाइन मोड)"
                halign: "center"
                font_style: "Caption"

            # --- गणना करने का मुख्य बटन ---
            MDFillRoundFlatButton:
                text: "🚀 गॉड गति से गणना करें"
                font_style: "Button"
                md_bg_color: 0.85, 0.15, 0.15, 1
                pos_hint: {"center_x": .5}
                size_hint_x: 0.8
                on_release: app.calculate_opataz()

            # --- परिणाम बॉक्स ---
            MDCard:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "8dp"
                size_hint_y: None
                height: "180dp"
                md_bg_color: 1, 1, 1, 1
                elevation: 2
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "📊 परिणाम (Results):"
                    font_style: "Subtitle1"
                    bold: True
                MDLabel:
                    id: output_k_g
                    text: "कुल बॉक्स (K): -  |  साइज़ (g): -"
                    font_style: "Body1"
                MDLabel:
                    id: output_prime
                    text: "ओपटाज़' (O'): -"
                    font_style: "Body1"
                MDLabel:
                    id: output_final
                    text: "FINAL OPATAZ: -"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Error"
'''

class OpatazApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        self.selected_file_path = None
        return Builder.load_string(KV)

    def clear_input(self):
        self.root.ids.input_data.text = ""
        self.selected_file_path = None
        self.root.ids.file_status.text = "डेटा साफ़ कर दिया गया है।"

    def open_file_manager(self):
        # फोन का इंटरनल स्टोरेज खोलेगा
        self.file_manager.show('/') 

    def select_path(self, path):
        self.exit_manager()
        if path.lower().endswith('.csv'):
            self.selected_file_path = path
            self.root.ids.file_status.text = f"फ़ाइल चुनी गई: {os.path.basename(path)}"
            self.root.ids.input_data.text = "" 
        else:
            self.root.ids.file_status.text = "गलत फ़ाइल! कृपया केवल .csv फ़ाइल चुनें।"

    def exit_manager(self, *args):
        self.file_manager.close()

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

    def calculate_opataz(self):
        if not opataz_cpp:
            self.root.ids.output_final.text = "C++ इंजन लोड नहीं हो सका!"
            return

        input_text = self.root.ids.input_data.text.strip()
        
        # --- विकल्प 1: मैन्युअल चेन्स की गणना (आपका असली C++ लॉजिक) ---
        if input_text:
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
                
                self.root.ids.output_k_g.text = f"कुल बॉक्स (K): {K}  |  साइज़ (g): {g:.4f}"
                self.root.ids.output_prime.text = f"ओपटाज़' (O'): {O_prime:.6f}"
                self.root.ids.output_final.text = f"FINAL OPATAZ: {O_final:.6f}"
                
            except Exception as e:
                self.root.ids.output_final.text = "गणना में त्रुटि आई!"

        # --- विकल्प 2: बड़ी CSV फ़ाइल (1GB तक) की पूरी तरह ऑफलाइन सुरक्षित गणना ---
        elif self.selected_file_path:
            try:
                chunk_size = 200000
                total_rows = 0
                firsts_kg = []
                A_vals_sum = 0.0
                global_min, global_max = float('inf'), -float('inf')
                col_mins, col_maxs = None, None
                all_chunks_raw = []

                # सुरक्षित मेमोरी मैनेजमेंट के साथ फ़ाइल रीड करना (आपका ओरिजिनल लॉजिक)
                for chunk in pd.read_csv(self.selected_file_path, chunksize=chunk_size, on_bad_lines='skip'):
                    chunk_clean = chunk.apply(pd.to_numeric, errors='coerce').dropna()
                    if chunk_clean.empty: continue
                    vals = chunk_clean.values.astype(np.float64)
                    total_rows += len(vals)
                    all_chunks_raw.append(vals)
                    
                    if vals.min() < global_min: global_min = vals.min()
                    if vals.max() > global_max: global_max = vals.max()
                    
                    if col_mins is None:
                        col_mins, col_maxs = vals.min(axis=0), vals.max(axis=0)
                    else:
                        col_mins = np.minimum(col_mins, vals.min(axis=0))
                        col_maxs = np.maximum(col_maxs, vals.max(axis=0))
                        
                    if vals.shape[1] == 1:
                        flat_vals = vals.flatten()
                        firsts_kg.extend(flat_vals.tolist())
                        A_vals_sum += np.sum(np.abs((flat_vals + flat_vals + flat_vals) / 3))
                    else:
                        firsts_kg.extend(vals[:, 0].tolist())
                        A_vals_sum += np.sum(np.abs((vals[:, 0] + vals.max(axis=1) + vals.min(axis=1)) / 3))

                if total_rows == 0:
                    self.root.ids.output_final.text = "फ़ाइल खाली है!"
                    return

                x = global_min
                A0_kg = A_vals_sum / total_rows
                S_kg = opataz_cpp.calc_S(firsts_kg)
                sigma_kg = opataz_cpp.calc_sigma(A0_kg, S_kg)
                n_kg = len(str(int(sigma_kg))) if sigma_kg > 0 else 1
                V_kg = 1 + (sigma_kg / (10 ** n_kg))
                K = opataz_cpp.calc_K(total_rows, V_kg)
                g = opataz_cpp.calc_g(global_max, x, K)
                
                n_elements = col_mins.shape[0]
                C_ratios = np.zeros(n_elements, dtype=np.float64)
                for idx in range(n_elements):
                    if col_maxs[idx] != 0: C_ratios[idx] = col_mins[idx] / col_maxs[idx]

                O_pts_sum = 0.0
                for vals in all_chunks_raw:
                    mod_vals = np.zeros_like(vals)
                    if n_elements == 2:
                        mod_vals[:, 0] = vals[:, 0] + (vals[:, 1] * C_ratios[0])
                        mod_vals[:, 1] = vals[:, 1] + (vals[:, 0] * C_ratios[1])
                    else:
                        for idx in range(n_elements): 
                            mod_vals[:, idx] = vals[:, idx] + (vals[:, idx] * C_ratios[idx])
                            
                    for idx in range(n_elements):
                        if (col_maxs[idx] - col_mins[idx]) >= 2: 
                            mod_vals[:, idx] = vals[:, idx].mean()
                            
                    if n_elements == 1:
                        lasts = mod_vals.flatten()
                        lasts = np.where(lasts == 0, 0.001, lasts)
                        O_pts_sum += np.sum(np.abs(lasts))
                    else:
                        lasts = mod_vals[:, -1]
                        firsts = mod_vals[:, 0]
                        calc_lasts = np.where(lasts == 0, 0.001, np.ceil(lasts))
                        components = K + firsts
                        components = np.where(components == 0, 0.001, components)
                        O_pts_sum += np.sum(np.abs(calc_lasts * components))

                if len(set(firsts_kg)) == 1:
                    O_prime = (O_pts_sum / total_rows) + (1.0 * K)
                else:
                    abs_firsts = np.abs(np.array(firsts_kg, dtype=np.float64))
                    R_filter = (abs_firsts.min() / abs_firsts.max()) * K if abs_firsts.max() != 0 else 0
                    O_prime = O_pts_sum + R_filter
                    
                O_prime = abs(O_prime)
                base_candidate = int(g)
                log_base = float(base_candidate + 1) if base_candidate % 2 != 0 else float(base_candidate)
                if log_base <= 1: log_base = 2.0
                
                O_final = O_prime if (O_prime <= 1 or log_base <= 1) else math.log(O_prime, log_base)

                self.root.ids.output_k_g.text = f"प्रोसेस्ड रोज़ (Rows): {total_rows:,} | K: {K}"
                self.root.ids.output_prime.text = f"ओपटाज़' (O'): {O_prime:.6f}"
                self.root.ids.output_final.text = f"FINAL OPATAZ: {O_final:.6f}"

            except Exception as e:
                self.root.ids.output_final.text = "CSV फाइल गणना में त्रुटि!"
        else:
            self.root.ids.output_final.text = "कृपया इनपुट दें या फ़ाइल चुनें!"

if __name__ == '__main__':
    OpatazApp().run()
            
