from tkinter import ttk
from tkinter import *
import customtkinter as ctk
import math
from GUIs.ModelFunctions.Functions.oxygenAndWaterAttenuation import find_oxygen_attenuation
from GUIs.ModelFunctions.Functions.oxygenAndWaterAttenuation import find_water_attenuation
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients
import numpy as np


def site_specific_below_rooftop_to_street_LoS():
    root = ctk.CTk()
    root.geometry("400x500")
    root.config(bg="#FFF8EA")
    root.title("Site Specific Modal for below rooftop to street level for LoS in urban scenarios")

    frequency_ranges = [
        "UHF propagation",
        "SHF propagation",
        "EHF propagation (Millimeter Wave)"
    ]

    environment_options = [
        "Urban very high-rise with frequency 28 GHz",
        "Urban low-rise with frequency 28 GHz",
        "Urban low-rise with frequency 60 GHz"
    ]

    is_UHF_propagation = False
    is_SHF_propagation = False
    is_EHF_propagation = False

    path_loss = 0
    breakpoint_distance = -1
    effective_road_height = -1
    path_loss_exponent = 0
    freq = 0

    def e_click(event):
        nonlocal path_loss_exponent, freq
        if e_combo.get() == environment_options[0]:
            path_loss_exponent = 2.21
            freq = 28
        elif e_combo.get() == environment_options[1]:
            path_loss_exponent = 2.06
            freq = 28
        elif e_combo.get() == environment_options[2]:
            path_loss_exponent = 1.9
            freq = 60

    def range_click(event):
        nonlocal is_UHF_propagation, is_SHF_propagation, is_EHF_propagation, traffic_label, traffic_combo
        is_UHF_propagation = False
        is_SHF_propagation = False
        is_EHF_propagation = False
        path_loss_button.pack_forget()
        if range_combo.get() == "UHF propagation":
            p_total_label.pack_forget()
            p_total.pack_forget()
            density_label.pack_forget()
            density.pack_forget()
            temp_label.pack_forget()
            temp.pack_forget()
            e_label.pack_forget()
            e_combo.pack_forget()
            traffic_label.pack_forget()
            traffic_combo.pack_forget()
            is_UHF_propagation = True
            wavelength_label.pack()
            wavelength.pack()
            height_1.config(values=list(range(1, 400)))
            height_1.current(0)
            height_2.config(values=list(range(1, 400)))
            height_2.current(0)
            f_combo.config(values=list(np.round(np.arange(0.3, 3.1, 0.1), 1)))
            f_combo.current(0)
            f_label.pack()
            f_combo.pack()
        elif range_combo.get() == "SHF propagation":
            # The roadway is 27 m wide, including 6 m wide footpaths on either side
            p_total_label.pack_forget()
            p_total.pack_forget()
            density_label.pack_forget()
            density.pack_forget()
            temp_label.pack_forget()
            temp.pack_forget()
            e_label.pack_forget()
            e_combo.pack_forget()
            is_SHF_propagation = True
            f_combo.config(values=[3.35, 8.45, 15.75])
            f_combo.current(0)
            f_label.pack()
            f_combo.pack()
            traffic_label.pack()
            traffic_combo.pack()
            wavelength_label.pack()
            wavelength.pack()
            height_1.config(values=[4, 8])
            height_1.current(0)
            height_2.config(values=[2.7, 1.6])
            height_2.current(0)
        elif range_combo.get() == "EHF propagation (Millimeter Wave)":
            f_label.pack_forget()
            f_combo.pack_forget()
            traffic_label.pack_forget()
            traffic_combo.pack_forget()
            height_1.config(values=list(range(1, 400)))
            height_1.current(0)
            height_2.config(values=list(range(1, 400)))
            height_2.current(0)
            is_EHF_propagation = True
            e_label.pack()
            e_combo.pack()
            wavelength_label.pack_forget()
            wavelength.pack_forget()
            p_total_label.pack()
            p_total.pack()
            density_label.pack()
            density.pack()
            temp_label.pack()
            temp.pack()
        path_loss_button.pack(pady=10)

    def calculate_path_loss():
        d = float(distance.get())
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        f = 0
        if range_combo.get() != "EHF propagation (Millimeter Wave)":
            f = float(f_combo.get())
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
        path_loss_root.config(bg="#FFECEF")
        nonlocal path_loss, breakpoint_distance
        path_loss = -1
        if is_UHF_propagation:
            wl = float(wavelength.get())
            breakpoint_distance = 4 * h1 * h2 / wl
            breakpoint_loss = abs(20 * math.log((math.pow(wl, 2) / (8 * math.pi * h1 * h2)), 10))
            if d < breakpoint_distance:
                path_loss = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
            elif d == breakpoint_distance:
                path_loss = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
            else:
                path_loss = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
        elif is_SHF_propagation:
            nonlocal effective_road_height
            wl = float(wavelength.get())
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
                path_loss = -1
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
                        path_loss = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
                    elif d == breakpoint_distance:
                        path_loss = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
                    else:
                        path_loss = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
                else:
                    basic_propagations_loss = abs(20 * math.log(wl / 2 * math.pi * r_s, 10))
                    path_loss = basic_propagations_loss + 20 + 30 * math.log(d / r_s, 10)
        elif is_EHF_propagation:
            ro = float(density.get())
            t = float(temp.get())
            p_tot = float(p_total.get())
            path_loss_at_reference_distance = 20 * math.log(freq * 1000, 10) - 28
            attenuation_by_gases = find_oxygen_attenuation(freq, t, p_tot)
            attenuation_by_rain = find_water_attenuation(freq, t, p_tot, ro)
            path_loss = path_loss_at_reference_distance + 10 * path_loss_exponent * math.log(
                d) + attenuation_by_gases + attenuation_by_rain
        if path_loss == -1:
            path_loss_root.geometry("150x50")
            note_label_3 = ctk.CTkLabel(path_loss_root, text="Invalid parameters", text_font=("Roboto", 11))
            note_label_3.pack()
            return
        calculatePathLossAndCoefficients(path_loss, "site_specific_below_rooftop_to_street_level_LoS", path_loss_root)

    e_label = ctk.CTkLabel(root, text="Please select environment type with frequency:", text_font=("Roboto", 11))
    e_combo = ttk.Combobox(root, values=environment_options, width=40)
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")
    e_combo.bind("<<ComboboxSelected>>", e_click)

    range_label = ctk.CTkLabel(root, text="Please select frequency range:", text_font=("Roboto", 11))
    range_label.pack()
    range_combo = ttk.Combobox(root, values=frequency_ranges, width=30)
    range_combo['state'] = 'readonly'
    range_combo.set("Select frequency range")
    range_combo.bind("<<ComboboxSelected>>", range_click)
    range_combo.pack()

    # 300 MHz - 3 GHz : UHF, 3 GHz - 30 GHz : SHF (here, upto 15 GHz), 30 GHz - 300 GHz (here, 100 GHz) : EHF
    f_label = ctk.CTkLabel(root, text="Please select operating frequency in GHz:", text_font=("Roboto", 11))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=[])
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.pack()

    height_label_1 = ctk.CTkLabel(root, text="Enter height of Station 1 in meters: ", text_font=("Roboto", 11))
    height_label_1.pack()
    height_1 = ttk.Combobox(root, values=list(range(1, 400)))
    height_1['state'] = 'readonly'
    height_1.set("Select station 1 height")
    height_1.pack()

    height_label_2 = ctk.CTkLabel(root, text="Enter height of Station 2 in meters: ", text_font=("Roboto", 11))
    height_label_2.pack()
    height_2 = ttk.Combobox(root, values=list(range(1, 400)))
    height_2['state'] = 'readonly'
    height_2.set("Select station 2 height")
    height_2.pack()

    distance_label = ctk.CTkLabel(root, text="Enter distance from Station 1 to Station 2 in meters: ", text_font=("Roboto", 11))
    distance_label.pack()
    distance = ttk.Entry(root, textvariable=DoubleVar)
    distance.pack()

    traffic_label = ctk.CTkLabel(root, text="Please select traffic conditions:", text_font=("Roboto", 11))
    traffic_combo = ttk.Combobox(root, values=["Heavy Traffic", "Light Traffic"])
    traffic_combo['state'] = 'readonly'
    traffic_combo.current(0)

    wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Roboto", 11))
    wavelength = ttk.Entry(root, textvariable=DoubleVar)

    temp_label = ctk.CTkLabel(root, text="Enter mean temperature in celsius: ", text_font=("Roboto", 11))
    temp = ttk.Entry(root, textvariable=DoubleVar)

    density_label = ctk.CTkLabel(root, text="Enter water vapour density in g/m3: ", text_font=("Roboto", 11))
    density = ttk.Entry(root, textvariable=DoubleVar)

    p_total_label = ctk.CTkLabel(root, text="Enter total air pressure in hPa: ", text_font=("Roboto", 11))
    p_total = ttk.Entry(root, textvariable=DoubleVar)

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()

