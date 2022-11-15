from tkinter import ttk
import customtkinter as ctk
from scipy import io
import math
import numpy as np


def indoor_transmission():
    root = ctk.CTk()
    root.geometry("600x300")
    root.title("Indoor Transmission Loss Model")

    area_options = [
        "Residential",
        "Office",
        "Commercial"
    ]

    power_loss_coefficient = 0
    floor_penetration_loss_factor = 0
    path_loss = 0
    variance = 0

    def area_click(event):
        d_combo.current(0)
        if area_combo.get() == "Residential":
            num_combo.config(values=list(range(1, 10)))
            num_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(1.8, 2.1, 0.1), 1)))
            f_combo.current(0)
        elif area_combo.get() == "Office":
            num_combo.config(values=list(range(1, 4)))
            num_combo.current(0)
            f_options = list(np.round(np.arange(1.8, 2.1, 0.1), 1))
            f_options.insert(0, 0.9)
            f_combo.config(values=f_options)
            f_combo.current(0)
        elif area_combo.get() == "Commercial":
            num_combo.config(values=list(range(1, 10)))
            num_combo.current(0)
            f_combo.config(values=list(np.round(np.arange(1.8, 2.1, 0.1), 1)))
            f_combo.current(0)

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("350x300")
        path_loss_root.title("Path Loss")
        nonlocal path_loss, variance, power_loss_coefficient, floor_penetration_loss_factor
        if area_combo.get() == "Residential":
            power_loss_coefficient = 28
            floor_penetration_loss_factor = 4 * int(num_combo.get())
        elif area_combo.get() == "Office":
            if f_combo.get() == 0.9:
                power_loss_coefficient = 33
                if num_combo.get() == 1:
                    floor_penetration_loss_factor = 9
                elif num_combo.get() == 2:
                    floor_penetration_loss_factor = 19
                elif num_combo.get() == 3:
                    floor_penetration_loss_factor = 24
            else:
                power_loss_coefficient = 30
                floor_penetration_loss_factor = 15 + 4 * (int(num_combo.get()) - 1)
        elif area_combo.get() == "Commercial":
            power_loss_coefficient = 22
            floor_penetration_loss_factor = 6 + 3 * (int(num_combo.get()) - 1)
        if float(d_combo.get()) >= 5:
            path_loss = 20 * math.log(float(f_combo.get()), 10) + power_loss_coefficient * math.log(
                float(d_combo.get()),
                10) + floor_penetration_loss_factor - 28
        else:
            path_loss = 20 * math.log(float(f_combo.get()), 10) + power_loss_coefficient * math.log(
                float(d_combo.get()),
                10) + floor_penetration_loss_factor
        variance = math.pow(10, -1 * (path_loss / 10))
        path_loss_text = "Path Loss: " + str(path_loss) + " dB"
        path_loss_label = ctk.CTkLabel(path_loss_root, text=path_loss_text)
        path_loss_label.pack()
        run_label = ctk.CTkLabel(path_loss_root, text="Please select number of monte-carlo runs:")
        run_combo = ttk.Combobox(path_loss_root, values=list(range(1, 10)))
        run_combo['state'] = 'readonly'
        run_combo.current(0)
        run_combo.bind("<<ComboboxSelected>>",
                       lambda event: run_click(event, current_root=path_loss_root, num=run_combo.get()))
        run_label.pack()
        run_combo.pack()

    def run_click(event, current_root, num):
        runs = int(num)
        coefficients_label = ctk.CTkLabel(current_root, text="Channel Coefficients are: ")
        coefficients_label.pack()
        np.random.seed(0)
        channel_coefficients = []
        for i in range(1, runs + 1):
            h = math.sqrt(variance) * complex(np.random.randn(1, 1), np.conj(np.random.randn(1, 1)))
            channel_coefficients.append(h)
            h_label = ctk.CTkLabel(current_root, text="h(" + str(i) + "): " + str(h))
            h_label.pack()
        io.savemat('channel_coefficients_indoor_transmission_loss.mat', {"channel_coefficients": channel_coefficients})

    area_label = ctk.CTkLabel(root, text="Please select area:", text_font=("Roboto", 11))
    area_label.pack(pady=2)
    area_combo = ttk.Combobox(root, values=area_options)
    area_combo['state'] = 'readonly'
    area_combo.set("Select area")
    area_combo.bind("<<ComboboxSelected>>", area_click)
    area_combo.pack()

    num_label = ctk.CTkLabel(root, text="Please select number of floors:", text_font=("Roboto", 11))
    num_label.pack(pady=2)
    num_combo = ttk.Combobox(root, values=[""])
    num_combo['state'] = 'readonly'
    num_combo.set("Select number of floors")
    num_combo.pack()

    d_label = ctk.CTkLabel(root, text="Please select separation distance between the BS-UE in meters:",
                           text_font=("Roboto", 11))
    d_label.pack(pady=2)
    d_combo = ttk.Combobox(root, values=list(range(1, 101)))
    d_combo['state'] = 'readonly'
    d_combo.set("Select distance")
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select frequency in GHz:", text_font=("Roboto", 11))
    f_label.pack(pady=2)
    f_combo = ttk.Combobox(root, values=[""])
    f_combo['state'] = 'readonly'
    f_combo.set("Select frequency")
    f_combo.pack()

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
