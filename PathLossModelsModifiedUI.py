import customtkinter
from IndoorTransmissionLossFunction import indoor_transmission

root = customtkinter.CTk()
root.geometry("900x500")


button_1 = customtkinter.CTkButton(root, fg_color="#242F9B", text_color="white", hover_color="#352F9B", width=200,
                                   height=45,
                                   text="Indoor Transmission Loss Model", command=indoor_transmission)
button_1.grid(row=0, column=0, padx=60, pady=70)

button_2 = customtkinter.CTkButton(root, fg_color="#711A75", text_color="white", hover_color="#821A75", width=200,
                                   height=45,
                                   text="Site General Model for above rooftop")
button_2.grid(row=1, column=0, padx=60, pady=70)

button_3 = customtkinter.CTkButton(root, fg_color="#A760FF", text_color="white", hover_color="#B860FF", width=200,
                                   height=45,
                                   text="Site General Model for below rooftop")
button_3.grid(row=2, column=0, padx=60, pady=70)

button_4 = customtkinter.CTkButton(root, fg_color="#F10086", text_color="white", hover_color="#F21086", width=200,
                                   height=45,
                                   text="Site General Model from below rooftop to street level")
button_4.grid(row=3, column=0, padx=60, pady=70)

button_5 = customtkinter.CTkButton(root, fg_color="#764AF1", text_color="white", hover_color="#874AF1", width=200,
                                   height=45,
                                   text="Site Specific Model for below rooftop LoS")
button_5.grid(row=0, column=1, padx=50, pady=70)

button_6 = customtkinter.CTkButton(root, fg_color="#242F9B", text_color="white", hover_color="#352F9B", width=200,
                                   height=45,
                                   text="Site Specific Model for below rooftop NLoS")
button_6.grid(row=1, column=1, padx=50, pady=70)

button_7 = customtkinter.CTkButton(root, fg_color="#711A75", text_color="white", hover_color="#821A75", width=200,
                                   height=45,
                                   text="Site Specific Model for above rooftop in Urban Scenario")
button_7.grid(row=2, column=1, padx=50, pady=70)

button_8 = customtkinter.CTkButton(root, fg_color="#A760FF", text_color="white", hover_color="#B860FF", width=200,
                                   height=45,
                                   text="Site Specific Model for above rooftop in Suburban Scenario")
button_8.grid(row=3, column=1, padx=50, pady=70)

button_9 = customtkinter.CTkButton(root, fg_color="#F10086", text_color="white", hover_color="#F21086", width=200,
                                   height=45,
                                   text="Site Specific Model from below rooftop to street level LoS")
button_9.grid(row=0, column=2, padx=50, pady=70)

button_10 = customtkinter.CTkButton(root, fg_color="#764AF1", text_color="white", hover_color="#874AF1", width=200,
                                    height=45,
                                    text="Site Specific Model from below rooftop to street level for 1 turn NLoS "
                                         "propagation")
button_10.grid(row=1, column=2, padx=50, pady=70)

button_11 = customtkinter.CTkButton(root, fg_color="#242F9B", text_color="white", hover_color="#352F9B", width=200,
                                    height=45,
                                    text="Site Specific Model from below rooftop to street level for 2 turn NLoS "
                                         "propagation")
button_11.grid(row=2, column=2, padx=50, pady=70)

button_12 = customtkinter.CTkButton(root, fg_color="#711A75", text_color="white", hover_color="#821A75", width=200,
                                    height=45,
                                    text="Site Specific Model in residential environments")
button_12.grid(row=3, column=2, padx=50, pady=70)

root.mainloop()
