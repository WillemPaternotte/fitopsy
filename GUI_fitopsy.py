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
from tinytag import TinyTag #VOOR META DATA MP3 BESTANDEN

import SQL_fitopsy

venster = Tk()

#--------opstarten---------------------#
venster.geometry("600x600") #bepaalt grootte window
mainFont = Font(
    family="Comic Sans MS",
    size= 40,
    )
venster.wm_title("fitopsy" )
venster["bg"] = "white"
venster.iconbitmap("fitopsy.ico")


# tag = TinyTag.get("C:/Users/robin/Sync/leerjaar 5/informatica/SQL/music/Future, Drake - Life Is Good.mp3") 
# tag = TinyTag.get('C:/Users/robin/Sync/leerjaar 5/informatica/SQL/music/Future, Drake - Life Is Good.mp3',) 

###------------------Functie defenities-----------------------------
def zoekNummer():
    gevonden_nummer=SQL_fitopsy.getSongFromTable("songs", ingevoerde_nummer.get())
    print(gevonden_nummer)

def BestandKiezen(): #zorgt ervoor dat windows verkenner opent, zodat filepath niet handmatigf moet worden ingevuld
    global file_path
    file_path = filedialog.askopenfilenames(filetypes=(("mp3 files","*.mp3"),("flac files","*.flac"),("wav files","*.wav"),("All files","*.*"))) #bepaalt welke bestandtypes gezein kunnen worden
    print(file_path)
    return(file_path)

# def metadata(file_path):
#     tag = TinyTag.get("file_path")
#     album = tag.album
#     print(album)

# filePath = BestandKiezen()

def NummerToevoegen():
    nieuw_nummer=SQL_fitopsy.addSong()



###------------------Hoofdprogramma---------------------------------
labelIntro = Label(venster,bg = "white", text="F I T O P S Y", font = mainFont ) #titel
labelIntro.grid(row=0,column=0, sticky="w")

labelNummer = Label(venster,bg ="White", text="nummer:" ) #nummerzoeken
labelNummer.grid(row=1, column=0, sticky="W")

ingevoerde_nummer = StringVar()
entryNummer = Entry(venster, textvariable=ingevoerde_nummer) #nummerzoeken
entryNummer.grid(row=1, column=2, sticky="W")

knopNummer = Button(venster, text="zoek nummer", width= 14, command=zoekNummer) #nummerzoeken
knopNummer.grid(row=1, column=3, sticky="W")

LabelNummerToevoegen = Label(venster,bg="white", text=" Nummer toevoegen:") #nummertoevoegen
LabelNummerToevoegen.grid(row=2, column=0, sticky="W")

NieuwNummer = StringVar()
entryNummerToevoegen = Entry(venster, textvariable=NieuwNummer) #nummertoevoegen
entryNummerToevoegen.grid(row=2, column=2, sticky="W")

knopNummerToevoegen = Button(venster,text="voeg nummer toe", width=14, command=NummerToevoegen) #nummertoevoegen
knopNummerToevoegen.grid(row=2, column=3, sticky="W")

knopBestand = Button(venster, text="zoek bestand", width= 14, command=BestandKiezen) #bestand
knopBestand.grid(row=3, column=3, sticky="W")

# knopBestand = Button(venster, text="zoek bestand", width= 14, command=lambda:[BestandKiezen(), metadata(file_path)]) #bestand
# knopBestand.grid(row=3, column=3, sticky="W")

# place(relx=0.5, rely=0.5, anchor=CENTER)

# knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
# knopSluit.place(relx=0.01, rely=0.0, anchor=NE)

# knopNummer = Button(venster, text="zoek nummer", width= 12, command=VoegnummerToe)
# knopNummer.grid(row=2,column=4,sticky="W")

venster.mainloop()

