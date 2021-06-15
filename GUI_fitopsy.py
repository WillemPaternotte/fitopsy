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

import datetime

from tinytag import TinyTag

import SQL_fitopsy



venster = Tk()

global playing 
playing = ""
global playlistVensterActive
playlistvensterActive = False
#--------opstarten---------------------#
pygame.init()
pygame.mixer.init()


mainFont = Font(
    family="Comic Sans MS", #Het suprieure lettertype
    size= 20,
    )
venster.geometry("900x400")
venster.wm_title("fitopsy" )
venster["bg"] = "white"
venster.iconbitmap("fitopsy.ico")


###------------------Functie defenities-----------------------------
def zoekNummer():
    zoekResultaten.delete(0, END)
    nummerResultaten = SQL_fitopsy.getSongIDsFromTable("songs", ingevoerde_nummer.get())#meerdere resultaten
    artiestResultaten = SQL_fitopsy.getSongIDsFromArtists(ingevoerde_nummer.get())
    IDs = nummerResultaten+artiestResultaten
    IDs = list(dict.fromkeys(IDs))
    print(IDs)
    for id in IDs:#meerdere resultaten in listbox stoppen
        nummer = SQL_fitopsy.getSongNameFromTable(id[0])[0]
        artiest = SQL_fitopsy.getArtistFromSong(id[0])[0]
        zoekResultaten.insert(END, nummer+" - "+artiest)


def selecteren(event):#activeert popu bij selectie in list box
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        nummer = event.widget.get(index)
        nummer = nummer.split(" -")
        nummer_id= SQL_fitopsy.getSongIDFromTable("songs", nummer[0])[0]
        nummerMenu(nummer_id)
    



def nummerMenu(id): #popup menu
    nummer = SQL_fitopsy.getSongNameFromTable(id)[0]
    artiest = SQL_fitopsy.getArtistFromSong(id)[0]

    nummer_menu =  Menu(venster, tearoff= 0)

    nummer_menu.add_command(label= nummer+" - "+artiest, command= lambda: nummerMenu(id))#knop heropent popup, zo kan je een label toevoegen aan het menu
    nummer_menu.add_separator()
    nummer_menu.add_command(label="Speel Nummer af", command= lambda: speelNummer(id))
    nummer_menu.add_command(label="Voeg nummer toe aan wachtrij", command= lambda: addSongWachtrij(id))
    #voeg hier meer commands toe


    x = venster.winfo_pointerx() - venster.winfo_vrootx()
    y = venster.winfo_pointery() - venster.winfo_vrooty()
    nummer_menu.tk_popup(x, y )
    
   
def speelNummer(nummer_id):
    nummer_Locatie = SQL_fitopsy.getSongLocationFromTable("songs", nummer_id)
    global playing
    playing = nummer_Locatie[0]
    pygame.mixer.music.load(nummer_Locatie[0])
    pygame.mixer.music.play()
    # print(nummer_Locatie)

def afspeelTijd(): #display afspeeltijd en wachtrij loop
    if not(playing == ""):
        huidige_tijd = datetime.timedelta(seconds = int(pygame.mixer.music.get_pos()/1000))
        tag = TinyTag.get(playing) #tinytag initialisatie
        totaal_tijd = int(tag.duration) #duration is sec
        mooie_totaal_tijd = datetime.timedelta(seconds = totaal_tijd)
        tijdLabel.configure(text= str(huidige_tijd) +" - "+str( mooie_totaal_tijd))

        if int(pygame.mixer.music.get_pos()/1000) >= (totaal_tijd-1):#check voor volgende nummer in deze functie anders hebben we 2 loop functies en dat is minder efficient
            volgendNummerWachtrij()
            print("ja")

    tijdLabel.after(1000,afspeelTijd)#loop iedere seconde


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

