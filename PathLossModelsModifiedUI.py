import customtkinter as ctk
from GUIs.ModelFunctions.IndoorTransmissionLossFunction import indoor_transmission
from GUIs.ModelFunctions.SiteGeneralAboveRooftopFunction import site_general_above_rooftop
from GUIs.ModelFunctions.SiteGeneralBelowRooftopFunction import site_general_below_rooftop
from GUIs.ModelFunctions.SiteGeneralBelowRooftopToStreetFunction import site_general_below_rooftop_to_street
from GUIs.ModelFunctions.SiteSpecificBelowRooftopLoSFunction import site_specific_below_rooftop_LoS
from GUIs.ModelFunctions.SiteSpecificBelowRooftopNLoSFunction import site_specific_below_rooftop_NLoS
from GUIs.ModelFunctions.SiteSpecificAboveRooftopUrbanFunction import site_specific_above_rooftop_urban
from GUIs.ModelFunctions.SiteSpecificAboveRooftopSuburbanFunction import site_specific_above_rooftop_suburban
from GUIs.ModelFunctions.SiteSpecificBelowRooftopToStreetLoSFunction import site_specific_below_rooftop_to_street_LoS
from GUIs.ModelFunctions.SiteSpecificBelowRooftopToStreetNLoS1TurnFunction \
    import site_specific_below_rooftop_to_street_1_turn_NLoS
from GUIs.ModelFunctions.SiteSpecificBelowRooftopToStreetNLoS2TurnFunction \
    import site_specific_below_rooftop_to_street_2_turn_NLoS
from GUIs.ModelFunctions.SiteSpecificResidentialFunction import site_specific_residential

root = ctk.CTk()
root.geometry("900x500")
root.title("Scenarios for Path Loss Models")
root.config(bg="#EEF2E6")

scenario = ctk.CTkButton(root, fg_color="#FFE15D", text_color="#DC3535", hover_color="#FFE15D", height=35,
                         text_font=("Ariel", 14, "bold"), text="SELECT SCENARIO FOR CALCULATING PATH LOSS")
scenario.grid(row=0, column=1, pady=20)

button_1 = ctk.CTkButton(root, fg_color="#3B9AE1", text_color="white", hover_color="#4C9AE1",
                         height=55, text_font=("Helvetica", 13), width=350,
                         text="Indoor Transmission Loss Model", command=indoor_transmission)
button_1.grid(row=1, column=0, padx=78, pady=60)

button_2 = ctk.CTkButton(root, fg_color="#FB2576", text_color="white", hover_color="#FC3576",
                         height=55, text_font=("Helvetica", 13), width=350,
                         text="Site General Model for Above Rooftop", command=site_general_above_rooftop)
button_2.grid(row=2, column=0, padx=78, pady=60)

button_3 = ctk.CTkButton(root, fg_color="#A760FF", text_color="white", hover_color="#B860FF",
                         height=55, text_font=("Helvetica", 13), width=350,
                         text="Site General Model for Below Rooftop", command=site_general_below_rooftop)
button_3.grid(row=3, column=0, padx=78, pady=60)

button_4 = ctk.CTkButton(root, fg_color="#F10086", text_color="white", hover_color="#F21086",
                         height=55, text_font=("Helvetica", 12), width=350,
                         text="Site General Model from Below\n Rooftop to Street Level",
                         command=site_general_below_rooftop_to_street)
button_4.grid(row=4, column=0, padx=78, pady=60)

button_5 = ctk.CTkButton(root, fg_color="#764AF1", text_color="white", hover_color="#874AF1",
                         height=55, text_font=("Helvetica", 12), width=350,
                         text="Site Specific Model for Below\n Rooftop LoS",
                         command=site_specific_below_rooftop_LoS)
button_5.grid(row=1, column=1, padx=78, pady=60)

button_6 = ctk.CTkButton(root, fg_color="#3B9AE1", text_color="white", hover_color="#4C9AE1",
                         height=55, text_font=("Helvetica", 12), width=350,
                         text="Site Specific Model for Below\n Rooftop NLoS",
                         command=site_specific_below_rooftop_NLoS)
button_6.grid(row=2, column=1, padx=78, pady=60)

button_7 = ctk.CTkButton(root, fg_color="#FB2576", text_color="white", hover_color="#FC3576",
                         height=55, text_font=("Helvetica", 12), width=350,
                         text="Site Specific Model for Above\n Rooftop in Urban Scenario",
                         command=site_specific_above_rooftop_urban)
button_7.grid(row=3, column=1, padx=78, pady=60)

button_8 = ctk.CTkButton(root, fg_color="#A760FF", text_color="white", hover_color="#B860FF",
                         height=55, text_font=("Helvetica", 12), width=350,
                         text="Site Specific Model for Above\n Rooftop in Suburban Scenario",
                         command=site_specific_above_rooftop_suburban)
button_8.grid(row=4, column=1, padx=78, pady=60)

button_9 = ctk.CTkButton(root, fg_color="#F10086", text_color="white", hover_color="#F21086",
                         height=55, text_font=("Helvetica", 12), width=350,
                         text="Site Specific Model from Below\n Rooftop to Street level LoS",
                         command=site_specific_below_rooftop_to_street_LoS)
button_9.grid(row=1, column=2, padx=78, pady=60)

button_10 = ctk.CTkButton(root, fg_color="#764AF1", text_color="white", hover_color="#874AF1",
                          height=55, text_font=("Helvetica", 12), width=350,
                          text="Site Specific Model in Residential\n Environments",
                          command=site_specific_residential)
button_10.grid(row=2, column=2, padx=78, pady=60)

button_11 = ctk.CTkButton(root, fg_color="#3B9AE1", text_color="white", hover_color="#4C9AE1",
                          height=55, text_font=("Helvetica", 12), width=350,
                          text="Site Specific Model from Below Rooftop to\n Street Level for 1-turn NLoS "
                               "Propagation",
                          command=site_specific_below_rooftop_to_street_1_turn_NLoS)
button_11.grid(row=3, column=2, padx=78, pady=60)

button_12 = ctk.CTkButton(root, fg_color="#FB2576", text_color="white", hover_color="#FC3576",
                          height=55, text_font=("Helvetica", 12), width=350,
                          text="Site Specific Model from Below Rooftop to\n Street Level for 2-turn NLoS "
                               "Propagation", command=site_specific_below_rooftop_to_street_2_turn_NLoS)
button_12.grid(row=4, column=2, padx=78, pady=60)

root.mainloop()
