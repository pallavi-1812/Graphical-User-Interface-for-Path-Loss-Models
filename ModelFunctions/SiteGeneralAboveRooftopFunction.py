from tkinter import ttk
import customtkinter as ctk
from scipy import io
import math
import numpy as np
from GUIs.ModelFunctions.Functions.rateLevel import rate_computation


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
    variance = 0

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
        nonlocal path_loss, variance
        path_loss = 10 * alpha * math.log(float(d_combo.get()), 10) + beta + 10 * gamma * math.log(float(f_combo.get()),
                                                                                                   10) + standard_deviation - 10
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
        io.savemat('channel_coefficients_site_general_above_rooftop_loss.mat',
                   {"channel_coefficients": channel_coefficients})
        rate_computation(channel_coefficients, runs, current_root)

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
