# Vul hier de naam van je programma in:
#fitopsy
#
# Vul hier jullie namen in:
# Willem Paternotte en Robin KUijpers
#
#
###------------------bibliotheek en globale variabelen--------------
from tkinter import *
from tkinter.font import Font

from pygame import mixer

import SQL_fitopsy

venster = Tk()

#--------opstarten---------------------#
mainFont = Font(
    family="Comic Sans MS", #Het suprieure lettertype
    size= 20,
    )
venster.wm_title("fitopsy" )
venster["bg"] = "white"
venster.iconbitmap("fitopsy.ico")




###------------------Functie defenities-----------------------------
def zoekNummer():
    gevonden_nummer=SQL_fitopsy.getSongFromTable("songs", ingevoerde_nummer.get())
    print(gevonden_nummer)

###------------------Hoofdprogramma---------------------------------
labelIntro = Label(venster,bg = "white", text="welkom", font = mainFont )
labelIntro.grid(row=0, column=0, sticky="W")

labelNummer = Label(venster,text="nummer:" )
labelNummer.grid(row=1, column=0, sticky="W")

ingevoerde_nummer = StringVar()
entryNummer = Entry(venster, textvariable=ingevoerde_nummer)
entryNummer.grid(row=1, column=1, sticky="E")

knopNummer = Button(venster, text="zoek nummer", width= 12, command=zoekNummer)
knopNummer.grid(row=1,column=4,sticky="E")

knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
knopSluit.grid(row=17, column=4)

venster.mainloop()

