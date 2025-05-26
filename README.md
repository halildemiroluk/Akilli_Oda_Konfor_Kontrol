
# 🛑 Ortam Konfor Kontrol Sistemi
Bu proje, ortam sıcaklığı, nem, CO₂ seviyesi, ışık ve gürültü gibi çevresel faktörleri dikkate alarak, bulanık mantık (fuzzy logic) kullanarak ortam konforunu artırmak için klima seviyesi ve pencere açıklığını otomatik olarak öneren bir kontrol sistemidir.

# 🔧 Kullanılan Teknolojiler
- Python
- Tkinter (GUI)
- scikit-fuzzy (bulanık mantık motoru)
- matplotlib (grafik çizimi)
- numpy (Sayısal Hesaplamalar)

# Özellikler

- Sıcaklık (10-40 °C)

- Nem (%0 - %100)

- CO₂ (400-2000 ppm)

- Işık Seviyesi (0-1000 lux)

- Gürültü Seviyesi (20-100 dB)

- 2 adet çıktı üretir:

- Klima Seviyesi (0-10 arası)

- Pencere Açıklığı (%0 - %100 arası)

- 10 adet bulanık kural içerir

- Üyelik fonksiyonlarını grafik olarak görselleştirme

- Kuralları ayrı bir pencerede metin olarak gösterme

# 📁 Dosya İçeriği
1. Gerekli Kütüphanelerin İmport Edilmesi
```python

import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

```

2. Bulanık Değişkenlerin Tanımlanması
Girdi (antecedent) ve çıktı (consequent) değişkenleri oluşturulur:
```python

temperature = ctrl.Antecedent(np.arange(10, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
co2 = ctrl.Antecedent(np.arange(400, 2001, 50), 'co2')
light = ctrl.Antecedent(np.arange(0, 1001, 50), 'light')
noise = ctrl.Antecedent(np.arange(20, 101, 5), 'noise')

ac_level = ctrl.Consequent(np.arange(0, 11, 1), 'ac_level')
window_opening = ctrl.Consequent(np.arange(0, 101, 1), 'window_opening')

```

3. Üyelik Fonksiyonlarının Tanımlanması
Her değişken için üyelik (membership) fonksiyonları tanımlanır:
```python

temperature['low'] = fuzz.trimf(temperature.universe, [10, 10, 22])
temperature['medium'] = fuzz.trimf(temperature.universe, [18, 25, 32])
temperature['high'] = fuzz.trimf(temperature.universe, [28, 40, 40])
# Diğer değişkenler için de benzer üyelik fonksiyonları tanımlanır

```
4. Bulanık Kuralların Tanımlanması
Sistem, sürücü durumu hakkında karar vermek için kurallara dayanır:
```python

rules = [
    ctrl.Rule(temperature['high'] | noise['high'], ac_level['high']),
    ctrl.Rule(co2['high'], window_opening['high']),
    ctrl.Rule(light['low'] & co2['medium'], window_opening['medium']),
    # Diğer kurallar...
]

```

5. Kontrol Sistemi Tanımlanması
```python

system = ctrl.ControlSystem(rules)
simulation = ctrl.ControlSystemSimulation(system)

```

6. Tkinter Arayüzünün Oluşturulması
Ana pencere yapılandırılır:
```python

window = tk.Tk()
window.title("Ortam Konfor Kontrol Sistemi")
window.configure(bg="#1e1e2f")

# Örnek: sıcaklık için kaydırıcı oluşturulur
temperature_scale = tk.Scale(window, from_=10, to=40, orient=tk.HORIZONTAL, label="Sıcaklık (°C)")
temperature_scale.pack()
# Diğer parametreler için de benzer kaydırıcılar oluşturulur

```

8. Hesaplama Fonksiyonu
Kullanıcıdan alınan girdilerle sistem çalıştırılır ve sonuç gösterilir:
```python

def hesapla():
    simulation.input['temperature'] = temperature_scale.get()
    simulation.input['humidity'] = humidity_scale.get()
    simulation.input['co2'] = co2_scale.get()
    simulation.input['light'] = light_scale.get()
    simulation.input['noise'] = noise_scale.get()
    simulation.compute()

    sonuc = f"Klima Seviyesi: {simulation.output['ac_level']:.2f}\n"
    sonuc += f"Pencere Açıklığı: {simulation.output['window_opening']:.2f}%"
    messagebox.showinfo("Sonuç", sonuc)

```

9. Grafik Gösterimi
Üyelik fonksiyonlarını matplotlib ile gösterir:
```python

def grafik_goster():
    fig, ax = plt.subplots()
    temperature.view(ax=ax)
    plt.show()


```

10. Kuralların Gösterimi
Kural listesini ayrı bir pencerede metin kutusunda gösterir:
```python

def kurallar_goster():
    kural_pencere = Toplevel(window)
    metin = Text(kural_pencere)
    for i, rule in enumerate(rules):
        metin.insert(tk.END, f"Kural {i+1}: {rule}\n\n")
    metin.pack()


```

11. Butonların Oluşturulması
Arayüzün altına işlem butonları yerleştirilir:
```python

def kurallar_goster():
    kural_pencere = Toplevel(window)
    metin = Text(kural_pencere)
    for i, rule in enumerate(rules):
        metin.insert(tk.END, f"Kural {i+1}: {rule}\n\n")
    metin.pack()


```

12. Arayüzün Başlatılması
```python

window.mainloop()


```


# 📝 Notlar
Eğer gerekli kütüphaneler yüklü değilse aşağıdaki komutla yüklenebilir:
```python

pip install numpy matplotlib scikit-fuzzy scipy networkx

```
- Arayüz sade tutulmuştur ve sezgiseldir.

# 🚀 Projeyi Çalıştırma
Aşağıdaki adımları takip ederek projeyi bilgisayarınıza indirip çalıştırabilirsiniz:
- Projeyi GitHub'dan klonla
```python

git clone https://github.com/halildemiroluk/Akilli_Oda_Konfor_Kontrol.git

```
- Proje klasörüne geç
```python

cd Akilli_Oda_Konfor_Kontrol

```

- Programı çalıştır
```python

python main.py

```
