from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import math
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_specific_above_rooftop_urban():
    root = ctk.CTk()
    root.geometry("700x700")
    root.title("Site Specific above Rooftop for Urban scenario")

    environment_options = [
        "medium sized city and suburban centers with medium tree density",
        "metropolitan centers"
    ]
    path_loss = 0
    street_orientation_factor = 0

    def avg_height_click(event):
        h1 = float(height_1.get())
        hr = float(avg_height_combo.get())
        w2 = float(sidewalk.get())
        if h1 < hr and w2 < 10:
            f_combo.config(values=list(range(2000, 16001)))
        else:
            f_combo.config(values=list(range(800, 5001)))
        f_combo.current(0)

    def settled_field_distance(d, wl, hr, h1):
        return wl * d * d / math.pow((h1 - hr), 2)

    def l1_msd(f, d, h1, hr, b):
        ka = 0
        kf = 0
        del_h1 = h1 - hr
        if h1 > hr:
            l_bsh = -18 * math.log(1 + del_h1, 10)
        else:
            l_bsh = 0
        if h1 > hr and f > 2:
            ka = 71.4
        elif h1 <= hr and f > 2 and d >= 500:
            ka = 73 - 0.8 * del_h1
        elif h1 <= hr and f > 2 and d < 500:
            ka = 73 - 1.6 * del_h1 * d / 1000
        elif h1 > hr and f <= 2:
            ka = 54
        elif h1 <= hr and f <= 2 and d >= 500:
            ka = 54 - 0.8 * del_h1
        elif h1 <= hr and f <= 2 and d < 500:
            ka = 54 - 1.6 * h1 * d / 1000
        if h1 > hr:
            kd = 18
        else:
            kd = 18 - 15 * del_h1 / hr
        if f > 2:
            kf = -8
        elif e_combo.get() == environment_options[0] and f <= 2:
            kf = -4 + 0.7 * (f / 925 - 1)
        elif e_combo.get() == environment_options[1] and f <= 2:
            kf = -4 + 1.5 * (f / 925 - 1)
        return l_bsh + ka + kd * math.log(d / 1000, 10) + kf * math.log(f, 10) - 9 * math.log(b, 10)

    def l2_msd(f, d, h1, hr, b, wl):
        del_h1 = h1 - hr
        ro = math.sqrt(math.pow(del_h1, 2) + math.pow(b, 2))
        del_hu = math.pow(10, -math.log(math.sqrt(b / wl), 10) - math.log(d, 10) / 9 + 10 * math.log(b / 2.35, 10) / 9)
        del_hl = (((0.00023 * b * b) - (0.1827 * b) - 9.4978) / (
            math.pow(math.log(f, 10), 2.938))) + 0.000718 * b + 0.06923
        theta = math.atan(del_h1 / b)
        qm = -1
        if h1 > hr + del_hu:
            qm = 2.35 * math.pow((del_h1 / d) * math.sqrt(b / wl), 0.9)
        elif hr + del_hu >= h1 >= hr + del_hl:
            qm = b / d
        elif h1 < hr + del_hl:
            qm = (b / (2 * math.pi * d)) * math.sqrt(wl / ro) * (1 / theta - 1 / (2 * math.pi + theta))
        return -10 * math.log(math.pow(qm, 2), 10)

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
        nonlocal path_loss, street_orientation_factor
        f = float(f_combo.get())
        d = float(d_combo.get())
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        w1 = float(street_width.get())
        hr = float(avg_height_combo.get())
        wl = float(wavelength.get())
        ds = settled_field_distance(d, wl, hr, h1)
        l = float(length.get())
        b = float(avg_b.get())
        phi = float(angle_combo.get())
        if 0 <= phi < 35:
            street_orientation_factor = -10 + 0.354 * phi
        elif 35 <= phi < 55:
            street_orientation_factor = 2.5 + 0.075 * (phi - 35)
        else:
            street_orientation_factor = 4.0 - 0.114 * (phi - 55)
        bf_loss = 32.4 + 20 * math.log(d / 1000, 10) + 20 * math.log(f, 10)
        rts_loss = -8.2 - (10 * math.log(w1, 10)) + (10 * math.log(f, 10)) + (
                20 * math.log((hr - h2), 10)) + street_orientation_factor
        msd_loss = 0
        d_bp = abs(hr - h1) * math.sqrt(1 / wl)
        l_upp = l1_msd(f, d_bp, h1, hr, b)
        l_low = l2_msd(f, d_bp, h1, hr, b, wl)
        l_mid = (l_low + l_upp) / 2
        v = 0.0417
        x = 0.1
        eta = (l_upp - l_low) * v
        d_h_bp = l_upp - l_low
        if l > ds and d_h_bp > 0:
            msd_loss = -math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / x) * (
                    l1_msd(f, d, h1, hr, b) - l_mid) + l_mid
        elif l <= ds and d_h_bp > 0:
            msd_loss = math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / x) * (
                    l2_msd(f, d, h1, hr, b, wl) - l_mid) + l_mid
        elif d_h_bp == 0:
            msd_loss = l2_msd(f, d, h1, hr, b, wl)
        elif l > ds and d_h_bp < 0:
            msd_loss = l1_msd(f, d, h1, hr, b) - math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / eta) * (
                    l_upp - l_mid) - l_upp + l_mid
        elif l <= ds and d_h_bp < 0:
            msd_loss = l2_msd(f, d, h1, hr, b, wl) - math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / eta) * (
                    l_mid - l_low) - l_low + l_mid
        if rts_loss + msd_loss > 0:
            path_loss = bf_loss + rts_loss + msd_loss
        else:
            path_loss = bf_loss
        calculatePathLossAndCoefficients(path_loss, "site_specific_above_rooftop_urban", path_loss_root)

    height_label_1 = ctk.CTkLabel(root, text="Enter height of Station 1 in meters: ", text_font=("Roboto", 11))
    height_label_1.pack()
    height_1 = ttk.Combobox(root, values=list(range(4, 51)))
    height_1.current(0)
    height_1['state'] = 'readonly'
    height_1.set("Select station 1 height")
    height_1.pack()

    height_label_2 = ctk.CTkLabel(root,
                                  text="Enter height of Station 2 in meters (should be less than average height of "
                                       "buildings): ", text_font=("Roboto", 11))
    height_label_2.pack()
    height_2 = ttk.Combobox(root, values=list(range(1, 4)))
    height_2.current(0)
    height_2['state'] = 'readonly'
    height_2.set("Select station 2 height")
    height_2.pack()

    e_label = ctk.CTkLabel(root, text="Please select environment type:", text_font=("Roboto", 11))
    e_label.pack()
    e_combo = ttk.Combobox(root, values=environment_options, width=60)
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")
    e_combo.pack()

    sidewalk_label = ctk.CTkLabel(root, text="Enter width of the sidewalk in meters: ", text_font=("Roboto", 11))
    sidewalk_label.pack()
    sidewalk = ttk.Entry(root, textvariable=DoubleVar)
    sidewalk.pack()

    street_width_label = ctk.CTkLabel(root, text="Enter width of the street in meters: ", text_font=("Roboto", 11))
    street_width_label.pack()
    street_width = ttk.Entry(root, textvariable=DoubleVar)
    street_width.pack()

    angle_label = ctk.CTkLabel(root, text="Please select angle of orientation of the street in degrees:", text_font=("Roboto", 11))
    angle_label.pack()
    angle_combo = ttk.Combobox(root, values=list(range(0, 91)))
    angle_combo.current(0)
    angle_combo['state'] = 'readonly'
    angle_combo.set("Select angle")
    angle_combo.pack()

    wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Roboto", 11))
    wavelength_label.pack()
    wavelength = ttk.Entry(root, textvariable=DoubleVar)
    wavelength.pack()

    length_label = ctk.CTkLabel(root, text="Enter length of the path covered by buildings in meters: ", text_font=("Roboto", 11))
    length_label.pack()
    length = ttk.Entry(root, textvariable=DoubleVar)
    length.pack()

    avg_b_label = ctk.CTkLabel(root, text="Enter average separation of buildings in meters: ", text_font=("Roboto", 11))
    avg_b_label.pack()
    avg_b = ttk.Entry(root, textvariable=DoubleVar)
    avg_b.pack()

    avg_height_label = ctk.CTkLabel(root, text="Please select average height of buildings in meters:", text_font=("Roboto", 11))
    avg_height_label.pack()
    avg_height_combo = ttk.Combobox(root, values=list(range(1, 6)))
    avg_height_combo['state'] = 'readonly'
    avg_height_combo.set("Select average height of buildings")
    avg_height_combo.bind("<<ComboboxSelected>>", avg_height_click)
    avg_height_combo.pack()

    d_label = ctk.CTkLabel(root, text="Please select path length in meters:", text_font=("Roboto", 11))
    d_label.pack()
    d_combo = ttk.Combobox(root, values=list(range(20, 1001)))
    d_combo.current(0)
    d_combo['state'] = 'readonly'
    d_combo.set("Select distance")
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in MHz:", text_font=("Roboto", 11))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=[])
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
