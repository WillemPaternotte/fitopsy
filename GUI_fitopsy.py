# Vul hier de naam van je programma in:
#fitopsy
#
# Vul hier jullie namen in:
# Willem Paternotte en Robin KUijpers
#
#
###------------------bibliotheek en globale variabelen--------------

from os import name

from tkinter import *
import tkinter
from tkinter.font import Font
from tkinter import filedialog

import pygame 
from pygame import Color, mixer

from tinytag import TinyTag #VOOR META DATA MP3 BESTANDEN
import tkinter as tk # voor popup scherm check

import datetime


import SQL_fitopsy



venster = Tk()

global playing 
playing = ""
global playlistVensterActive
playlistvensterActive = False

playlist_naam = StringVar()
#--------opstarten---------------------#
pygame.init()
pygame.mixer.init()


titelFont = Font(
    family="Comic Sans MS",
    size= 20,
    )

mainFont = Font(
    family="Comic Sans MS",
    size= 9,
    )
    
venster.geometry("900x400")
venster.wm_title("fitopsy" )
venster["bg"] = "#1ED760"
venster.iconbitmap("fitopsy.ico")

green = "#1ED760"
black = "#F0F0F0"
# black = "#191414"

#globale variabele voor het tonen van nummerGegevens
name = ""
artist = ""
genre = ""
file_path = ""
album = ""
bitrate = 0
year = 0


###------------------Functie defenities-----------------------------

#zoeken functies
def zoekNummer():
    zoekResultaten.delete(0, END)
    nummerResultaten = SQL_fitopsy.getSongIDsFromTable("songs", ingevoerde_nummer.get())#meerdere resultaten
    artiestResultaten = SQL_fitopsy.getSongIDsFromArtists(ingevoerde_nummer.get())
    IDs = nummerResultaten+artiestResultaten
    IDs = list(dict.fromkeys(IDs))
    for id in IDs:#meerdere resultaten in listbox stoppen
        nummer = SQL_fitopsy.getSongNameFromTable(id[0])[0]
        artiest = SQL_fitopsy.getArtistFromSong(id[0])[0]
        zoekResultaten.insert(END, nummer+" - "+artiest)

def selecterenZoeken(event):#activeert popu bij selectie in list box
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        nummer = event.widget.get(index)
        nummer = nummer.split(" -")#pakt alleen nummer(hij krijgt nummer - artiest bij selecteren)
        nummer_id= SQL_fitopsy.getSongIDFromTable("songs", nummer[0])[0]#tuple erin, tuple eruit.
        nummerMenu(nummer_id)
    
def nummerMenu(id): #popup menu
    nummer = SQL_fitopsy.getSongNameFromTable(id)[0]
    artiest = SQL_fitopsy.getArtistFromSong(id)[0]

    nummer_menu =  Menu(venster, tearoff= 0)#zorgt dat je niet tear off kan doen(tearoff is het menu los maken)

    nummer_menu.add_command(label= nummer+" - "+artiest, command= lambda: nummerMenu(id))#knop heropent popup, zo kan je een label toevoegen aan het menu
    nummer_menu.add_separator()
    nummer_menu.add_command(label="Speel Nummer af", command= lambda: speelNummer(id))
    nummer_menu.add_command(label="Voeg nummer toe aan wachtrij", command= lambda: addSongWachtrij(id))
    nummer_menu.add_command(label="Voeg nummer toe aan Playlist", command= lambda: addSongPlaylistMenu(id, x,y))
    #voeg hier meer commands toe


    x = venster.winfo_pointerx() - venster.winfo_vrootx()
    y = venster.winfo_pointery() - venster.winfo_vrooty()
    nummer_menu.tk_popup(x, y )

#afpselen en wachtrij functies  
def speelNummer(nummer_id):#speelt nummer af
    nummer_Locatie = SQL_fitopsy.getSongLocationFromTable("songs", nummer_id)#is tuple
    global playing
    playing = nummer_Locatie[0]
    pygame.mixer.music.load(nummer_Locatie[0])
    pygame.mixer.music.play()    

def speelPlaylist(playlist): #speelt eerste nummer playlist en stop de rest in wachtrij 
    wachtrij.delete(0, END)
    songlist =  SQL_fitopsy.getSongIDsFromPlaylist(playlist)
    speelNummer(songlist[0][0])
    for x in range(len(songlist)-1):#lengte is 1 korter want eerste nummer is al aan het spelen
        addSongWachtrij(songlist[x+1][0])#omdat de lengte 1 korter is moet die index 1 groter om het juiste nummer toetevoegen

