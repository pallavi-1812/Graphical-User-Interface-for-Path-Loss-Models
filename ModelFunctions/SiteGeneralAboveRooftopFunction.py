from tkinter import ttk
import customtkinter as ctk
import math
import numpy as np
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_general_above_rooftop():
    root = ctk.CTk()
    root.geometry("650x250")
    root.title("Site General Path Loss Model for Above Rooftop")
    root.config(bg="#FFF8EA")

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
        path_loss_root.geometry("400x400")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        nonlocal path_loss
        path_loss = 10 * alpha * math.log(float(d_combo.get()), 10) + beta + 10 * gamma * math.log(float(f_combo.get()),
                                                                                                   10) + standard_deviation - 10
        calculatePathLossAndCoefficients(path_loss, "site_general_above_rooftop", path_loss_root)

    e_label = ctk.CTkLabel(root, text="Please select environment type:", text_font=("Helvetica", 12))
    e_label.pack(pady=2)
    e_combo = ttk.Combobox(root, values=environment_options, font=("Helvetica", 10))
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")
    e_combo.bind("<<ComboboxSelected>>", e_click)
    e_combo.pack()

    d_label = ctk.CTkLabel(root, text="Please select distance between the transmitting and receiving stations in "
                                      "meters:", text_font=("Helvetica", 12))
    d_label.pack(pady=2)
    d_combo = ttk.Combobox(root, values=[""], font=("Helvetica", 10))
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
