from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import math
import numpy as np
from GUIs.ModelFunctions.Functions.oxygenAndWaterAttenuation import find_oxygen_attenuation
from GUIs.ModelFunctions.Functions.oxygenAndWaterAttenuation import find_water_attenuation
from GUIs.ModelFunctions.Functions.findCoefficients import calculatePathLossAndCoefficients


def site_specific_below_rooftop_NLoS():
    root = ctk.CTk()
    root.geometry("550x500")
    root.title("Site Specific Modal within street canyons for NLoS")
    root.config(bg="#FFF8EA")

    environment_options = [
        "Urban environment",
        "Residential environment"
    ]
    building_shapes = [
        "wedge-shaped",
        "chamfered-shape"
    ]
    environment_options_ehf = [
        "Urban very high-rise with frequency 28 GHz",
        "Urban low-rise with frequency 28 GHz",
        "Urban low-rise with frequency 60 GHz"
    ]
    type_of_propagation = ""

    path_loss = 0
    path_loss_los = -1
    breakpoint_distance = -1
    effective_road_height = -1
    path_loss_exponent = 0
    freq = 0
    l_c = 0
    l_att = 0

    def ehf_click(event):
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

    def find_los_loss(propagation):
        nonlocal breakpoint_distance, path_loss_los
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        d = float(distance_1.get())
        wl = float(wavelength.get())
        f = 0
        if propagation != "ehf":
            f = float(f_combo.get())
        if propagation == "uhf":
            breakpoint_distance = 4 * h1 * h2 / wl
            breakpoint_loss = abs(20 * math.log((math.pow(wl, 2) / (8 * math.pi * h1 * h2)), 10))
            if d < breakpoint_distance:
                path_loss_los = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
            elif d == breakpoint_distance:
                path_loss_los = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
            else:
                path_loss_los = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
        elif propagation == "shf":
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
        else:
            ro = float(density.get())
            t = float(temp.get())
            p_tot = float(p_total.get())
            path_loss_at_reference_distance = 20 * math.log(freq * 1000, 10) - 28
            attenuation_by_gases = find_oxygen_attenuation(freq, t, p_tot)
            attenuation_by_rain = find_water_attenuation(freq, t, p_tot, ro)
            path_loss_los = path_loss_at_reference_distance + 10 * path_loss_exponent * math.log(
                d) + attenuation_by_gases + attenuation_by_rain
        return path_loss_los

    def f_click(event):
        nonlocal type_of_propagation
        f = float(f_combo.get())
        path_loss_button.pack_forget()
        if 2 < f <= 38:
            e_label.pack()
            e_combo.pack()
            b_label.pack()
            b_combo.pack()
            height_label_1.pack()
            height_1.pack()
            height_label_2.pack()
            height_2.pack()
            if 2.1 <= f <= 3:
                temp_label.pack_forget()
                temp.pack_forget()
                density_label.pack_forget()
                density.pack_forget()
                p_total_label.pack_forget()
                p_total.pack_forget()
                traffic_label.pack_forget()
                traffic_combo.pack_forget()
                e_ehf_label.pack_forget()
                e_ehf_combo.pack_forget()
                type_of_propagation = "uhf"
            elif 3 < f <= 30:
                temp_label.pack_forget()
                temp.pack_forget()
                density_label.pack_forget()
                density.pack_forget()
                p_total_label.pack_forget()
                p_total.pack_forget()
                type_of_propagation = "shf"
                traffic_label.pack()
                traffic_combo.pack()
                e_ehf_label.pack_forget()
                e_ehf_combo.pack_forget()
                height_1.config(values=[4, 8])
                height_1.current(0)
                height_2.config(values=[2.7, 1.6])
                height_2.current(0)
            else:
                type_of_propagation = "ehf"
                traffic_label.pack_forget()
                traffic_combo.pack_forget()
                e_ehf_label.pack()
                e_ehf_combo.pack()
                height_1.config(values=list(range(1, 400)))
                height_1.current(0)
                height_2.config(values=list(range(1, 400)))
                height_2.current(0)
                temp_label.pack()
                temp.pack()
                density_label.pack()
                density.pack()
                p_total_label.pack()
                p_total.pack()
        else:
            e_label.pack_forget()
            e_combo.pack_forget()
            b_label.pack_forget()
            b_combo.pack_forget()
            height_label_1.pack_forget()
            height_1.pack_forget()
            height_label_2.pack_forget()
            height_2.pack_forget()
            traffic_label.pack_forget()
            traffic_combo.pack_forget()
            e_ehf_label.pack_forget()
            e_ehf_combo.pack_forget()
            temp_label.pack_forget()
            temp.pack_forget()
            density_label.pack_forget()
            density.pack_forget()
            p_total_label.pack_forget()
            p_total.pack_forget()
        path_loss_button.pack(pady=20)

    def calculate_path_loss():
        w1 = float(street_width_1.get())
        w2 = float(street_width_2.get())
        x1 = float(distance_1.get())
        x2 = float(distance_2.get())
        angle = float(corner_angle.get())
        wl = float(wavelength.get())
        f = float(f_combo.get())
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("400x400")
        path_loss_root.config(bg="#FFECEF")
        path_loss_root.title("Path Loss")
        nonlocal path_loss, l_c, l_att
        path_loss = -1
        if 0.8 <= f <= 2:
            reflection_path_loss = 20 * math.log(x1 + x2, 10) + x1 * x2 * (
                    3.86 / (math.pow(angle, 3.5) * (w1 * w2))) + 20 * math.log(4 * math.pi / wl, 10)
            diffraction_path_loss = 10 * math.log(x1 * x2 * (x1 + x2), 10) + 2 * 40 * (
                    math.atan(x2 / w2) + math.atan(x1 / w1) - math.pi / 2) / (2 * math.pi) - 0.1 * (
                                            90 - angle * (180 / math.pi)) + 20 * math.log(4 * math.pi / wl,
                                                                                          10)

            path_loss = -10 * math.log(
                (math.pow(10, -1 * reflection_path_loss / 10) + math.pow(10, -1 * diffraction_path_loss / 10)), 10)
        else:
            d_corner = 30
            l_corner = 20 if e_combo.get() == environment_options[0] else 30
            beta = 6 if b_combo.get() == building_shapes[0] else 4.2 + (1.4 * math.log(f * 1000, 10) - 7.8) * (
                    0.8 * math.log(x1, 10) - 1.0)
            if w1 / 2 + 1 < x2 <= w1 / 2 + 1 + d_corner:
                l_c = l_corner * math.log((x2 - w1 / 2), 10) / math.log(1 + d_corner, 10)
            elif x2 > w1 / 2 + 1 + d_corner:
                l_c = l_corner
            if x2 > w1 / 2 + 1 + d_corner:
                l_att = 10 * beta * math.log(((x1 + x2) / (x1 + w1 / 2 + d_corner)), 10)
            else:
                l_att = 0
            los_loss = find_los_loss(type_of_propagation)
            if los_loss == -1:
                path_loss_root.geometry("150x50")
                note_label_3 = ctk.CTkLabel(path_loss_root, text="Invalid parameters", text_font=("Helvetica", 12))
                note_label_3.pack()
                return
            path_loss = los_loss + l_c + l_att
        calculatePathLossAndCoefficients(path_loss, "site_specific_below_rooftop_NLoS", path_loss_root)

    e_label = ctk.CTkLabel(root, text="Please select environment type:", text_font=("Helvetica", 12))
    e_combo = ttk.Combobox(root, values=environment_options, font=("Helvetica", 10))
    e_combo['state'] = 'readonly'
    e_combo.set("Select environment")

    b_label = ctk.CTkLabel(root, text="Please select shape of building:", text_font=("Helvetica", 12))
    b_combo = ttk.Combobox(root, values=building_shapes, font=("Helvetica", 10))
    b_combo['state'] = 'readonly'
    b_combo.set("Select building shape")

    e_ehf_label = ctk.CTkLabel(root, text="Please select environment type with frequency:", text_font=("Helvetica", 12))
    e_ehf_combo = ttk.Combobox(root, values=environment_options_ehf, width=40, font=("Helvetica", 10))
    e_ehf_combo['state'] = 'readonly'
    e_ehf_combo.set("Select environment")
    e_ehf_combo.bind("<<ComboboxSelected>>", ehf_click)

    height_label_1 = ctk.CTkLabel(root, text="Enter height of Station 1 in meters: ", text_font=("Helvetica", 12))
    height_1 = ttk.Combobox(root, values=list(range(1, 400)), font=("Helvetica", 10))
    height_1['state'] = 'readonly'
    height_1.set("Select station 1 height")

    height_label_2 = ctk.CTkLabel(root, text="Enter height of Station 2 in meters: ", text_font=("Helvetica", 12))
    height_2 = ttk.Combobox(root, values=list(range(1, 400)), font=("Helvetica", 10))
    height_2['state'] = 'readonly'
    height_2.set("Select station 2 height")

    traffic_label = ctk.CTkLabel(root, text="Please select traffic conditions:", text_font=("Helvetica", 12))
    traffic_combo = ttk.Combobox(root, values=["Heavy Traffic", "Light Traffic"], font=("Helvetica", 10))
    traffic_combo['state'] = 'readonly'
    traffic_combo.current(0)

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in GHz:", text_font=("Helvetica", 12))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=list(np.round(np.arange(0.8, 38.1, 0.1), 1)), font=("Helvetica", 10))
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.bind("<<ComboboxSelected>>", f_click)
    f_combo.pack()

    street_width_label_1 = ctk.CTkLabel(root, text="Enter street width at position of Station 1 in meters: ",
                                        text_font=("Helvetica", 12))
    street_width_label_1.pack()
    street_width_1 = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    street_width_1.pack()

    street_width_label_2 = ctk.CTkLabel(root, text="Enter street width at position of Station 2 in meters: ",
                                        text_font=("Helvetica", 12))
    street_width_label_2.pack()
    street_width_2 = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    street_width_2.pack()

    distance_label_1 = ctk.CTkLabel(root, text="Enter distance from Station 1 to street crossing in meters: ",
                                    text_font=("Helvetica", 12))
    distance_label_1.pack()
    distance_1 = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    distance_1.pack()

    distance_label_2 = ctk.CTkLabel(root, text="Enter distance from Station 2 to street crossing in meters: ",
                                    text_font=("Helvetica", 12))
    distance_label_2.pack()
    distance_2 = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    distance_2.pack()

    corner_angle_label = ctk.CTkLabel(root, text="Enter corner angle in radians: ", text_font=("Helvetica", 12))
    corner_angle_label.pack()
    corner_angle = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    corner_angle.pack()

    wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Helvetica", 12))
    wavelength_label.pack()
    wavelength = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))
    wavelength.pack()

    temp_label = ctk.CTkLabel(root, text="Enter mean temperature in celsius: ", text_font=("Helvetica", 12))
    temp = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))

    density_label = ctk.CTkLabel(root, text="Enter water vapour density in g/m3: ", text_font=("Helvetica", 12))
    density = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))

    p_total_label = ctk.CTkLabel(root, text="Enter total air pressure in hPa: ", text_font=("Helvetica", 12))
    p_total = ttk.Entry(root, textvariable=DoubleVar, font=("Helvetica", 10))

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", fg_color="#7F669D", text_color="#EFF5F5",
                                     hover_color="#8F779D", height=30, command=calculate_path_loss,
                                     text_font=("Ariel", 12))
    path_loss_button.pack(pady=20)

    root.mainloop()
