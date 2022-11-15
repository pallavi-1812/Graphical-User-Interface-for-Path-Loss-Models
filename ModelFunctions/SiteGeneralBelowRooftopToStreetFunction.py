# The model is valid for frequencies in the 300-3 000 MHz range. The model is based on measurements
# made with antenna heights between 1.9 and 3.0 m above ground, and transmitter-receiver distances
# up to 3 000 m
from tkinter import ttk
import customtkinter as ctk
from statistics import NormalDist
import math
import numpy as np
from scipy import io
from GUIs.ModelFunctions.Functions.rateLevel import rate_computation


def site_general_below_rooftop_to_street():
    root = ctk.CTk()
    root.geometry("600x350")
    root.title("Site General for below rooftop to street level")

    path_loss = 0
    variance = 0
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
        nonlocal l_urban, path_loss, variance
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
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
        variance = math.pow(10, -1 * (path_loss / 10))
        path_loss_text = "Path Loss: " + str(path_loss) + " dB"
        path_loss_label = ctk.CTkLabel(path_loss_root, text=path_loss_text)
        path_loss_label.pack()
        run_label = ctk.CTkLabel(path_loss_root, text="Please select number of monte-carlo runs:")
        run_combo = ttk.Combobox(path_loss_root, values=list(range(1, 10)))
        run_combo['state'] = 'readonly'
        run_combo.current(0)
        run_combo.bind("<<ComboboxSelected>>",
                       lambda event: run_click(event, current_root=path_loss_root, num=run_combo.get()))
        run_label.pack()
        run_combo.pack()

    def run_click(event, current_root, num):
        runs = int(num)
        coefficients_label = ctk.CTkLabel(current_root, text="Channel Coefficients are: ")
        coefficients_label.pack()
        np.random.seed(0)
        channel_coefficients = []
        for i in range(1, runs + 1):
            h = math.sqrt(variance) * complex(np.random.randn(1, 1), np.conj(np.random.randn(1, 1)))
            channel_coefficients.append(h)
            h_label = ctk.CTkLabel(current_root, text="h(" + str(i) + "): " + str(h))
            h_label.pack()
        io.savemat('channel_coefficients_site_general_below_rooftop_to_street_loss.mat',
                   {"channel_coefficients": channel_coefficients})
        rate_computation(channel_coefficients, runs, current_root)

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
