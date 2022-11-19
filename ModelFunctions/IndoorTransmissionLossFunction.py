from tkinter import ttk
import customtkinter as ctk
import math
import numpy as np
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def indoor_transmission():
    root = ctk.CTk()
    root.geometry("600x300")
    root.config(bg="#FFF8EA")
    root.title("Indoor Transmission Loss Model")

    area_options = [
        "Residential",
        "Office",
        "Commercial"
    ]

    path_loss = 0

    def area_click(event):
        d_combo.current(0)
        if area_combo.get() == "Residential":
            num_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(1.8, 2.1, 0.1), 1)))
            f_combo.current(0)
        elif area_combo.get() == "Office":
            num_combo.current(0)
            f_options = list(np.round(np.arange(1.8, 2.1, 0.1), 1))
            f_options.insert(0, 0.9)
            f_combo.config(values=f_options)
            f_combo.current(0)
        elif area_combo.get() == "Commercial":
            num_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(1.8, 2.1, 0.1), 1)))
            f_combo.current(0)

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("450x500")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        f = float(f_combo.get())
        d = float(d_combo.get())
        n = int(num_combo.get())
        nonlocal path_loss
        shadow_fading_constant = 0
        power_loss_coefficient = 0
        floor_penetration_loss_factor = 0
        if area_combo.get() == "Residential":
            power_loss_coefficient = 28
            floor_penetration_loss_factor = 4 * n
            if d >= 3:
                shadow_fading_constant = 8
        elif area_combo.get() == "Office":
            if f == 0.9:
                power_loss_coefficient = 33
                if num_combo.get() == 1:
                    floor_penetration_loss_factor = 9
                elif num_combo.get() == 2:
                    floor_penetration_loss_factor = 19
                elif num_combo.get() == 3:
                    floor_penetration_loss_factor = 24
            else:
                if d >= 4:
                    shadow_fading_constant = 10
                power_loss_coefficient = 30
                floor_penetration_loss_factor = 15 + 4 * (n - 1)
        elif area_combo.get() == "Commercial":
            power_loss_coefficient = 22
            floor_penetration_loss_factor = 6 + 3 * (n - 1)
            if d >= 4:
                shadow_fading_constant = 10
        if n == 0:
            floor_penetration_loss_factor = 0
        path_loss = 20 * math.log(f, 10) + power_loss_coefficient * math.log(
            d, 10) + floor_penetration_loss_factor - shadow_fading_constant
        calculatePathLossAndCoefficients(path_loss, "indoor_transmission", path_loss_root)

    area_label = ctk.CTkLabel(root, text="Please select area:", text_font=("Helvetica", 12))
    area_label.pack(pady=2)
    area_combo = ttk.Combobox(root, values=area_options, font=("Helvetica", 10))
    area_combo['state'] = 'readonly'
    area_combo.set("Select area")
    area_combo.bind("<<ComboboxSelected>>", area_click)
    area_combo.pack()

    num_label = ctk.CTkLabel(root, text="Please select number of floors:", text_font=("Helvetica", 12))
    num_label.pack(pady=2)
    num_combo = ttk.Combobox(root, values=list(range(0, 4)), font=("Helvetica", 10))
    num_combo['state'] = 'readonly'
    num_combo.set("Select number of floors")
    num_combo.pack()

    d_label = ctk.CTkLabel(root, text="Please select the distance between the transmitter and receiver in meters:",
                           text_font=("Helvetica", 12))
    d_label.pack(pady=2)
    d_combo = ttk.Combobox(root, values=list(range(2, 1001)), font=("Helvetica", 10))
    d_combo['state'] = 'readonly'
    d_combo.set("Select distance")
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select frequency in GHz:", text_font=("Helvetica", 12))
    f_label.pack(pady=2)
    f_combo = ttk.Combobox(root, values=[""], font=("Helvetica", 10))
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", fg_color="#7F669D", text_color="#EFF5F5",
                                     hover_color="#8F779D", height=30, command=calculate_path_loss,
                                     text_font=("Ariel", 12))
    path_loss_button.pack(pady=20)

    root.mainloop()
