# Vul hier de naam van je programma in:
#fitopsy
#
# Vul hier jullie namen in:
# Willem Paternotte en Robin KUijpers
#
#
###------------------bibliotheek en globale variabelen--------------
from tkinter import *
import tkinter
from tkinter.font import Font

import pygame
from pygame import mixer

import tinytag

import SQL_fitopsy

venster = Tk()

#--------opstarten---------------------#
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("011_-_Town_Hall_Pelly.mp3")
pygame.mixer.music.play()

mainFont = Font(
    family="Comic Sans MS", #Het suprieure lettertype
    size= 20,
    )
venster.geometry("900x400")
venster.wm_title("fitopsy" )
venster["bg"] = "white"
venster.iconbitmap("fitopsy.ico")


print(venster.winfo_width)

###------------------Functie defenities-----------------------------
def zoekNummer():
    gevonden_nummer= SQL_fitopsy.getSongIDFromTable("songs", ingevoerde_nummer.get())[0]

    nummerMenu(gevonden_nummer)

def nummerMenu(id): #popup menu
    nummer = SQL_fitopsy.getSongNameFromTable(id)[0]
    artiest = SQL_fitopsy.getArtistFromSong(id)[0]

    nummer_menu =  Menu(venster, tearoff= 0)

    nummer_menu.add_command(label= nummer+" - "+artiest, command= lambda: nummerMenu(id))
    nummer_menu.add_separator()
    nummer_menu.add_command(label="Speel Nummer af", command= lambda: speelNummer(id))
    nummer_menu.add_command(label="Voeg nummer toe aan wachtrij", command= lambda: addSongWachtrij(id))

    nummer_menu.tk_popup(int(venster.winfo_width()*0.5), int(venster.winfo_height()*0.5) )
    
   
def speelNummer(nummer_id):
    nummer_Locatie = SQL_fitopsy.getSongLocationFromTable("songs", nummer_id)
    pygame.mixer.music.load(nummer_Locatie[0])
    pygame.mixer.music.play()
    # print(nummer_Locatie)

def pausePlay():
    if pygame.mixer.music.get_busy() == True:
        pygame.mixer.music.pause()
        knopPausePlay.configure(text="play")
    else:
        pygame.mixer.music.unpause()
        knopPausePlay.configure(text="pause")

def addSongWachtrij(id):
    nummer = SQL_fitopsy.getSongNameFromTable(id)[0]
    artiest = SQL_fitopsy.getArtistFromSong(id)[0]
    wachtrij.insert(END, nummer+" - "+artiest)

###------------------Hoofdprogramma---------------------------------
labelIntro = Label(venster,bg = "white", text="welkom", font = mainFont )
labelIntro.grid(row=0, column=0, sticky="W")

labelNummer = Label(venster,text="nummer:" )
labelNummer.grid(row=1, column=0, sticky="W")

ingevoerde_nummer = StringVar()
entryNummer = Entry(venster, textvariable=ingevoerde_nummer)
entryNummer.grid(row=1, column=1, sticky="E")

knopNummer = Button(venster, text="zoek nummer", width= 12, command=zoekNummer)
knopNummer.grid(row=1,column=4,sticky="W")

##BOVEN BALK
top = Frame(venster, bg="grey", width=400, height= 100)
top.place(relx=0.5, y=0, anchor=N)

knopPausePlay = Button(top, text="pause", width = 12, command=pausePlay)
knopPausePlay.place(relx=0.5, y=4, anchor=N)

#wachtrij
wachtrijFrame = Frame(top, width=30)
wachtrijFrame.place(relx=0.95, y=60, anchor=E)

wachtrij = Listbox(wachtrijFrame, bg="grey", width=20, height=5)
wachtrij.pack(pady=5)
wachtrijLabel = Label(top, text="wachtrij", width= 17)
wachtrijLabel.place(relx=0.95, y=5, anchor=E)



knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
knopSluit.grid(row=17, column=4)


venster.mainloop()