def afspeelTijd(): #display afspeeltijd en wachtrij loop
    if not(playing == ""):
        huidige_tijd = datetime.timedelta(seconds = int(pygame.mixer.music.get_pos()/1000))
        tag = TinyTag.get(playing) #tinytag initialisatie
        totaal_tijd = int(tag.duration) #duration is sec
        mooie_totaal_tijd = datetime.timedelta(seconds = totaal_tijd)
        tijdLabel.configure(text= str(huidige_tijd) +" - "+str( mooie_totaal_tijd))

        if int(pygame.mixer.music.get_pos()/1000) >= (totaal_tijd-1):#check voor volgende nummer in deze functie anders hebben we 2 loop functies en dat is minder efficient
            volgendNummerWachtrij()

    tijdLabel.after(1000,afspeelTijd)#loop iedere seconde

def pausePlay():
    if pygame.mixer.music.get_busy() == True:
        pygame.mixer.music.pause()
        knopPausePlay.configure(text="play")
    else:
        pygame.mixer.music.unpause()
        knopPausePlay.configure(text="pause")
        
def addSongWachtrij(id): #voegt 1 nummer toe aan wachtrij
    nummer = SQL_fitopsy.getSongNameFromTable(id)[0]
    artiest = SQL_fitopsy.getArtistFromSong(id)[0]
    wachtrij.insert(END, nummer+" - "+artiest)#nummer als laatse in wachtrij

def addPlaylistWachtrij(playlist): #voegt alle nummers van playlist toe aan wachtrij
    songlist =  SQL_fitopsy.getSongIDsFromPlaylist(playlist)
    for x in range(len(songlist)):
        addSongWachtrij(songlist[x][0])

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

#playlist functies
def playlistListboxVullen(resulutaten):#voegt alle playlist toe aan listbox playlist
    for resultaat in resulutaten:
        playlistListbox.insert(END, resultaat)
        
def selecterenPlaylist(event):#activeert popup bij selectie in list box voor playlist
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        playlist = event.widget.get(index)
        playlistMenu(playlist[0])
        
def playlistMenu(playlist):# menu voor opites playlist
    playlist_menu =  Menu(venster, tearoff= 0)

    playlist_menu.add_command(label= playlist, command= lambda: playlistMenu(playlist))#knop heropent popup, zo kan je een label toevoegen aan het menu
    playlist_menu.add_separator()
    playlist_menu.add_command(label="Speel playlist af", command= lambda: speelPlaylist(playlist))
    playlist_menu.add_command(label="Voeg playlist toe aan wachtrij", command= lambda: addPlaylistWachtrij(playlist))
    #voeg hier meer commands toe

    #vind x en y en plaats daar popup
    x = venster.winfo_pointerx() - venster.winfo_vrootx()
    y = venster.winfo_pointery() - venster.winfo_vrooty()
    playlist_menu.tk_popup(x, y )
    
def voegPlaylistToe():#maakt playlist aan in database en listbox
    naam = playlist_naam.get()
    if naam != "" :
        SQL_fitopsy.addPlaylist(naam)#voeg to aan database
        playlistListbox.insert(END, naam)#update list box met nieuwe playlist

def addSongPlaylistMenu(id, x,y):#popup voor als je een nummer aan een playlist wilt toevoegen
    nummer = SQL_fitopsy.getSongNameFromTable(id)[0]
    artiest = SQL_fitopsy.getArtistFromSong(id)[0]
    
    addSongPlaylist_menu =  Menu(venster, tearoff= 0)

    addSongPlaylist_menu.add_command(label= nummer+" - "+artiest, command= lambda: addSongPlaylistMenu(id))#knop heropent popup, zo kan je een label toevoegen aan het menu
    addSongPlaylist_menu.add_separator()
    playlists = Menu(venster, tearoff= 0)
    addSongPlaylist_menu.add_cascade(label = "selecteer playlist", menu= playlists)
    allPlaylists = SQL_fitopsy.getAllPlaylists()
    for playlist in allPlaylists:#maakt voor elke playlist een menu knop aan
        playlists.add_command(label = playlist, command=lambda: addSongPlaylist(nummer, playlist))


    addSongPlaylist_menu.tk_popup(x, y )

def addSongPlaylist(nummer, playlist):#voegt een nummer met playlist samen sql functie
    SQL_fitopsy.addSongOnPlaylist(nummer, playlist[0])

#Nummer toevoegen functies(robin)
def BestandKiezen(): #zorgt ervoor dat windows verkenner opent, zodat filepath niet handmatigf moet worden ingevuld
    global file_path
    file_path = StringVar()
    file_path = filedialog.askopenfilenames(filetypes=(("mp3 files","*.mp3"),("FLAC files","*.flac"),("wav files","*.wav"),("All files","*.*"))) #bepaalt welke bestandtypes gezein kunnen worden
    # print(file_path)
    return(file_path)

