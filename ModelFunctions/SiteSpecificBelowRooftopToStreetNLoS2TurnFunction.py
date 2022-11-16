import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import math
from time import sleep
import numpy as np
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_specific_below_rooftop_to_street_2_turn_NLoS():
    root = ctk.CTk()
    root.geometry("600x400")
    root.config(bg="#FFF8EA")
    root.title("Site Specific below rooftop to street level for 2 turn NLoS")

    curr = 0
    path_loss = 0
    l_los = 0
    turn_distances = []
    breakpoint_distance = -1
    effective_road_height = -1
    path_loss_los = -1

    def calculate_below_rooftop_LoS(d, f):
        nonlocal breakpoint_distance, path_loss_los
        wl = float(wavelength.get())
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        if f in [430, 750, 905, 1834, 2400]:
            breakpoint_distance = 4 * h1 * h2 / wl
            breakpoint_loss = abs(20 * math.log((math.pow(wl, 2) / (8 * math.pi * h1 * h2)), 10))
            if d < breakpoint_distance:
                path_loss_los = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
            elif d == breakpoint_distance:
                path_loss_los = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
            else:
                path_loss_los = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
        else:
            nonlocal effective_road_height
            effective_road_height = -1
            if traffic_combo.get() == "Heavy Traffic":
                if f == 3.35:
                    if h1 == 4:
                        if h2 == 2.7:
                            effective_road_height = 1.3
                    else:
                        if h2 == 2.7:
                            effective_road_height = 1.6
                elif f == 8.45:
                    if h1 == 4:
                        if h2 == 2.7:
                            effective_road_height = 1.6
                    else:
                        if h2 == 2.7:
                            effective_road_height = 1.6
                else:
                    if h1 == 4:
                        if h2 == 2.7:
                            effective_road_height = 1.4
                    else:
                        if h2 == 2.7:
                            effective_road_height = 1000
            else:
                if f == 3.35:
                    if h1 == 4:
                        if h2 == 2.7:
                            effective_road_height = 0.59
                        else:
                            effective_road_height = 0.23
                elif f == 8.45:
                    if h1 == 4:
                        if h2 == 2.7:
                            effective_road_height = 1000
                        else:
                            effective_road_height = 0.43
                    else:
                        if h2 == 2.7:
                            effective_road_height = 1000
                else:
                    if h1 == 4:
                        if h2 == 2.7:
                            effective_road_height = 1000
                        else:
                            effective_road_height = 0.74
                    else:
                        if h2 == 2.7:
                            effective_road_height = 1000
            if effective_road_height == -1:
                path_loss_los = -1
            elif effective_road_height == 1000:
                breakpoint_distance = 4 * h1 * h2 / wl
            else:
                breakpoint_distance = 4 * (h1 - effective_road_height) * (h2 - effective_road_height) / wl
            if effective_road_height != -1 and h1 > effective_road_height and h2 > effective_road_height:
                r_s = 20  # experimentally derived
                if d < r_s:
                    breakpoint_loss = abs(20 * math.log(
                        (math.pow(wl, 2) / (8 * math.pi * (h1 - effective_road_height) * (h2 - effective_road_height))),
                        10))
                    if d < breakpoint_distance:
                        path_loss_los = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
                    elif d == breakpoint_distance:
                        path_loss_los = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
                    else:
                        path_loss_los = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
                else:
                    basic_propagations_loss = abs(20 * math.log(wl / 2 * math.pi * r_s, 10))
                    path_loss_los = basic_propagations_loss + 20 + 30 * math.log(d / r_s, 10)
        return path_loss_los

    def find_l_los_1_turn(x1, x2, f):
        nonlocal l_los
        l_los = calculate_below_rooftop_LoS(x1 + x2, f)
        if l_los == -1:
            return -1
        diff_parameter = 3.45 * math.pow(10, 4) * math.pow(f * math.pow(10, 6), -0.46)
        s_2 = math.pow(diff_parameter, 2)
        d_corner = 30
        if x2 > max(s_2, d_corner):
            return l_los + 10 * math.log((x1 * x2) / (x1 + x2), 10) - 20 * math.log(diff_parameter, 10)
        else:
            l_los_0 = calculate_below_rooftop_LoS(x1, f)
            l_los_max = calculate_below_rooftop_LoS(x1 + max(s_2, d_corner), f)
            if l_los_0 == -1 or l_los_max == -1:
                return -1
            return l_los_0 + (l_los_max - l_los_0) * x1 / max(s_2, d_corner)

    def f_click(event):
        path_loss_button.pack_forget()
        note_label.pack_forget()
        f = float(f_combo.get())
        height_label_1.pack()
        height_1.pack()
        height_label_2.pack()
        height_2.pack()
        if f in [430, 750, 905, 1834, 2400]:
            traffic_label.pack_forget()
            traffic_combo.pack_forget()
        else:
            traffic_label.pack()
            traffic_combo.pack()
            height_1.config(values=[4, 8])
            height_1.current(0)
            height_2.config(values=[2.7, 1.6])
            height_2.current(0)
        note_label.pack()
        path_loss_button.pack()

    def n_th_loss_list(turn_dist):
        loss_2_turn = []
        nonlocal curr
        curr = 0
        d_corner = 30
        f = float(f_combo.get())
        s_1 = 0.54 * math.pow(f * 1000, 0.076)
        s_2 = 3.45 * math.pow(10, 4) * math.pow(f * math.pow(10, 6), -0.46)
        max_d = max(math.pow(s_2, 2), d_corner)
        for d in turn_dist:
            x1 = d[0]
            x2 = d[1]
            x3 = d[2]
            if x3 > max_d:
                los_loss = calculate_below_rooftop_LoS(x1 + x2 + x3, f)
                if los_loss == -1:
                    return -1
                curr = los_loss + 10 * math.log(x1 * x2 * x3 / (x1 + x2 + x3), 10) - 20 * math.log(
                    s_1,
                    10) - 20 * math.log(
                    s_2, 10)
            else:
                l_los_0 = find_l_los_1_turn(x1 + x2, 0, f)
                l_los_max = find_l_los_1_turn(x1 + x2, max(math.pow(s_2, 2), d_corner), f)
                if l_los_0 == -1 or l_los_max == -1:
                    return -1
                curr = l_los_0 + (l_los_max - l_los_0) * x1 / max_d
            loss_2_turn.append(curr)
        return loss_2_turn

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("400x400")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        nonlocal path_loss, turn_distances
        n = int(n_combo.get())
        sleep(2)
        for i in range(1, n + 1):
            print("for " + str(i) + " corner: ")
            x_1 = input("Please enter the distance between first corner and Station 1 in meters:")
            x_2 = input("Please enter the distance between first corner and second corner in meters:")
            x_3 = input("Please enter the distance between second corner and Station 2 in meters:")
            x_dist = [float(x_1), float(x_2), float(x_3)]
            turn_distances.append(x_dist)

        curr_loss = n_th_loss_list(turn_distances)
        if curr_loss == -1:
            path_loss_root.geometry("150x50")
            note_label_3 = ctk.CTkLabel(path_loss_root, text="Invalid parameters", text_font=("Roboto", 11))
            note_label_3.pack()
            return
        curr_sum = 0
        for val in curr_loss:
            curr_sum += math.pow(math.pow(10, val / 10), -1)
        path_loss = -10 * math.log(curr_sum, 10)
        print("Please go to GUI to check path loss and channel coefficients")
        calculatePathLossAndCoefficients(path_loss, "site_specific_below_rooftop_to_street_level_NLoS_2_turn",
                                         path_loss_root)

    wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Roboto", 11))
    wavelength_label.pack()
    wavelength = ttk.Entry(root, textvariable=DoubleVar)
    wavelength.pack()

    d_label = ctk.CTkLabel(root, text="Please select the distance between terminals in meters:", text_font=("Roboto", 11))
    d_label.pack()
    d_combo = ttk.Combobox(root, values=list(range(1, 1001)))
    d_combo.current(0)
    d_combo['state'] = 'readonly'
    d_combo.pack()

    height_label_1 = ctk.CTkLabel(root, text="Enter height of Station 1 in meters: ", text_font=("Roboto", 11))
    height_1 = ttk.Combobox(root, values=list(np.round(np.arange(1.5, 4.1, 0.1), 1)))
    height_1['state'] = 'readonly'
    height_1.current(0)

    height_label_2 = ctk.CTkLabel(root, text="Enter height of Station 2 in meters: ", text_font=("Roboto", 11))
    height_2 = ttk.Combobox(root, values=list(np.round(np.arange(1.5, 4.1, 0.1), 1)))
    height_2['state'] = 'readonly'
    height_2.current(0)

    traffic_label = ctk.CTkLabel(root, text="Please select traffic conditions:", text_font=("Roboto", 11))
    traffic_combo = ttk.Combobox(root, values=["Heavy Traffic", "Light Traffic"])
    traffic_combo['state'] = 'readonly'
    traffic_combo.current(0)

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in MHz:", text_font=("Roboto", 11))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=[430, 750, 905, 1834, 2400, 3705, 4860])
    f_combo.current(0)
    f_combo['state'] = 'readonly'
    f_combo.bind("<<ComboboxSelected>>", f_click)
    f_combo.pack()

    n_label = ctk.CTkLabel(root, text="Please select for how many 2-Turn route path, you want to calculate path loss:",
                           text_font=("Roboto", 11))
    n_label.pack()
    n_combo = ttk.Combobox(root, values=list(range(1, 5)))
    n_combo.current(0)
    n_combo['state'] = 'readonly'
    n_combo.pack()

    note_label = ctk.CTkLabel(root,
                              text="Please go to terminal for entering values of corner distances after clicking on "
                                   "path "
                                   "loss button", text_font=("Roboto", 11))

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
