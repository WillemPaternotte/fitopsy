# Vul hier de naam van je programma in:
#
#
# Vul hier jullie namen in:
# Willem Paternotte en Robin KUijpers
#
#
###------------------bibliotheek en globale variabelen--------------
from tkinter import *
import MCPizzeriaSQL
venster = Tk()

#--------opstarten---------------------#
venster.wm_title("MC Pizzeria" )
venster["bg"] = "black"
venster.iconbitmap("download.ico")



###------------------Functie defenities-----------------------------
def zoekKlant():
    gevonden_klanten=MCPizzeriaSQL.zoekKlantInTabel(ingevoerde_klantnaam.get())
    print(gevonden_klanten)

###------------------Hoofdprogramma---------------------------------
labelIntro = Label(venster,text="welkom" )
labelIntro.grid(row=0, column=0, sticky="W")

labelklantnaam = Label(venster,text="klantnaam:" )
labelklantnaam.grid(row=1, column=0, sticky="W")

ingevoerde_klantnaam = StringVar()
entryKlantnaam = Entry(venster, textvariable=ingevoerde_klantnaam)
entryKlantnaam.grid(row=1, column=1, sticky="w")

knopzoekopklant = Button(venster, text="zoek klant", width= 12, command=zoekKlant)
knopzoekopklant.grid(row=1,column=4,sticky="W")

knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
knopSluit.grid(row=17, column=4)

venster.mainloop()

