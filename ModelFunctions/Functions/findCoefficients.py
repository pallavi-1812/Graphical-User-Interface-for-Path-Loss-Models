import math
import customtkinter as ctk
from tkinter import ttk
from scipy import io
import numpy as np
from GUIs.ModelFunctions.Functions.rateLevel import rate_computation


def calculatePathLossAndCoefficients(path_loss, scenario_name, path_loss_root):
    variance = math.pow(10, -1 * (path_loss / 10))
    path_loss_text = "Path Loss: " + str(path_loss) + " dB"
    path_loss_label = ctk.CTkLabel(path_loss_root, text=path_loss_text)
    path_loss_label.pack()
    run_label = ctk.CTkLabel(path_loss_root, text="Please select number of monte-carlo runs:")
    run_combo = ttk.Combobox(path_loss_root, values=list(range(1, 10)))
    run_combo['state'] = 'readonly'
    run_combo.current(0)
    run_combo.bind("<<ComboboxSelected>>",
                   lambda event: run_click(event, current_root=path_loss_root, num=run_combo.get(), variance=variance,
                                           file_name=scenario_name))
    run_label.pack()
    run_combo.pack()


def run_click(event, current_root, num, variance, file_name):
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
    filename = "channel_coefficients_"+file_name+"_loss.mat"
    io.savemat(filename, {"channel_coefficients": channel_coefficients})
    rate_computation(channel_coefficients, runs, current_root)