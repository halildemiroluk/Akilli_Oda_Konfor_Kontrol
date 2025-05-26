import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdi ve çıktı tanımları
temp = ctrl.Antecedent(np.arange(10, 41, 1), 'temp')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
co2 = ctrl.Antecedent(np.arange(400, 2001, 100), 'co2')
light = ctrl.Antecedent(np.arange(0, 1001, 50), 'light')
noise = ctrl.Antecedent(np.arange(20, 101, 5), 'noise')

ac_level = ctrl.Consequent(np.arange(0, 11, 1), 'ac_level')
ac_level.defuzzify_method = 'centroid'

window_open = ctrl.Consequent(np.arange(0, 101, 1), 'window_open')
window_open.defuzzify_method = 'mom'

# Üyelik fonksiyonları
temp['low'] = fuzz.trimf(temp.universe, [10, 10, 20])
temp['comfortable'] = fuzz.trimf(temp.universe, [18, 24, 28])
temp['high'] = fuzz.trimf(temp.universe, [26, 40, 40])

humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 30])
humidity['normal'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 100, 100])

co2['low'] = fuzz.trimf(co2.universe, [400, 400, 800])
co2['medium'] = fuzz.trimf(co2.universe, [700, 1000, 1300])
co2['high'] = fuzz.trimf(co2.universe, [1200, 2000, 2000])

light['dim'] = fuzz.trimf(light.universe, [0, 0, 300])
light['normal'] = fuzz.trimf(light.universe, [200, 500, 800])
light['bright'] = fuzz.trimf(light.universe, [700, 1000, 1000])

noise['low'] = fuzz.trimf(noise.universe, [20, 20, 40])
noise['moderate'] = fuzz.trimf(noise.universe, [35, 60, 75])
noise['high'] = fuzz.trimf(noise.universe, [70, 100, 100])

ac_level['off'] = fuzz.trimf(ac_level.universe, [0, 0, 3])
ac_level['medium'] = fuzz.trimf(ac_level.universe, [2, 5, 8])
ac_level['high'] = fuzz.trimf(ac_level.universe, [7, 10, 10])

window_open['closed'] = fuzz.trimf(window_open.universe, [0, 0, 20])
window_open['partly'] = fuzz.trimf(window_open.universe, [20, 60, 90])
window_open['fully'] = fuzz.trimf(window_open.universe, [85, 100, 100])

# Kurallar
rules = [
    ctrl.Rule(temp['high'] | noise['high'], ac_level['high']),
    ctrl.Rule(temp['comfortable'] & noise['moderate'], ac_level['medium']),
    ctrl.Rule(temp['low'], ac_level['off']),
    ctrl.Rule(humidity['low'], ac_level['off']),
    ctrl.Rule(humidity['high'] & temp['high'], ac_level['high']),
    ctrl.Rule(co2['high'], window_open['fully']),
    ctrl.Rule(co2['medium'], window_open['partly']),
    ctrl.Rule(co2['low'], window_open['closed']),
    ctrl.Rule(light['dim'], window_open['partly']),
    ctrl.Rule(light['bright'], window_open['closed']),
    ctrl.Rule(noise['high'], window_open['closed']),
]

system = ctrl.ControlSystem(rules)

# Arayüz
pencere = tk.Tk()
pencere.title("Ortam Konfor Kontrol Sistemi")
pencere.configure(bg="#1c2331")

label_fg = "#e0f2f1"
entry_bg = "#37474f"
entry_fg = "#ffffff"
font_label = ("Arial", 10, "bold")

# Girdi bileşenleri
girdiler = {}

def create_input_row(label_text, row, from_, to_, step):
    tk.Label(pencere, text=label_text, bg=pencere['bg'], fg=label_fg, font=font_label).grid(row=row, column=0, padx=10, pady=6, sticky="e")

    scale = tk.Scale(pencere, from_=from_, to=to_, resolution=step, orient=tk.HORIZONTAL,
                     length=200, bg=entry_bg, fg=entry_fg, highlightbackground=entry_bg)
    scale.grid(row=row, column=1, padx=10, pady=6)

    entry = tk.Entry(pencere, bg=entry_bg, fg=entry_fg, width=6, justify='center')
    entry.grid(row=row, column=2, padx=5)

    def update_scale(val):
        try:
            v = float(val)
            if from_ <= v <= to_:
                scale.set(v)
        except:
            pass

    def update_entry(val):
        entry.delete(0, tk.END)
        entry.insert(0, str(val))

    entry.bind("<KeyRelease>", lambda e: update_scale(entry.get()))
    scale.config(command=update_entry)

    return scale

