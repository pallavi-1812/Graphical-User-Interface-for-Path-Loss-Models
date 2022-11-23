from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import math
import numpy as np
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_specific_above_rooftop_suburban():
    root = ctk.CTk()
    root.geometry("650x500")
    root.title("Site Specific above Rooftop for suburban scenario")
    root.config(bg="#FFF8EA")

    path_loss = 0

    def find_l_0_n(d, d_rd, phi, h1, h2, hr, w, wl, f):
        k = 0
        while True:
            d_k = find_d_k(k, phi, h1, h2, hr, w)
            d_k1 = find_d_k(k + 1, phi, h1, h2, hr, w)
            if d_k <= d < d_k1 < d_rd:
                l_dk = find_loss_dk(k, phi, h1, h2, hr, w, wl)
                l_dk1 = find_loss_dk(k + 1, phi, h1, h2, hr, w, wl)
                return l_dk + (l_dk1 - l_dk) * (d - d_k) / (d_k1 - d_k)
            elif d_k <= d < d_rd < d_k1:
                l_dk = find_loss_dk(k, phi, h1, h2, hr, w, wl)
                l_d_rd = find_loss_d_rd(k, f, phi, h1, h2, hr, w, wl)
                return l_dk + (l_d_rd - l_dk) * (d - d_k) / (d_rd - d_k)
            k += 1

    def find_k(f, phi, h1, h2, hr, w):
        k = 0
        d_rd = find_d_rd(f, phi, h1, h2, hr, w)
        while True:
            d_k = find_d_k(k, phi, h1, h2, hr, w)
            d_k1 = find_d_k(k + 1, phi, h1, h2, hr, w)
            if d_k <= d_rd <= d_k1:
                return k
            k += 1

    def find_loss_d_rd(k, f, phi, h1, h2, hr, w, wl):
        l_dk = find_loss_dk(k, phi, h1, h2, hr, w, wl)
        l_dk1 = find_loss_dk(k + 1, phi, h1, h2, hr, w, wl)
        dk = find_d_k(k, phi, h1, h2, hr, w)
        dk1 = find_d_k(k + 1, phi, h1, h2, hr, w)
        d_rd = find_d_rd(f, phi, h1, h2, hr, w)
        return l_dk + ((l_dk1 - l_dk) * (d_rd - dk) / (dk1 - dk))

    def find_d_rd(f, phi, h1, h2, hr, w):
        d3 = find_d_kp(3, phi, h1, h2, hr, w)
        d4 = find_d_kp(4, phi, h1, h2, hr, w)
        d1 = find_d_kp(1, phi, h1, h2, hr, w)
        d2 = find_d_kp(2, phi, h1, h2, hr, w)
        return math.log(f, 10) * (
                0.25 * d3 + 0.25 * d4 - 0.16 * d1 - 0.35 * d2) + 0.25 * d1 + 0.56 * d2 + 0.10 * d3 + 0.10 * d4

    def find_d_k(k, phi, h1, h2, hr, w):
        b_k = find_bk(k, h1, h2, hr, w)
        return math.sqrt(math.pow(b_k / math.sin(phi), 2) + math.pow((h1 - h2), 2))

    def find_loss_dk(k, phi, h1, h2, hr, w, wl):
        d_kp = find_d_kp(k, phi, h1, h2, hr, w)
        return 20 * math.log((4 * math.pi * d_kp / (math.pow(0.4, k) * wl)), 10)

    def find_d_kp(k, phi, h1, h2, hr, w):
        phi_k = find_phi_k(k, phi, h1, h2, hr, w)
        a_k = find_ak(k, h1, h2, hr, w)
        return math.sqrt(math.pow(a_k / math.sin(phi_k), 2) + math.pow((h1 - h2), 2))

    def find_ak(k, h1, h2, hr, w):
        return w * (h1 - h2) * (2 * k + 1) / (2 * (hr - h2))

    def find_bk(k, h1, h2, hr, w):
        return w * (h1 - h2) * (2 * k + 1) / (2 * (hr - h2)) - k * w

    def find_phi_k(k, phi, h1, h2, hr, w):
        a_k = find_ak(k, h1, h2, hr, w)
        b_k = find_bk(k, h1, h2, hr, w)
        return math.atan(a_k * phi / b_k)

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("400x400")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        nonlocal path_loss
        w = float(street_width.get())
        phi = float(angle_combo.get())
        wl = float(wavelength.get())
        hr = float(avg_height_combo.get())
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        d = float(d_combo.get())
        f = float(f_combo.get())
        d0 = find_d_k(0, phi, h1, h2, hr, w)
        d_rd = find_d_rd(f, phi, h1, h2, hr, w)
        l_0_n = find_l_0_n(d, d_rd, phi, h1, h2, hr, w, wl, f)
        k_l_drd = find_k(f, phi, h1, h2, hr, w)
        if d < d0:
            path_loss = 20 * math.log((4 * math.pi * d / wl), 10)
        elif d0 <= d <= d_rd:
            path_loss = l_0_n
        elif d >= d_rd:
            path_loss = 32.1 * math.log(d / d_rd, 10) + find_loss_d_rd(k_l_drd, f, phi, h1, h2, hr, w, wl)
        calculatePathLossAndCoefficients(path_loss, "site_specific_above_rooftop_suburban", path_loss_root)

    street_width_label = ctk.CTkLabel(root, text="Enter width of the street in meters: ", text_font=("Helvetica", 12))
    street_width_label.pack()
    street_width = ttk.Combobox(root, values=list(range(10, 26)), font=("Helvetica", 10))
    street_width.current(0)
    street_width['state'] = 'readonly'
    street_width.current(0)
    street_width.pack()

    angle_label = ctk.CTkLabel(root, text="Please select angle of orientation of the street in degrees:",
                               text_font=("Helvetica", 12))
    angle_label.pack()
    angle_combo = ttk.Combobox(root, values=list(range(1, 91)), font=("Helvetica", 10))
    angle_combo.current(0)
    angle_combo['state'] = 'readonly'
    angle_combo.current(0)
    angle_combo.pack()

    wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Helvetica", 12))
    wavelength_label.pack()
    wavelength = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    wavelength.pack()

    avg_height_label = ctk.CTkLabel(root, text="Please select average height of buildings in meters:",
                                    text_font=("Helvetica", 12))
    avg_height_label.pack()
    avg_height_combo = ttk.Combobox(root, values=list(range(11, 21)), font=("Helvetica", 10))
    avg_height_combo.current(0)
    avg_height_combo['state'] = 'readonly'
    avg_height_combo.current(0)
    avg_height_combo.pack()

    height_label_1 = ctk.CTkLabel(root, text="Enter height of Station 1 in meters: ", text_font=("Helvetica", 12))
    height_label_1.pack()
    height_1 = ttk.Combobox(root, values=list(range(6, 111)), font=("Helvetica", 10))
    height_1.current(0)
    height_1['state'] = 'readonly'
    height_1.pack()

    height_label_2 = ctk.CTkLabel(root,
                                  text="Enter height of Station 2 in meters (should be less than average height of "
                                       "buildings): ", text_font=("Helvetica", 12))
    height_label_2.pack()
    height_2 = ttk.Combobox(root, values=list(range(1, 17)), font=("Helvetica", 10))
    height_2.current(0)
    height_2['state'] = 'readonly'
    height_2.pack()

    d_label = ctk.CTkLabel(root, text="Please select path length in meters:", text_font=("Helvetica", 12))
    d_label.pack()
    d_combo = ttk.Combobox(root, values=list(range(10, 1001)), font=("Helvetica", 10))
    d_combo.current(0)
    d_combo['state'] = 'readonly'
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in GHz:", text_font=("Helvetica", 12))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=list(np.round(np.arange(0.8, 38.1, 0.1), 1)), font=("Helvetica", 10))
    f_combo['state'] = 'readonly'
    f_combo.current(0)
    f_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", fg_color="#7F669D", text_color="#EFF5F5",
                                     hover_color="#8F779D", height=30, command=calculate_path_loss,
                                     text_font=("Ariel", 12))
    path_loss_button.pack(pady=20)

    root.mainloop()
