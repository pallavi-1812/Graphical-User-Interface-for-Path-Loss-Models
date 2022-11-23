from tkinter import ttk
import customtkinter as ctk
import math
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_specific_below_rooftop_to_street_1_turn_NLoS():
    root = ctk.CTk()
    root.geometry("500x320")
    root.config(bg="#FFF8EA")
    root.title("Site Specific below rooftop to street NLoS 1 turn")

    environment_options = [
        "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS"
    ]

    alpha = 2.12
    beta = 29.2
    gamma = 2.11
    standard_deviation = 5.06

    path_loss = 0

    def e_click(event):
        # x1+x2 should be in given range
        nonlocal alpha, beta, gamma, standard_deviation
        if e_combo.get() == "Urban high-rise/LoS" or e_combo.get() == "Urban low-rise/LoS":
            x_1_combo.config(values=list(range(55, 1201)))
            x_1_combo.current(0)
            x_2_combo.config(values=list(range(55, 1201)))
            x_2_combo.current(0)
        elif e_combo.get() == "Urban high-rise/NLoS":
            alpha = 4.00
            beta = 10.2
            gamma = 2.36
            standard_deviation = 7.60
            x_1_combo.config(values=list(range(260, 1201)))
            x_1_combo.current(0)
            x_2_combo.config(values=list(range(260, 1201)))
            x_2_combo.current(0)
        f_combo.config(values=[905, 1834, 2400, 3705, 4860])
        f_combo.current(0)

    def find_l_los(d, f):
        # subtracting 10 for considering directivity of the tx antenna
        return 10 * alpha * math.log(d, 10) + beta + 10 * gamma * math.log(f, 10) + standard_deviation - 10

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("400x400")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        nonlocal path_loss
        f = float(f_combo.get())
        x1 = float(x_1_combo.get())
        x2 = float(x_2_combo.get())
        l_los = find_l_los(x1 + x2, f)
        diff_parameter = 3.45 * math.pow(10, 4) * math.pow(f * math.pow(10, 6), -0.46)
        s_2 = math.pow(diff_parameter, 2)
        d_corner = 30
        if x2 > max(s_2, d_corner):
            path_loss = l_los + 10 * math.log((x1 * x2) / (x1 + x2), 10) - 20 * math.log(diff_parameter, 10)
        else:
            l_los_0 = find_l_los(x1, f)
            l_los_max = find_l_los(x1 + max(s_2, d_corner), f)
            path_loss = l_los_0 + (l_los_max - l_los_0) * x1 / max(s_2, d_corner)
        calculatePathLossAndCoefficients(path_loss, "site_specific_below_rooftop_to_street_NLoS_1_turn", path_loss_root)

    e_label = ctk.CTkLabel(root, text="Please select environment type:", text_font=("Helvetica", 12))
    e_label.pack(pady=2)
    e_combo = ttk.Combobox(root, values=environment_options, font=("Helvetica", 10))
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")
    e_combo.bind("<<ComboboxSelected>>", e_click)
    e_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in MHz:", text_font=("Helvetica", 12))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=[905, 1834, 2400, 3705, 4860], font=("Helvetica", 10))
    f_combo.current(0)
    f_combo['state'] = 'readonly'
    f_combo.pack()

    x_1_label = ctk.CTkLabel(root, text="Please select the distance between corner and Station 1 in meters:",
                             text_font=("Helvetica", 12))
    x_1_label.pack()
    x_1_combo = ttk.Combobox(root, values=list(range(1, 101)), font=("Helvetica", 10))
    x_1_combo.current(0)
    x_1_combo['state'] = 'readonly'
    x_1_combo.pack()

    x_2_label = ctk.CTkLabel(root, text="Please select the distance between corner and Station 2 in meters:",
                             text_font=("Helvetica", 12))
    x_2_label.pack()
    x_2_combo = ttk.Combobox(root, values=list(range(1, 101)), font=("Helvetica", 10))
    x_2_combo.current(0)
    x_2_combo['state'] = 'readonly'
    x_2_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", fg_color="#7F669D", text_color="#EFF5F5",
                                     hover_color="#8F779D", height=30, command=calculate_path_loss,
                                     text_font=("Ariel", 12))
    path_loss_button.pack(pady=20)

    root.mainloop()