def metadata(file_path):
    global name
    global artist
    global genre
    global album
    global bitrate
    global year
    tag = TinyTag.get(file_path)

    name = tag.title
    artist = tag.artist
    genre = tag.genre
    album = tag.album
    bitrate = tag.bitrate
    year = tag.year
    streams = 0

    nieuw_nummer=SQL_fitopsy.addSong(name,artist,genre,file_path,0)

    nummerGegevens()
    # print("hola",name)

def nummerGegevens():

    popup = Tk()
    popup.wm_title("fitopsy" )
    popup["bg"] = "white"
    popup.iconbitmap("fitopsy.ico")
    popup.geometry("300x120")

    labelNummer = Label(popup,bg ="White", text="Titel:     "+ name)
    labelNummer.grid(row=2, column=0, sticky="W")

    labelArtist = Label(popup,bg ="White", text="Artiest: "+ artist)
    labelArtist.grid(row=1, column=0, sticky="W")

    labelGenre = Label(popup,bg ="White", text="Genre:  "+ genre)
    labelGenre.grid(row=3, column=0, sticky="W")

    labelInfo = Label(popup,bg ="White", text="Info")
    labelInfo.grid(row=0, column=0, sticky="W")

    labelExtraInfo = Label(popup,bg ="White", text="extra info")
    labelExtraInfo.grid(row=0, column=2, sticky="W")

    labelAlbum = Label(popup,bg ="White", text="Album:  "+album)
    labelAlbum.grid(row=1, column=2, sticky="W")

    labelBitrate = Label(popup,bg ="White", text="Bitrate:   "+str(round(bitrate))+"kBits/s")
    labelBitrate.grid(row=2, column=2, sticky="W")
    
    labelYear = Label(popup,bg ="White", text="Jaar:        "+str(year))
    labelYear.grid(row=3, column=2, sticky="W")

    LabelSluiten = Button(popup,bg="white", text=" ok ", command= popup.destroy)
    LabelSluiten.place(relx= 0.5, rely= 0.8)
    
def NummerToevoegen():
    name = ingevoerde_name.get()
    artist = ingevoerde_artist.get()
    genre = ingevoerde_genre.get()
    file_path = ingevoerde_file_path.get()
    # print("name::",name)
    nieuw_nummer=SQL_fitopsy.addSong(name,artist,genre,file_path,0)
    print(f"{name =}")

def on_enter(e):
    knopNummerToevoegen['background'] = 'white'

def on_leave(e):
    knopNummerToevoegen['background'] = 'SystemButtonFace'

def HandmatigToevoegen(): #popup handmaig toevoegen
    global ingevoerde_name
    global ingevoerde_artist
    global ingevoerde_genre
    global ingevoerde_file_path

    popup = Toplevel(venster)
    # popup = Tk()
    popup.wm_title("fitopsy" )
    popup["bg"] = "white"
    popup.iconbitmap("fitopsy.ico")
    popup.geometry("300x150")

    ingevoerde_genre = StringVar()
    ingevoerde_genre.set("Hiphop") #keuzemenu voor genres
    entryGenre = OptionMenu(popup, ingevoerde_genre, "Hiphop","Rock","Pop","Klassiek","K-pop","Jazz","Disoc", "Electro","Alternatief" )
    entryGenre.grid(row=2, column=1, sticky="W")

    labelName = Label(popup,bg ="White", text="Titel:" )
    labelName.grid(row=0, column=0, sticky="W")
    
    ingevoerde_name = StringVar()
    entryName = Entry(popup, textvariable=ingevoerde_name)
    entryName.grid(row=0, column=1, sticky="W")

    labelArtist = Label(popup,bg ="White", text="Artiest:" )
    labelArtist.grid(row=1, column=0, sticky="W")
    
    ingevoerde_artist = StringVar()
    entryArtist = Entry(popup, textvariable=ingevoerde_artist)
    entryArtist.grid(row=1, column=1, sticky="W")

    LabelSluiten = Button(popup,bg="white", text=" opslaan", command=NummerToevoegen)
    LabelSluiten.place(relx=0.5,rely=0.8)

    labelGenre = Label(popup,bg ="White", text="Genre:" )
    labelGenre.grid(row=2, column=0, sticky="W")

    # ingevoerde_genre = StringVar()
    # entryGenre = Entry(popup, textvariable=ingevoerde_genre)
    # entryGenre.grid(row=2, column=1, sticky="W")

    labelFilepath = Label(popup,bg ="White", text="Filepath:" )
    labelFilepath.grid(row=3, column=0, sticky="W")

    ingevoerde_file_path = StringVar()
    entryFilepath = Entry(popup, textvariable=ingevoerde_file_path)
    entryFilepath.grid(row=3, column=1, sticky="W")

