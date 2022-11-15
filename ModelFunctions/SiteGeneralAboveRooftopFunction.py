from tkinter import ttk
import customtkinter as ctk
import math
import numpy as np
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_general_above_rooftop():
    root = ctk.CTk()
    root.geometry("430x250")
    root.title("Site General Path Loss Model for Above Rooftop")

    environment_options = [
        "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS"
    ]

    alpha = 2.29
    beta = 28.6
    gamma = 1.96
    standard_deviation = 3.48

    path_loss = 0

    def e_click(event):
        if e_combo.get() == "Urban high-rise/LoS" or e_combo.get() == "Urban low-rise/LoS":
            d_combo.config(values=list(range(55, 1201)))
            d_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(2.2, 73.1, 0.1), 1)))
            f_combo.current(0)
        elif e_combo.get() == "Urban high-rise/NLoS":
            nonlocal alpha, beta, gamma, standard_deviation
            alpha = 4.39
            beta = -6.27
            gamma = 2.30
            standard_deviation = 6.89
            d_combo.config(values=list(range(260, 1201)))
            d_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(2.2, 66.6, 0.1), 1)))
            f_combo.current(0)

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
        nonlocal path_loss
        path_loss = 10 * alpha * math.log(float(d_combo.get()), 10) + beta + 10 * gamma * math.log(float(f_combo.get()),
                                                                                                   10) + standard_deviation - 10
        calculatePathLossAndCoefficients(path_loss, "site_general_above_rooftop", path_loss_root)

    e_label = ctk.CTkLabel(root, text="Please select environment type:")
    e_label.pack(pady=2)
    e_combo = ttk.Combobox(root, values=environment_options)
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")
    e_combo.bind("<<ComboboxSelected>>", e_click)
    e_combo.pack()

    d_label = ctk.CTkLabel(root, text="Please select distance in meters:")
    d_label.pack(pady=2)
    d_combo = ttk.Combobox(root, values=[""])
    d_combo['state'] = 'readonly'
    d_combo.set("Select distance")
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select frequency in GHz:")
    f_label.pack(pady=2)
    f_combo = ttk.Combobox(root, values=[""])
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
