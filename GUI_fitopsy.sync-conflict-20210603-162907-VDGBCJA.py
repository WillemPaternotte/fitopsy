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
from tkinter import filedialog
from pygame import mixer

import SQL_fitopsy

venster = Tk()

#--------opstarten---------------------#
mainFont = Font(
    family="Comic Sans MS",
    size= 40,
    )
venster.wm_title("fitopsy" )
venster["bg"] = "white"
venster.iconbitmap("fitopsy.ico")




###------------------Functie defenities-----------------------------
def zoekNummer():
    gevonden_nummer=SQL_fitopsy.getSongFromTable("songs", ingevoerde_nummer.get())
    print(gevonden_nummer)

def NummerToevoegen():
    nieuw_nummer=SQL_fitopsy.addSong()

filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')

def BestandKiezen():
    file_path = filedialog.askopenfilenames
    print(file_path)

###------------------Hoofdprogramma---------------------------------
labelIntro = Label(venster,bg = "white", text="F I T O P S Y", font = mainFont )
labelIntro.grid(row=0,column=0, sticky="w")

labelNummer = Label(venster,bg ="White", text="nummer:" )
labelNummer.grid(row=1, column=0, sticky="W")

ingevoerde_nummer = StringVar()
entryNummer = Entry(venster, textvariable=ingevoerde_nummer)
entryNummer.grid(row=1, column=2, sticky="W")

knopNummer = Button(venster, text="zoek nummer", width= 14, command=zoekNummer)
knopNummer.grid(row=1, column=3, sticky="W")

LabelNummerToevoegen = Label(venster,bg="white", text=" Nummer toevoegen:")
LabelNummerToevoegen.grid(row=2, column=0, sticky="W")

NieuwNummer = StringVar()
entryNummerToevoegen = Entry(venster, textvariable=NieuwNummer)
entryNummerToevoegen.grid(row=2, column=2, sticky="W")

knopNummerToevoegen = Button(venster,text="voeg nummer toe", width=14, command=NummerToevoegen)
knopNummerToevoegen.grid(row=2, column=3, sticky="W")

knopBestand = Button(venster, text="zoek bestand", width= 14, command=BestandKiezen)
knopBestand.grid(row=3, column=3, sticky="W")

# place(relx=0.5, rely=0.5, anchor=CENTER)

# knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
# knopSluit.place(relx=0.01, rely=0.0, anchor=NE)

# knopNummer = Button(venster, text="zoek nummer", width= 12, command=VoegnummerToe)
# knopNummer.grid(row=2,column=4,sticky="W")

venster.mainloop()