girdiler['temp'] = create_input_row("Sıcaklık (°C)", 0, 10, 40, 1)
girdiler['humidity'] = create_input_row("Nem (%)", 1, 0, 100, 1)
girdiler['co2'] = create_input_row("CO₂ (ppm)", 2, 400, 2000, 100)
girdiler['light'] = create_input_row("Işık (lux)", 3, 0, 1000, 50)
girdiler['noise'] = create_input_row("Gürültü (dB)", 4, 20, 100, 5)

sonuc_label = tk.Label(pencere, text="", bg=pencere['bg'], fg="#80e27e", font=("Arial", 11, "bold"))
sonuc_label.grid(row=6, column=0, columnspan=3, pady=10)

def hesapla():
    try:
        sim = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)
        for key, scale in girdiler.items():
            sim.input[key] = scale.get()
        sim.compute()

        sonuc = f"🌬 Klima Seviyesi: {sim.output['ac_level']:.2f} / 10\n"
        sonuc += f"🪟 Pencere Açıklığı: %{sim.output['window_open']:.2f}"
        sonuc_label.config(text=sonuc)

    except Exception as e:
        messagebox.showerror("Hata", str(e))

def grafik_goster():
    grafik_pencere = tk.Toplevel(pencere)
    grafik_pencere.title("Üyelik Fonksiyonları")
    grafik_pencere.configure(bg="#1c2331")

    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    axs = axs.flatten()

    variables = [
        (temp, "Sıcaklık (°C)"),
        (humidity, "Nem (%)"),
        (co2, "CO₂ (ppm)"),
        (light, "Işık (lux)"),
        (noise, "Gürültü (dB)"),
        (ac_level, "Klima Seviyesi"),
        (window_open, "Pencere Açıklığı (%)")
    ]

    for i, (var, title) in enumerate(variables):
        ax = axs[i]
        for term_name, mf in var.terms.items():
            ax.plot(var.universe, mf.mf, label=term_name)
        ax.set_title(title, color='#80deea')
        ax.set_xlabel("Değerler", color='white')
        ax.set_ylabel("Üyelik", color='white')
        ax.legend()
        ax.grid(True)
        ax.set_facecolor('#263238')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

    # Kalan boş grafik alanlarını sil
    for j in range(len(variables), len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=grafik_pencere)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_rules():
    rule_texts = []
    for i, rule in enumerate(rules):
        rule_texts.append(f"Kural {i+1}: {rule}")

    rule_window = tk.Toplevel(pencere)
    rule_window.title("Kurallar")
    rule_window.configure(bg="#1c2331")

    text_widget = tk.Text(rule_window, wrap=tk.WORD, bg="#263238", fg="#e0f2f1", font=("Arial", 10), width=80, height=25)
    text_widget.pack(padx=10, pady=10)

    for rule in rule_texts:
        text_widget.insert(tk.END, rule + "\n\n")

    text_widget.config(state=tk.DISABLED)

# Butonlar
btn_hesapla = tk.Button(pencere, text="Hesapla", command=hesapla, bg="#00acc1", fg="#ffffff",
                        activebackground="#26c6da", font=("Arial", 11, "bold"), relief="raised", bd=3)
btn_hesapla.grid(row=5, column=0, columnspan=3, pady=10, ipadx=10, ipady=4)

btn_grafik = tk.Button(pencere, text="Grafikleri Göster", command=grafik_goster, bg="#8e24aa", fg="#ffffff",
                       activebackground="#ba68c8", font=("Arial", 11, "bold"))
btn_grafik.grid(row=7, column=0, columnspan=3, pady=(5, 0), ipadx=10, ipady=4)

btn_kurallar = tk.Button(pencere, text="Kuralları Göster", command=show_rules, bg="#43a047", fg="#ffffff",
                         activebackground="#66bb6a", font=("Arial", 11, "bold"))
btn_kurallar.grid(row=8, column=0, columnspan=3, pady=(5, 15), ipadx=10, ipady=4)

pencere.mainloop()
