# The model is valid for frequencies in the 300-3 000 MHz range. The model is based on measurements
# made with antenna heights between 1.9 and 3.0 m above ground, and transmitter-receiver distances
# up to 3 000 m
from tkinter import ttk
import customtkinter as ctk
from statistics import NormalDist
import math
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_general_below_rooftop_to_street():
    root = ctk.CTk()
    root.geometry("600x350")
    root.title("Site General for below rooftop to street level")
    root.config(bg="#FFF8EA")

    path_loss = 0
    l_urban = 0

    urban_category = [
        "urban",
        "suburban",
        "dense urban/high-rise"
    ]

    def e_click(event):
        nonlocal l_urban
        if e_combo.get() == urban_category[0]:
            l_urban = 0
        elif e_combo.get() == urban_category[1]:
            l_urban = 6.8
        elif e_combo.get() == urban_category[2]:
            l_urban = 2.3

    def calculate_path_loss():
        nonlocal l_urban, path_loss
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        f = float(f_combo.get())
        d = float(d_combo.get())
        p = int(percentage_combo.get())
        sigma = 7
        w = 20
        l_los_median = 32.45 + 20 * math.log(f, 10) + 20 * math.log(d / 1000, 10)
        los_location_percentage = 1.5624 * sigma * (math.sqrt((-2) * math.log((1 - (p / 100)), 10)) - 1.1774)
        loss_los = l_los_median + los_location_percentage
        l_nlos_median = 9.5 + 45 * math.log(f, 10) + 40 * math.log(d / 1000, 10) + l_urban
        nlos_location_percentage = sigma * (NormalDist().inv_cdf(p / 100))
        loss_nlos = l_nlos_median + nlos_location_percentage
        if p < 45:
            d_los = 212 * (math.pow(math.log(p / 100, 10), 2)) - 64 * math.log(p / 100, 10)
        else:
            d_los = 79.2 - 70 * (p / 100)
        if d < d_los:
            path_loss = loss_los
        elif d > d_los + w:
            path_loss = loss_nlos
        else:
            path_loss = loss_los + (loss_nlos - loss_los) * (d - d_los) / w
        calculatePathLossAndCoefficients(path_loss, "site_general_below_rooftop_to_street_level", path_loss_root)

    d_label = ctk.CTkLabel(root, text="Please select the distance between terminals in meters:", text_font=("Roboto", 11))
    d_label.pack()
    d_combo = ttk.Combobox(root, values=list(range(1, 3001)))
    d_combo.current(0)
    d_combo['state'] = 'readonly'
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in MHz:", text_font=("Roboto", 11))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=list(range(300, 3001)))
    f_combo.current(0)
    f_combo['state'] = 'readonly'
    f_combo.pack()

    percentage_label = ctk.CTkLabel(root, text="Please select the required location percentage (%):", text_font=("Roboto", 11))
    percentage_label.pack()
    percentage_combo = ttk.Combobox(root, values=list(range(1, 100)))
    percentage_combo.current(0)
    percentage_combo['state'] = 'readonly'
    percentage_combo.pack()

    e_label = ctk.CTkLabel(root, text="Please select urban category:", text_font=("Roboto", 11))
    e_label.pack()
    e_combo = ttk.Combobox(root, values=urban_category)
    e_combo['state'] = 'readonly'
    e_combo.current(0)
    e_combo.bind("<<ComboboxSelected>>", e_click)
    e_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
