from tkinter import ttk
import customtkinter as ctk
import math
import numpy as np
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_general_below_rooftop():
    root = ctk.CTk()
    root.geometry("600x250")
    root.title("Site General Path Loss Model for below Rooftop")

    environment_options = [
        "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS", "Urban low-rise/NLoS"
    ]

    alpha = 2.12
    beta = 29.2
    gamma = 2.11
    standard_deviation = 5.06

    path_loss = 0

    def e_click(event):
        nonlocal alpha, beta, gamma, standard_deviation
        if e_combo.get() == "Urban high-rise/LoS" or e_combo.get() == "Urban low-rise/LoS":
            alpha = 2.12
            beta = 29.2
            gamma = 2.11
            standard_deviation = 5.06
            d_combo.config(values=list(range(5, 661)))
            d_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(0.8, 73.1, 0.1), 1)))
            f_combo.current(0)
        elif e_combo.get() == "Urban high-rise/NLoS":
            alpha = 4.00
            beta = 10.2
            gamma = 2.36
            standard_deviation = 7.60
            d_combo.config(values=list(range(30, 716)))
            d_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(0.8, 38.1, 0.1), 1)))
            f_combo.current(0)
        elif e_combo.get() == "Urban low-rise/NLoS":
            alpha = 5.06
            beta = -4.68
            gamma = 2.02
            standard_deviation = 9.33
            d_combo.config(values=list(range(30, 251)))
            d_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(10, 73.1, 0.1), 1)))
            f_combo.current(0)

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
        nonlocal path_loss
        path_loss = 10 * alpha * math.log(float(d_combo.get()), 10) + beta + 10 * gamma * math.log(float(f_combo.get()),
                                                                                                   10) + standard_deviation - 10
        calculatePathLossAndCoefficients(path_loss, "site_general_below_rooftop", path_loss_root)

    e_label = ctk.CTkLabel(root, text="Please select environment type:", text_font=("Roboto", 11))
    e_label.pack(pady=2)
    e_combo = ttk.Combobox(root, values=environment_options)
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")
    e_combo.bind("<<ComboboxSelected>>", e_click)
    e_combo.pack()

    d_label = ctk.CTkLabel(root, text="Please select 3-D distance between the transmitting and receiving stations in "
                                      "meters:", text_font=("Roboto", 11))
    d_label.pack(pady=2)
    d_combo = ttk.Combobox(root, values=[""])
    d_combo['state'] = 'readonly'
    d_combo.set("Select distance")
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in GHz:", text_font=("Roboto", 11))
    f_label.pack(pady=2)
    f_combo = ttk.Combobox(root, values=[""])
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