def volgendNummerWachtrij():
    nummer = wachtrij.get(0) #0 is het eerste element uit de listbox
    if nummer != "":#nummer is niet None maar heeft ook geen data dus lege string
        nummer = nummer.split(" -")
        nummer_id= SQL_fitopsy.getSongIDFromTable("songs", nummer[0])[0]
        speelNummer(nummer_id)
        wachtrij.delete(0)#verwijdert eerste element uit listbox 
    else:
        pygame.mixer.music.stop()
        tijdLabel.configure(text="0:00 - 0:00")

def playlistAanmaken():
    global playlistvensterActive
    running = playlistvensterActive
    if running != True:
        playlistVenster = Tk()
        playlistVenster.wm_title("fitopsy" )
        playlistVenster["bg"] = "white"
        playlistVenster.iconbitmap("fitopsy.ico")
        playlistVenster.protocol("WM_DELETE_WINDOW", lambda: (playlistWindowDelete(), playlistVenster.destroy()))
        running = True
    playlistvensterActive = running

def playlistWindowDelete(): #global variabele update moest appart want python deed stom
    global playlistvensterActive
    playlistvensterActive = False
    
    


###------------------Hoofdprogramma---------------------------------
labelIntro = Label(venster,bg = "white", text="welkom", font = mainFont )
labelIntro.grid(row=0, column=0, sticky="W")

zoeken =Frame(venster, bg="grey", width=400, height= 400)
zoeken.place(relx= 0.5, y =105,anchor= N)

##ZOEKEN--
labelNummer = Label(zoeken,text="zoeken:", width =12 )
labelNummer.place(relx = 0, y=0, anchor= NW)

ingevoerde_nummer = StringVar()
entryNummer = Entry(zoeken, textvariable=ingevoerde_nummer)
entryNummer.place(relx= 0.5, y = 0, anchor= N)

knopNummer = Button(zoeken, text="zoek nummer", width= 12, command=zoekNummer)
knopNummer.place(relx = 1, y = 0, anchor = NE )

#resultaten listbox
resultatenFrame = Frame(zoeken, width=30, height=50)
resultatenFrame.place(relx=0.5, y=30, anchor=N)

zoekResultaten =  Listbox(resultatenFrame, bg="grey", width=30, height=5)
zoekResultaten.pack(padx=5, pady=19)
resultatenLabel =  Label(resultatenFrame, text="resultaten:", width=17,)
resultatenLabel.place(relx=0.5, rely=0.1, anchor=CENTER)

zoekResultaten.bind("<<ListboxSelect>>", selecteren)

#PLAYLIST
playlistFrame = Frame(venster, bg="grey", width=200, height=900)
playlistFrame.place(relx= 1, y = 0, anchor= NE)

playlistLabel = Label(playlistFrame, text="Mijn Playlists:", width= 12)
playlistLabel.place(relx= 0.5, y= 20, anchor=N)

playlistToevoegenKnop = Button(playlistFrame, text="maak nieuwe playlist", width= 20, command= lambda:playlistAanmaken())
playlistToevoegenKnop.place(relx= 0.5, y = 40, anchor=N)
##BOVEN BALK
top = Frame(venster, bg="grey", width=400, height= 100)
top.place(relx=0.5, y=0, anchor=N)

knopPausePlay = Button(top, text="pause", width = 12, command=pausePlay)
knopPausePlay.place(relx=0.5, y=4, anchor=N)

knopVolgende = Button(top, text = "next", width=12, command= volgendNummerWachtrij)
knopVolgende.place(relx=0.5, y=70, anchor=N)

tijdLabel = Label(top, text="0:00 - 0:00", width = 14)
tijdLabel.place(relx = 0.5, y= 40, anchor=N)

#wachtrij
wachtrijFrame = Frame(top, width=30)
wachtrijFrame.place(relx=0.95, y=60, anchor=E)

wachtrij = Listbox(wachtrijFrame, bg="grey", width=20, height=5)
wachtrij.pack(pady=5)
wachtrijLabel = Label(top, text="wachtrij", width= 17)
wachtrijLabel.place(relx=0.95, y=5, anchor=E)



# knopSluit = Button(venster, text="Sluiten", width=12, command=venster.destroy)
# knopSluit.grid(row=17, column=4)

afspeelTijd()
venster.mainloop()