##============HOOFD PROGRAMMA==================
##====ZOEKEN===
zoeken =Frame(venster, bg= black, width=400, height= 400)
zoeken.place(relx= 0.5, y =120,anchor= N)

labelNummer = Label(zoeken,text="zoeken:", width =12 )
labelNummer.place(relx = 0, y=3, anchor= NW)

ingevoerde_nummer = StringVar()
entryNummer = Entry(zoeken, textvariable=ingevoerde_nummer, width= 40)
entryNummer.place(relx= 0.5, y = 5, anchor= N)

knopNummer = Button(zoeken, text="zoek nummer", width= 12, command=zoekNummer)
knopNummer.place(relx = 1, y = 0, anchor = NE )

    #resultaten listbox
resultatenFrame = Frame(zoeken, width=30, height=50)
resultatenFrame.place(relx=0.5, y=30, anchor=N)

zoekResultaten =  Listbox(resultatenFrame, bg= "white" , width=40, height=100)
zoekResultaten.pack(padx=5, pady=19)
resultatenLabel =  Label(resultatenFrame, text="resultaten:", width=17,)
resultatenLabel.place(relx=0.5, y=10, anchor=CENTER)

zoekResultaten.bind("<<ListboxSelect>>", selecterenZoeken)

#====PLAYLIST=====
playlistFrame = Frame(venster, bg= black , width=220, height=900)
playlistFrame.place(relx= 1, y = 0, anchor= NE)

playlistLabel = Label(playlistFrame, text="Mijn Playlists:", width= 12)
playlistLabel.place(relx= 0.5, y= 20, anchor=N)

playlistListbox = Listbox(playlistFrame, width= 30, height= 15)
playlistListbox.place(relx=0.5, y = 50, anchor= N)
playlistListboxVullen(SQL_fitopsy.getAllPlaylists())#vult listbox met al de bestaande playlists
playlistListbox.bind("<<ListboxSelect>>", selecterenPlaylist)#zorgt er voor dat functie selecterenPlaylist 

playlist_naam =StringVar()
playlistEntry = Entry(playlistFrame, textvariable=playlist_naam)
playlistEntry.place(relx=0.5, y = 330, anchor=N)

playlistToevoegenKnop = Button(playlistFrame, text="maak nieuwe playlist", width= 20, command= voegPlaylistToe)
playlistToevoegenKnop.place(relx= 0.5, y = 300, anchor=N)

##BOVEN BALK
top = Frame(venster, bg= black, width=400, height= 100)
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

wachtrij = Listbox(wachtrijFrame, bg="white", width=20, height=5)
wachtrij.pack(pady=5)
wachtrijLabel = Label(top, text="wachtrij", width= 17)
wachtrijLabel.place(relx=0.95, y=5, anchor=E)


##===Nummer Toevoegen===
left = Frame(venster, bg= black , width=220, height=900)
left.place(relx= 0, y = 0, anchor= NW)

titelLabel= Label(left, text= "FITOPSY", width= 20,fg = green, font=titelFont)
titelLabel.place(relx= 0.5, y = 20, anchor= CENTER)
subTitelLabel = Label(left, text="""Not a Spotify clone.
Robin Kuijpers en Willem Paternotte """,fg = green, font=mainFont )
subTitelLabel.place(relx= 0.5, y = 60, anchor= CENTER)

knopNummerToevoegen = Button(left,bg="#fffffb",fg="#191414",border=0 ,text="nummer toevoegen \n met metadata", width=20, command=lambda:[BestandKiezen(), metadata(file_path[0])]) 
knopNummerToevoegen.place(relx= 0.5, y = 150, anchor= CENTER)
knopNummerToevoegen.bind("<Enter>", on_enter)   #voor het effect van activebackground
knopNummerToevoegen.bind("<Leave>", on_leave)

knopNummerHandmatigToevoegen = Button(left,text="Nummer toevoegen \n zonder metadata", width=20,height=2, command=lambda: HandmatigToevoegen()) 
knopNummerHandmatigToevoegen.place(relx= 0.5, y = 200, anchor= CENTER)



##191414 spotify zwart
##1DB954 spotify groen
##fffffb wit
##ebe6e1 donker wit
afspeelTijd()
venster.mainloop()
